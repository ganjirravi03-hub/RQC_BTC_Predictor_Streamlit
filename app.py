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

# ---------------- USER DB ----------------
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

# ---------------- AUTH ----------------
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

# ---------------- BTC DATA (LIVE + FALLBACK) ----------------
def get_btc_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": 1, "interval": "minute"}
        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            raise Exception("API error")

        data = r.json()
        prices = data.get("prices", [])

        if not prices:
            raise Exception("Empty data")

        df = pd.DataFrame(prices, columns=["time", "price"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df["source"] = "LIVE"
        return df

    except Exception:
        # -------- FALLBACK DEMO DATA --------
        times = pd.date_range(end=datetime.now(), periods=60, freq="min")
        prices = [87000 + i * 2 for i in range(60)]

        df = pd.DataFrame({
            "time": times,
            "price": prices,
            "source": "DEMO"
        })
        return df

# ---------------- SIMPLE PREDICTION ----------------
def btc_prediction(df):
    if len(df) < 10:
        return "HOLD", "Low data"

    diff = df["price"].iloc[-1] - df["price"].iloc[-10]

    if diff > 0:
        return "BUY", "Uptrend momentum"
    elif diff < 0:
        return "SELL", "Downtrend momentum"
    else:
        return "HOLD", "Sideways market"

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("📊 BTC Phoenix Dashboard")
    st.caption(f"Welcome {st.session_state.user}")

    df = get_btc_data()
    latest_price = df["price"].iloc[-1]
    source = df["source"].iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 BTC Price (USD)", f"${latest_price:,.2f}")

    with col2:
        if source == "LIVE":
            st.success("Source: CoinGecko (Live)")
        else:
            st.warning("Source: Demo / Fallback")

    with col3:
        signal, reason = btc_prediction(df)
        if signal == "BUY":
            st.success("🟢 BUY")
        elif signal == "SELL":
            st.error("🔴 SELL")
        else:
            st.warning("🟡 HOLD")

    # -------- CHART --------
    st.subheader("📈 BTC Price Chart (Last 24 Hours)")
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(x="time:T", y="price:Q", tooltip=["price"])
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

    st.caption(f"Last update: {df['time'].iloc[-1]}")
    st.caption("⚠️ Educational purpose only. Not financial advice.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
                            
