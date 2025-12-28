import streamlit as st
import requests
import pandas as pd
import altair as alt
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(
    page_title="BTC Phoenix",
    layout="wide",
    initial_sidebar_state="collapsed"
)

RAZORPAY_LINK = "https://rzp.io/l/btcphoenix199"

# ================= FIREBASE INIT =================
# ⛔ serviceAccountKey.json file same folder me honi chahiye
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= BTC DATA =================
@st.cache_data(ttl=60)
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": 1}
    r = requests.get(url, params=params, timeout=10)
    data = r.json().get("prices", [])
    df = pd.DataFrame(data, columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# ================= AUTH PAGE =================
def auth_page():
    st.title("🔐 BTC Phoenix Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------- LOGIN ----------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            try:
                auth.get_user_by_email(email)
                st.session_state.user = email
                st.success("✅ Login Successful")
                st.rerun()
            except:
                st.error("❌ User not found")

    # ---------- REGISTER ----------
    with tab2:
        r_email = st.text_input("New Email", key="reg_email")
        r_pass = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Create Account"):
            try:
                auth.create_user(email=r_email, password=r_pass)
                db.collection("users").document(r_email).set({
                    "paid": False,
                    "created": datetime.utcnow()
                })
                st.success("✅ Account Created. Login Now.")
            except Exception as e:
                st.error("❌ Error creating account")

# ================= DASHBOARD =================
def dashboard():
    st.title("📊 BTC Phoenix Dashboard")
    st.caption(f"👤 {st.session_state.user}")

    user_doc = db.collection("users").document(st.session_state.user).get()
    paid = user_doc.to_dict().get("paid", False)

    df = get_btc_data()

    if df.empty:
        st.error("BTC data not available")
        return

    st.metric(
        "💰 BTC Price (USD)",
        f"${df['price'].iloc[-1]:,.2f}"
    )

    chart = alt.Chart(df).mark_line().encode(
        x="time:T",
        y="price:Q"
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)

    st.divider()
    st.subheader("🤖 Prediction Panel")

    if not paid:
        st.warning("🔒 Premium Locked")
        st.markdown("### 💳 Unlock Premium – ₹199")
        st.link_button("Pay with Razorpay", RAZORPAY_LINK)
        st.caption("Payment ke baad auto unlock ho jayega")
    else:
        st.success("✅ Premium Active")
        signal = "📈 UP ⬆️" if df["price"].iloc[-1] > df["price"].iloc[0] else "📉 DOWN ⬇️"
        st.metric("Market Signal", signal)
        st.caption("AI Engine Coming Soon")

    st.divider()

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ================= MAIN =================
if st.session_state.user is None:
    auth_page()
else:
    dashboard()
    
