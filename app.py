import streamlit as st
import bcrypt
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", page_icon="🔐", layout="centered")

USER_DB = "users.json"

# ---------------- HELPERS ----------------
def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------------- DASHBOARD ----------------
def dashboard():
    st.success(f"✅ Welcome {st.session_state.user_email}")
    st.header("📊 BTC Phoenix Dashboard")

    st.write("🔒 Your account is secure.")
    st.write("🚀 Prediction system coming next.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

# ---------------- AUTH UI ----------------
def auth_page():
    st.title("🔐 BTC Phoenix Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    users = load_users()

    # -------- LOGIN --------
    with tab1:
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            if email in users and verify_password(password, users[email]):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

    # -------- REGISTER --------
    with tab2:
        new_email = st.text_input("📧 New Email")
        new_password = st.text_input("🔑 New Password", type="password")

        if st.button("Register"):
            if new_email in users:
                st.warning("⚠️ Email already registered")
            elif len(new_password) < 6:
                st.warning("⚠️ Password minimum 6 characters")
            else:
                users[new_email] = hash_password(new_password)
                save_users(users)
                st.success("✅ Registration successful. Now login.")

# ---------------- MAIN ----------------
if st.session_state.logged_in:
    dashboard()
else:
    auth_page()
                
