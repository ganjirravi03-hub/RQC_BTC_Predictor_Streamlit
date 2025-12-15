import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", layout="centered")
st.title("🔥 BTC Phoenix – Live Buy / Sell / Hold")
st.caption("Stable BTC Signal Engine (v1.0 FINAL)")

# ---------------- DATA FETCH ----------------
@st.cache_data(ttl=60)
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minute"
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if isinstance(data, dict) and "prices" in data:
        df = pd.DataFrame(data["prices"], columns=["time", "price"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        return df, "LIVE"

    raise Exception("API_FAIL")

# ---------------- FALLBACK ----------------
def demo_data():
    prices = np.linspace(43000, 43250, 60)
    time = pd.date_range(end=datetime.now(), periods=60, freq="min")
    df = pd.DataFrame({"time": time, "price": prices})
    return df, "DEMO"

# ---------------- SIGNAL ENGINE ----------------
def signal_engine(df):
    df["ma_fast"] = df["price"].rolling(5).mean()
    df["ma_slow"] = df["price"].rolling(20).mean()

    if df["ma_fast"].iloc[-1] > df["ma_slow"].iloc[-1]:
        return "🟢 BUY", "Uptrend"
    elif df["ma_fast"].iloc[-1] < df["ma_slow"].iloc[-1]:
        return "🔴 SELL", "Downtrend"
    else:
        return "🟡 HOLD", "Sideways"

# ---------------- MAIN ----------------
try:
    df, source = get_btc_data()
except:
    df, source = demo_data()

price = df["price"].iloc[-1]
signal, reason = signal_engine(df)

st.metric("💰 BTC Price (USD)", f"${price:,.2f}")
st.success(f"📢 SIGNAL: {signal}")
st.info(f"Reason: {reason}")
st.caption(f"Data Source: {source}")

with st.expander("📊 Last 10 Data Points"):
    st.dataframe(df.tail(10))
    
