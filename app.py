import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="BTC Phoenix Predictor", layout="centered")

st.title("🔥 BTC Phoenix – Live Buy / Sell / Hold")
st.write("Real-time BTC signal engine (Stable & Fast)")

# -----------------------------
# DATA FETCH (CoinGecko – No API Key)
# -----------------------------
@st.cache_data(ttl=60)
def fetch_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minute"
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()["prices"]

    df = pd.DataFrame(data, columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# -----------------------------
# SIGNAL LOGIC (PROFIT FRIENDLY)
# -----------------------------
def generate_signal(df):
    short_ma = df["price"].rolling(5).mean()
    long_ma = df["price"].rolling(20).mean()

    if short_ma.iloc[-1] > long_ma.iloc[-1]:
        return "🟢 BUY", "Uptrend detected"
    elif short_ma.iloc[-1] < long_ma.iloc[-1]:
        return "🔴 SELL", "Downtrend detected"
    else:
        return "🟡 HOLD", "Sideways market"

# -----------------------------
# MAIN EXECUTION
# -----------------------------
try:
    df = fetch_btc_data()
    last_price = df["price"].iloc[-1]

    signal, reason = generate_signal(df)

    st.metric("💰 BTC Price (USD)", f"${last_price:,.2f}")
    st.success(f"📢 SIGNAL: {signal}")
    st.caption(reason)

    with st.expander("📊 Last 10 Prices"):
        st.dataframe(df.tail(10))

except Exception as e:
    st.error("Live data failed. Please refresh.")
    st.text(str(e))
    
