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
# serviceAccountKey.json same folder me hona chahiye
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= BTC DATA (CoinGecko) =================
@st.cache_data(ttl=60)
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": 1}
    r = requests.get(url, params=params, timeout=10)
    data = r.json().get("prices", [])

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# ================= AUTH PAGE =================
def auth_page():
    st.title("🔐 BTC Phoenix Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------- LOGIN ----------
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

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
        r_email = st.text_input("New Email")
        r_pass = st.text_input("New Password", type="password")

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
        st.error("⚠️ BTC data unavailable")
        return

    st.metric("💰 BTC Price (USD)", f"${df['price'].iloc[-1]:,.2f}")

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
        st.caption("Payment ke baad auto-unlock (Webhook Ready)")
    else:
        st.success("✅ Premium Active")
        signal = "📈 UP ⬆️" if df["price"].iloc[-1] > df["price"].iloc[0] else "📉 DOWN ⬇️"
        st.metric("Market Signal", signal)
        st.caption("AI / ML Engine v2 coming soon")

    st.divider()
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ================= MAIN =================
if st.session_state.user is None:
    auth_page()
else:
    dashboard()
        
import streamlit as st
import pandas as pd
import openai

# 🔑 API Key (yaha apni key daal)
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI Assistant", layout="centered")

st.title("🤖 AI Smart Assistant")
st.write("Chat + File Analysis System 🚀")

# =========================
# 📂 FILE UPLOAD SECTION
# =========================
uploaded_file = st.file_uploader("Upload your file (CSV or TXT)", type=["csv", "txt"])

file_content = ""

if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.write("📊 CSV Preview:")
        st.dataframe(df.head())
        file_content = df.to_string()
    else:
        file_content = uploaded_file.read().decode("utf-8")
        st.write("📄 File Content Preview:")
        st.text(file_content[:500])

# =========================
# 💬 CHAT SECTION
# =========================
user_input = st.text_input("Ask something...")

if st.button("Submit"):
    if user_input:

        prompt = f"""
        User Question: {user_input}
        
        File Data:
        {file_content}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            answer = response['choices'][0]['message']['content']

            st.success("✅ Response:")
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# 🧠 FOOTER
# =========================
st.markdown("---")
st.caption("Made with ❤️ by Ravi AI System")
