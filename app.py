import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

# ---------------- CONFIG ----------------
APP_NAME = "BTC Phoenix"
PREMIUM_PRICE = 199

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    firebase_admin.initialize_app(
        credentials.Certificate(dict(st.secrets["firebase"]))
    )

db = firestore.client()

# ---------------- UI ----------------
st.set_page_config(page_title=APP_NAME, page_icon="🔥", layout="centered")
st.title("🔥 BTC Phoenix – AI Bitcoin Predictor")

# ---------------- AUTH ----------------
st.subheader("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        user = auth.get_user_by_email(email)
        st.session_state["user"] = email
        st.success("Login successful")
    except:
        st.error("User not found")

if "user" not in st.session_state:
    st.stop()

# ---------------- USER DATA ----------------
user_ref = db.collection("users").document(st.session_state["user"])
user_doc = user_ref.get()

if not user_doc.exists:
    user_ref.set({
        "email": st.session_state["user"],
        "paid": False,
        "amount": 0,
        "created": datetime.now()
    })

user_data = user_ref.get().to_dict()

# ---------------- BTC DATA ----------------
st.subheader("📊 Live Bitcoin Data")

btc = yf.download("BTC-USD", period="7d", interval="1h")
st.line_chart(btc["Close"])

last_prices = btc["Close"].tail(60).values

# ---------------- AI / ML SIGNAL ----------------
def ai_signal(prices):
    diff = np.mean(np.diff(prices))
    if diff > 0:
        return "📈 BUY"
    elif diff < 0:
        return "📉 SELL"
    else:
        return "⚖️ HOLD"

signal = ai_signal(last_prices)

st.subheader("🤖 AI Market Signal")
st.markdown(f"## {signal}")

# ---------------- PREMIUM LOGIC ----------------
if user_data["paid"]:
    st.success("💎 Premium User")
    st.markdown("### 🔮 Advanced AI Prediction Enabled")
else:
    st.warning("🔒 Premium Locked")

    if st.button("Unlock Premium ₹199"):
        # Razorpay webhook will update this in real use
        user_ref.update({
            "paid": True,
            "amount": PREMIUM_PRICE,
            "paid_at": datetime.now()
        })
        st.success("Premium Activated (Demo Auto-Verify)")
        st.experimental_rerun()

# ---------------- ADMIN DASHBOARD ----------------
st.divider()
st.subheader("📊 Admin Dashboard")

if st.session_state["user"] == "admin@gmail.com":
    users = db.collection("users").stream()
    total_users = 0
    paid_users = 0
    revenue = 0

    for u in users:
        total_users += 1
        d = u.to_dict()
        if d.get("paid"):
            paid_users += 1
            revenue += d.get("amount", 0)

    st.metric("👥 Total Users", total_users)
    st.metric("💎 Premium Users", paid_users)
    st.metric("💰 Revenue (₹)", revenue)

st.divider()
st.caption("⚠️ Educational purpose only. Not financial advice.")
