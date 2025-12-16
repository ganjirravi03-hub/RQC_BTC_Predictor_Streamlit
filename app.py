import streamlit as st
import sqlite3
import bcrypt
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", page_icon="🔐", layout="centered")

# ---------------- DB ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password BLOB
)
""")
conn.commit()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ---------------- HELPERS ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def get_btc_price():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd"},
            timeout=10
        )
        return r.json()["bitcoin"]["usd"]
    except:
        return None

# ---------------- LOGIN PAGE ----------------
def login_register():
    st.markdown("## 🔐 BTC Phoenix Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------- LOGIN ----------
    with tab1:
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            c.execute("SELECT password FROM users WHERE email=?", (email,))
            row = c.fetchone()

            if row and check_password(password, row[0]):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

    # ---------- REGISTER ----------
    with tab2:
        new_email = st.text_input("📧 New Email")
        new_password = st.text_input("🔑 New Password", type="password")

        if st.button("Register"):
            c.execute("SELECT * FROM users WHERE email=?", (new_email,))
            if c.fetchone():
                st.error("Email already exists")
            else:
                hashed = hash_password(new_password)
                c.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (new_email, hashed)
                )
                conn.commit()
                st.success("✅ Registration successful. Now login.")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.markdown("## 🚀 BTC Phoenix Dashboard")
    st.write(f"👤 Logged in as: **{st.session_state.user_email}**")

    price = get_btc_price()
    if price:
        st.metric("💰 Bitcoin Price (USD)", f"${price:,}")
    else:
        st.error("Failed to fetch BTC price")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()

# ---------------- ROUTER ----------------
if st.session_state.logged_in:
    dashboard()
else:
    login_register()
    
