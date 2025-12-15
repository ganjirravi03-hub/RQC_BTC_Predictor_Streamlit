import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="BTC Price Predictor",
    page_icon="💰",
    layout="wide"
)

st.title("💰 BTC Price Predictor")
st.caption("Live BTC price data and prediction app powered by AI/ML")

# =========================
# TIMEFRAME SELECTOR
# =========================
st.subheader("⏱️ Select Timeframe")

timeframe_map = {
    "1 Hour": ("7d", "1h"),
    "4 Hour": ("30d", "4h"),
    "1 Day": ("6mo", "1d"),
    "1 Week": ("2y", "1wk"),
}

selected_tf = st.selectbox(
    "Choose timeframe",
    list(timeframe_map.keys())
)

period, interval = timeframe_map[selected_tf]

# =========================
# FETCH BTC DATA
# =========================
@st.cache_data(ttl=300)
def load_btc_data(period, interval):
    data = yf.download(
        tickers="BTC-USD",
        period=period,
        interval=interval,
        progress=False
    )
    return data

btc_data = load_btc_data(period, interval)

# =========================
# SHOW LIVE DATA
# =========================
st.subheader("📈 Live BTC Data")

if btc_data.empty:
    st.error("BTC data not available right now.")
    st.stop()

st.dataframe(btc_data.tail(5), width="stretch")

# =========================
# LOAD MODEL (UPLOAD)
# =========================
st.subheader("🤖 Predict BTC Price")

uploaded_model = st.file_uploader(
    "Upload your trained model (model.pkl)",
    type=["pkl"]
)

model = None
if uploaded_model is not None:
    model = joblib.load(uploaded_model)
    st.success("✅ Model loaded successfully")

# =========================
# PREDICTION
# =========================
if model is not None and "Close" in btc_data.columns and len(btc_data) > 0:
    latest_close = np.array([[btc_data["Close"].iloc[-1]]])

    try:
        prediction = model.predict(latest_close)[0]
        st.metric(
            "Predicted BTC Price (Next Interval)",
            f"${prediction:,.2f}"
        )
    except Exception as e:
        st.error("Prediction error. Check model input shape.")
else:
    st.info("⬆️ Upload model.pkl to activate prediction")

# =========================
# BTC PRICE CHART
# =========================
st.subheader("📊 BTC Price Chart")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=btc_data.index,
        y=btc_data["Close"],
        mode="lines",
        name="BTC Close Price"
    )
)

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, width="stretch")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🔹 Made with ❤️ by Ravi Ganjir")
