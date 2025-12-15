# ===============================
# BTC Predictor Streamlit App
# ===============================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objs as go

st.set_page_config(page_title="BTC Predictor", layout="wide")

st.title("💰 BTC Price Predictor")
st.write("Live BTC price data and prediction app powered by AI/ML")

# -------------------------------
# Load your trained model
# -------------------------------
try:
    model = joblib.load("model.pkl")  # Upload your trained model in workspace
    st.success("✅ Model loaded successfully")
except:
    st.warning("⚠️ Model not found. Upload 'model.pkl' in your workspace")

# -------------------------------
# Optionally use API keys (Secrets)
# -------------------------------
# Uncomment if you want to use Binance API
# api_key = st.secrets["BINANCE_API_KEY"]
# api_secret = st.secrets["BINANCE_API_SECRET"]

# -------------------------------
# Fetch BTC data
# -------------------------------
st.subheader("📈 Live BTC Data")
btc_data = yf.download(
    tickers="BTC-USD",
    period="30d",
    interval="1h",
    auto_adjust=True,    # last 30 days data only
    progress=False
)
btc_data.reset_index(inplace=True)
st.dataframe(btc_data.tail(5))  # Show last 5 rows

# -------------------------------
# Prediction
# -------------------------------
st.subheader("🤖 Predict BTC Price")

# Prepare input features (simple example: using previous closing price)
if 'Close' in btc_data.columns:
    latest_close = btc_data['Close'].values[-1].reshape(1, -1)  # shape for model
    if 'model' in locals():
        predicted_price = model.predict(latest_close)[0]
        st.metric("Predicted BTC Price (next interval)", f"${predicted_price:,.2f}")
    else:
        st.info("Upload a trained model to get predictions")

# -------------------------------
# Plot BTC chart
# -------------------------------
st.subheader("📊 BTC Price Chart")
fig = go.Figure()
fig.add_trace(go.Scatter(x=btc_data['Datetime'], y=btc_data['Close'], mode='lines', name='BTC Close'))
fig.update_layout(title="BTC Price Last 30 Days", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, width='stretch')  # future proof

# -------------------------------
# Footer
# -------------------------------
st.write("🔹 Made with ❤️ by Ravi Ganjir")
