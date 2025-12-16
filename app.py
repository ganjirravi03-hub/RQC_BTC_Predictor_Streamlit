import streamlit as st
import sqlite3
import bcrypt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", page_icon="🔐", layout="centered")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password BLOB
)
""")
conn.commit()

# ---------------- HELPERS ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def user_exists(email):
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    return c.fetchone() is not None

def create_user(email, password):
    hashed = hash_password(password)
    c.execute("INSERT INTO users VALUES (?, ?)", (email, hashed))
    conn.commit()

def authenticate(email, password):
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    if result:
        return verify_password(password, result[0])
    return False

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- UI ----------------
st.title("🔐 BTC Phoenix Secure Login")

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------- LOGIN ----------
with tab1:
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if authenticate(email, password):
            st.session_state.logged_in = True
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid email or password")

# ---------- REGISTER ----------
with tab2:
    new_email = st.text_input("📧 New Email")
    new_password = st.text_input("🔑 New Password", type="password")

    if st.button("Register"):
        if user_exists(new_email):
            st.error("❌ Email already exists")
        else:
            create_user(new_email, new_password)
            st.success("✅ Registration successful. Now login.")

# ---------------- DASHBOARD ----------------
if st.session_state.logged_in:
    st.success("🎉 Welcome to BTC Phoenix Dashboard")
    st.write("🚀 Next step: BTC Live Data & Prediction")
    
