import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# =========================
# APP CONFIG
# =========================
st.set_page_config(
    page_title="BTC Price Predictor",
    page_icon="💰",
    layout="centered"
)

st.title("💰 BTC Price Predictor")
st.caption("Live BTC price data with timeframe & BUY / SELL signals")

# =========================
# TIMEFRAME SELECTOR
# =========================
st.subheader("⏱️ Select Timeframe")

timeframe_map = {
    "1 Hour": ("30d", "1h"),
    "4 Hour": ("60d", "4h"),
    "1 Day": ("1y", "1d"),
    "1 Week": ("5y", "1wk"),
}

selected_tf = st.selectbox("Choose timeframe", list(timeframe_map.keys()))
period, interval = timeframe_map[selected_tf]

# =========================
# FETCH BTC DATA
# =========================
@st.cache_data(ttl=300)
def load_data(period, interval):
    data = yf.download(
        tickers="BTC-USD",
        period=period,
        interval=interval
    )
    data.dropna(inplace=True)
    return data

data = load_data(period, interval)

if data.empty:
    st.error("⚠️ No data received. Try another timeframe.")
    st.stop()

# =========================
# LIVE DATA TABLE
# =========================
st.subheader("📈 Live BTC Data")
st.dataframe(data.tail(10), width="stretch")

# =========================
# BUY / SELL SIGNAL LOGIC
# =========================
st.subheader("🚦 Trading Signal")

data["MA_5"] = data["Close"].rolling(5).mean()
data["MA_20"] = data["Close"].rolling(20).mean()

latest_price = data["Close"].iloc[-1]
ma5 = data["MA_5"].iloc[-1]
ma20 = data["MA_20"].iloc[-1]

if ma5 > ma20:
    signal = "BUY 🚀"
    color = "green"
elif ma5 < ma20:
    signal = "SELL 🔻"
    color = "red"
else:
    signal = "HOLD ⚖️"
    color = "orange"

st.markdown(
    f"""
    <h2 style='color:{color}; text-align:center'>
        {signal}
    </h2>
    <p style='text-align:center'>
        Latest Price: <b>${latest_price:,.2f}</b>
    </p>
    """,
    unsafe_allow_html=True
)

# =========================
# PRICE CHART
# =========================
st.subheader("📊 BTC Price Chart")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["Close"],
    name="BTC Price",
    line=dict(width=2)
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA_5"],
    name="MA 5",
    line=dict(dash="dot")
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA_20"],
    name="MA 20",
    line=dict(dash="dash")
))

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, width="stretch")

# =========================
# FOOTER
# =========================
st.markdown(
    "<hr><center>🔹 Made with ❤️ by <b>Ravi Ganjir</b></center>",
    unsafe_allow_html=True
)
