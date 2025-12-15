import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BTC Phoenix", layout="centered")

# ---------------- TITLE ----------------
st.title("🔥 BTC Phoenix – Live Buy / Sell / Hold")
st.caption("Stable BTC Signal Engine (FINAL v1.1)")

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
last_update = datetime.now().strftime("%d %b %Y | %H:%M:%S")

# ---------------- UI BADGE ----------------
if source == "LIVE":
    st.success("🟢 LIVE DATA")
else:
    st.warning("🟡 DEMO DATA (API TEMP ISSUE)")

# ---------------- BIG SIGNAL BANNER ----------------
st.markdown(
    f"""
    <div style="padding:20px;border-radius:15px;
    background-color:#0f172a;color:white;text-align:center;
    font-size:28px;font-weight:bold;">
    {signal}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.metric("💰 BTC Price (USD)", f"${price:,.2f}")
st.caption(f"📌 Reason: {reason}")
st.caption(f"⏱ Last Update: {last_update}")

# ---------------- PRICE CHART ----------------
st.subheader("📈 BTC Price (Last 60 Minutes)")
st.line_chart(df.set_index("time")["price"])

# ---------------- DATA TABLE ----------------
with st.expander("📊 Last 10 Data Points"):
    st.dataframe(df.tail(10))
    
