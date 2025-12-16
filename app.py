import streamlit as st

st.set_page_config(page_title="BTC Phoenix Dashboard", layout="centered")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("🔐 BTC Phoenix Login")
    st.caption("Enter email to access dashboard")

    email = st.text_input("📧 Email")
    if st.button("Login") and email:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.experimental_rerun()

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("📊 BTC Phoenix Dashboard")

    st.success(f"Welcome, {st.session_state.user_email}")
    st.info("Plan: FREE USER")

    st.markdown("### 📈 Trading")
    st.page_link("pages/1_BTC_Signal.py", label="➡️ Open BTC Signal")

    st.markdown("### 📚 Learning (Coming Soon)")
    st.write("- BTC Basics")
    st.write("- Risk Management")
    st.write("- AI Trading Concepts")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
    
