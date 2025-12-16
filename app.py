import streamlit as st
import requests
import pandas as pd
import altair as alt
import bcrypt
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", layout="wide")
USER_FILE = "users.json"

# ---------------- USER DB HELPERS ----------------
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH PAGE ----------------
def auth_page():
    st.title("🔐 BTC Phoenix Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])
    users = load_users()

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email in users and check_password(password, users[email]):
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
                users[r_email] = hash_password(r_password)
                save_users(users)
                st.success("Registration successful. Please login.")

# ---------------- BTC DATA (SAFE) ----------------
def get_btc_data():
    try:
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

    except Exception:
        return pd.DataFrame()

# ---------------- DASHBOARD (FINAL FIXED) ----------------
def dashboard():
    st.title("📊 BTC Phoenix Dashboard")
    st.success(f"Welcome {st.session_state.user}")

    df = get_btc_data()

    if df.empty:
        st.warning("⚠️ Live BTC data temporarily unavailable. Refresh after 1 min.")
        st.stop()

    latest_price = float(df["price"].iloc[-1])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 BTC Price (USD)", f"${latest_price:,.2f}")
        st.caption("Source: CoinGecko (Live)")
    with col2:
        st.info("Next Phase: ML Prediction • Paid Access • APK")

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="time:T",
            y="price:Q",
            tooltip=["time:T", "price:Q"]
        )
        .properties(height=400)
    )

    st.subheader("📈 BTC Price Chart (Last 24 Hours)")
    st.altair_chart(chart, use_container_width=True)

    st.caption(f"Last update: {df['time'].iloc[-1]}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
    
