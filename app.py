import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="BTC Phoenix Predictor", layout="centered")

st.title("🔥 BTC Phoenix – Live Buy / Sell / Hold")
st.write("Real-time BTC signal engine (Stable & Fast)")

# -----------------------------
# SAFE DATA FETCH
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
    data = r.json()

    # ✅ SAFETY CHECK
    if "prices" not in data:
        raise ValueError("API limit or temporary issue")

    df = pd.DataFrame(data["prices"], columns=["time", "price"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# -----------------------------
# FALLBACK DATA (ALWAYS WORKS)
# -----------------------------
def fallback_data():
    prices = np.linspace(43000, 43200, 60)
    time = pd.date_range(end=datetime.now(), periods=60, freq="min")
    return pd.DataFrame({"time": time, "price": prices})

# -----------------------------
# SIGNAL LOGIC
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
# MAIN APP
# -----------------------------
try:
    df = fetch_btc_data()
    data_source = "LIVE DATA"

except Exception:
    df = fallback_data()
    data_source = "DEMO DATA (API TEMP ISSUE)"

last_price = df["price"].iloc[-1]
signal, reason = generate_signal(df)

st.metric("💰 BTC Price (USD)", f"${last_price:,.2f}")
st.success(f"📢 SIGNAL: {signal}")
st.caption(reason)
st.info(f"Data Source: {data_source}")

with st.expander("📊 Last 10 Prices"):
    st.dataframe(df.tail(10))
    
