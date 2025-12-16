import streamlit as st
import requests
import pandas as pd
import altair as alt
import bcrypt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", layout="wide")

# ---------------- SIMPLE USER STORE (DEMO SAFE) ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- AUTH FUNCTIONS ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# ---------------- LOGIN / REGISTER ----------------
def auth_page():
    st.title("🔐 BTC Phoenix Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if email in st.session_state.users:
                if check_password(password, st.session_state.users[email]):
                    st.session_state.logged_in = True
                    st.session_state.user = email
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Wrong password")
            else:
                st.error("User not found")

    with tab2:
        r_email = st.text_input("Email", key="reg_email")
        r_password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if r_email in st.session_state.users:
                st.warning("User already exists")
            else:
                st.session_state.users[r_email] = hash_password(r_password)
                st.success("Registration successful. Please login.")

# ---------------- BTC DATA ----------------
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": 1, "interval": "minute"}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("📊 BTC Phoenix Dashboard")
    st.caption("Live BTC price • Phase 1 (Stable)")

    try:
        df = get_btc_data()
        latest_price = df.iloc[-1]["price"]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 BTC Price (USD)", f"${latest_price:,.2f}")
            st.success("Data Source: LIVE (CoinGecko)")

        with col2:
            st.info("Next: Chart + ML prediction")

        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x="time:T",
                y="price:Q",
                tooltip=["price"]
            )
            .properties(height=400)
        )

        st.subheader("📈 BTC Price Chart (Last 24h)")
        st.altair_chart(chart, use_container_width=True)

        st.caption(f"Last update: {df.iloc[-1]['time']}")

    except Exception as e:
        st.error("Live data failed. Please refresh.")
        st.code(str(e))

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    auth_page()
else:
    dashboard()
    
