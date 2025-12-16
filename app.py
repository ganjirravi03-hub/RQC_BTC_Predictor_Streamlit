import streamlit as st
import sqlite3
import bcrypt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", layout="centered")

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
    st.session_state.user_email = ""

# ---------------- HELPERS ----------------
def register_user(email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users VALUES (?,?)", (email, hashed))
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    data = c.fetchone()
    if data and bcrypt.checkpw(password.encode(), data[0]):
        return True
    return False

# ---------------- UI ----------------
st.title("🔐 BTC Phoenix Secure Login")

menu = st.tabs(["Login", "Register"])

# -------- LOGIN --------
with menu[0]:
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if login_user(email, password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login successful")
        else:
            st.error("Invalid email or password")

# -------- REGISTER --------
with menu[1]:
    st.subheader("Register")
    new_email = st.text_input("New Email")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):
        if register_user(new_email, new_pass):
            st.success("Registration successful. Now login.")
        else:
            st.error("Email already exists")

# ---------------- DASHBOARD ----------------
if st.session_state.logged_in:
    st.divider()
    st.success(f"Welcome {st.session_state.user_email}")
    st.header("📊 BTC Dashboard")

    st.metric("BTC Price", "$ Loading...")
    st.info("Next: BTC chart + ML prediction")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()
        
