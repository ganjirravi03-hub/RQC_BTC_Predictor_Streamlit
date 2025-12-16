import streamlit as st
import requests
import pandas as pd
import altair as alt
import bcrypt
import json
import os
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", layout="wide")
USER_FILE = "users.json"
RAZORPAY_LINK = "https://rzp.io/l/btcphoenix199"

# ---------------- USER DB ----------------
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH ----------------
def auth_page():
    st.title("🔐 BTC Phoenix Secure Login")
    tab1, tab2 = st.tabs(["Login", "Register"])
    users = load_users()

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if email in users and check_password(password, users[email]["password"]):
                st.session_state.logged_in = True
                st.session_state.user = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        r_email = st.text_input("Email", key="r_email")
        r_password = st.text_input("Password", type="password", key="r_pass")
        if st.button("Register"):
            if r_email in users:
                st.warning("User already exists")
            else:
                users[r_email] = {
                    "password": hash_password(r_password),
                    "paid": False,
                    "created": str(datetime.utcnow())
                }
                save_users(users)
                st.success("Registration successful. Please login.")

# ---------------- BTC DATA ----------------
@st.cache_data(ttl=60)
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": 1}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    prices = data.get("prices", [])
    if not prices:
        return pd.DataFrame()
    df = pd.DataFrame(prices, columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# ---------------- RULE BASED PREDICTION ----------------
def rule_based_prediction(prices):
    if len(prices) < 10:
        return "⚖️ SIDEWAYS"

    first = prices[0]
    last = prices[-1]

    if last > first:
        return "📈 UP ⬆️ (Bullish)"
    elif last < first:
        return "📉 DOWN ⬇️ (Bearish)"
    else:
        return "⚖️ SIDEWAYS"

# ---------------- DASHBOARD ----------------
def dashboard():
    users = load_users()
    user = users[st.session_state.user]

    st.title("📊 BTC Phoenix Dashboard")
    st.caption(f"Welcome {st.session_state.user}")

    df = get_btc_data()
    if df.empty:
        st.warning("BTC data unavailable. Refresh.")
        st.stop()

    st.metric("💰 BTC Price (USD)", f"${df['price'].iloc[-1]:,.2f}")

    chart = alt.Chart(df).mark_line().encode(
        x="time:T",
        y="price:Q"
    ).properties(height=350)

    st.altair_chart(chart, width="stretch")

    st.divider()
    st.subheader("🤖 BTC Prediction Panel")

    if not user["paid"]:
        st.warning("🔒 Premium feature locked")
        st.markdown("### 💳 Unlock Premium – ₹199")
        st.link_button("Pay with Razorpay", RAZORPAY_LINK)

        if st.button("✅ I have paid"):
            users[st.session_state.user]["paid"] = True
            save_users(users)
            st.success("Payment verified. Access granted.")
            st.rerun()
    else:
        st.success("✅ Premium Access Active")

        last_prices = df["price"].iloc[-10:].tolist()
        signal = rule_based_prediction(last_prices)

        st.metric("📊 Market Signal", signal)
        st.caption("Rule-Based Smart Analysis | ML Upgrade Coming")

    st.divider()
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
    
