import streamlit as st
import requests
import pandas as pd
import altair as alt
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime
from openai import OpenAI

# ================= CONFIG =================
st.set_page_config(page_title="BTC Phoenix", layout="wide")

RAZORPAY_LINK = "https://rzp.io/l/btcphoenix199"
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# ================= FIREBASE =================
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
    r = requests.get(url, params=params)
    data = r.json().get("prices", [])

    df = pd.DataFrame(data, columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# ================= AUTH =================
def auth_page():
    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email")
        if st.button("Login"):
            try:
                auth.get_user_by_email(email)
                st.session_state.user = email
                st.success("Login Successful")
                st.rerun()
            except:
                st.error("User not found")

    with tab2:
        email = st.text_input("New Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            try:
                auth.create_user(email=email, password=password)
                db.collection("users").document(email).set({
                    "paid": False,
                    "created": datetime.utcnow()
                })
                st.success("Account Created")
            except:
                st.error("Error creating account")

# ================= AI ASSISTANT =================
def ai_section():
    st.subheader("🤖 AI Assistant")

    uploaded_file = st.file_uploader("Upload CSV/TXT", type=["csv", "txt"])
    file_content = ""

    if uploaded_file:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            file_content = df.to_string()
        else:
            file_content = uploaded_file.read().decode("utf-8")
            st.text(file_content[:300])

    user_input = st.text_input("Ask AI")

    if st.button("Ask AI"):
        if user_input:
            prompt = f"{user_input}\n\nData:\n{file_content}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content
            st.success(answer)

# ================= DASHBOARD =================
def dashboard():
    st.title("📊 BTC Phoenix")

    user_doc = db.collection("users").document(st.session_state.user).get()
    paid = user_doc.to_dict().get("paid", False)

    df = get_btc_data()

    st.metric("BTC Price", f"${df['price'].iloc[-1]:,.2f}")

    chart = alt.Chart(df).mark_line().encode(
        x="time:T",
        y="price:Q"
    )
    st.altair_chart(chart, use_container_width=True)

    st.divider()

    if not paid:
        st.warning("Premium Locked")
        st.link_button("Unlock ₹199", RAZORPAY_LINK)
    else:
        st.success("Premium Active")
        signal = "UP 📈" if df["price"].iloc[-1] > df["price"].iloc[0] else "DOWN 📉"
        st.metric("Signal", signal)

        # 🔥 AI SECTION INSIDE PREMIUM
        ai_section()

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ================= MAIN =================
if st.session_state.user:
    dashboard()
else:
    auth_page()
