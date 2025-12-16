import streamlit as st

st.set_page_config(page_title="BTC Phoenix", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("🔐 BTC Phoenix Login")
    email = st.text_input("Email")

    if st.button("Login") and email:
        st.session_state.logged_in = True
        st.rerun()

def dashboard():
    st.title("📊 BTC Phoenix Dashboard")
    st.success("Login successful")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

if st.session_state.logged_in:
    dashboard()
else:
    login_page()
    
