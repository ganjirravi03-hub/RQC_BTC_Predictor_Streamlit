import streamlit as st
import sqlite3
import bcrypt

st.set_page_config(page_title="BTC Phoenix Secure", layout="centered")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password BLOB
)
""")
conn.commit()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# ---------------- AUTH FUNCTIONS ----------------
def register_user(email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?,?)", (email, hashed))
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    data = c.fetchone()
    if data and bcrypt.checkpw(password.encode(), bytes(data[0])):
        return True
    return False

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("🔐 BTC Phoenix Secure Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Password", type="password", key="login_pass")

        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        new_email = st.text_input("📧 New Email", key="reg_email")
        new_pass = st.text_input("🔑 New Password", type="password", key="reg_pass")

        if st.button("Register"):
            if register_user(new_email, new_pass):
                st.success("Registration successful. Now login.")
            else:
                st.error("Email already exists")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("📊 BTC Phoenix Dashboard")
    st.success(f"Welcome, {st.session_state.user_email}")

    st.markdown("### 📈 Trading")
    st.page_link("pages/1_BTC_Signal.py", label="➡️ Open BTC Signal")

    st.markdown("### 🔒 Security Status")
    st.info("✔ Password Protected\n✔ User Isolated\n✔ No Misuse")

    st.markdown("### ⚠️ Disclaimer")
    st.caption("This is not financial advice. Trade at your own risk.")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

# ---------------- MAIN ----------------
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
