import streamlit as st
import numpy as np
import pandas as pd
import requests
import plotly.graph_objects as go
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="BTC Price Predictor",
    page_icon="₿",
    layout="wide"
)

# =========================
# PREMIUM HEADER (LOGO + TITLE)
# =========================
col1, col2 = st.columns([1, 4])

with col1:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.warning("Logo missing")

with col2:
    st.markdown(
        """
        <h1 style='margin-bottom:0'>BTC Price Predictor</h1>
        <p style='color:gray;margin-top:5px'>
        Live Market View • Smart Prediction • Brand Demo
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# =========================
# LIVE BTC PRICE
# =========================
st.subheader("📡 Live BTC Price")

def get_live_btc():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url, timeout=10)
    return r.json()["bitcoin"]["usd"]

try:
    live_price = get_live_btc()
    st.metric("BTC / USD", f"${live_price:,}")
except:
    st.error("Live price fetch failed")

st.divider()

# =========================
# INPUT SECTION
# =========================
st.subheader("🧠 Manual Input (Demo Prediction)")

values = []
cols = st.columns(4)
default_vals = [50000, 51000, 49500, 50500]

for i in range(4):
    with cols[i]:
        val = st.number_input(
            f"Value {i+1}",
            value=default_vals[i],
            step=100
        )
        values.append(val)

# =========================
# PREDICTION + CHART
# =========================
if st.button("🚀 Predict BTC Price"):
    arr = np.array(values)
    prediction = round(arr.mean(), 2)

    st.success(f"📈 Predicted BTC Price: ${prediction:,}")

    # Chart
    df = pd.DataFrame({
        "Input Values": arr,
        "Index": [1, 2, 3, 4]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Index"],
        y=df["Input Values"],
        mode="lines+markers",
        name="Input Prices"
    ))

    fig.add_hline(
        y=prediction,
        line_dash="dash",
        annotation_text="Prediction"
    )

    fig.update_layout(
        title="BTC Input Trend vs Prediction",
        xaxis_title="Sequence",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("⚠️ Demo logic (Live ML model coming next)")

st.divider()

# =========================
# FOOTER / MONETIZATION TEASER
# =========================
st.markdown(
    """
    ### 💎 Coming Soon
    - 🤖 AI LSTM Prediction
    - 📱 Android APK
    - 🔐 Premium Signals
    - 💰 Paid Membership Access
    """
)
