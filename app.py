import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="BTC Price Predictor",
    page_icon="💰",
    layout="centered"
)

st.title("💰 BTC Price Predictor")
st.caption("Live BTC price data and prediction app powered by AI/ML")

# ======================================
# TIMEFRAME SELECTOR
# ======================================
st.subheader("⏱ Select Timeframe")

timeframe_map = {
    "1 Hour": ("7d", "1h"),
    "4 Hours": ("30d", "4h"),
    "1 Day": ("6mo", "1d"),
}

selected_tf = st.selectbox(
    "Choose timeframe",
    list(timeframe_map.keys())
)

period, interval = timeframe_map[selected_tf]

# ======================================
# LOAD BTC DATA
# ======================================
@st.cache_data(ttl=300)
def load_btc_data(period, interval):
    data = yf.download(
        "BTC-USD",
        period=period,
        interval=interval,
        progress=False
    )
    data.reset_index(inplace=True)
    return data

df = load_btc_data(period, interval)

# ======================================
# LIVE DATA TABLE
# ======================================
st.subheader("📊 Live BTC Data")

if df.empty:
    st.error("BTC data not available right now.")
    st.stop()

st.dataframe(df.tail(5), use_container_width=True)

# ======================================
# MODEL UPLOAD
# ======================================
st.subheader("🤖 Predict BTC Price")

uploaded_model = st.file_uploader(
    "Upload your trained model (model.pkl)",
    type=["pkl"]
)

prediction = None
signal = None
color = "gray"

if uploaded_model:
    try:
        model = pickle.load(uploaded_model)

        last_close = float(df["Close"].iloc[-1])
        prediction = float(model.predict([[last_close]])[0])

        st.success(f"📈 Predicted Next Price: **${prediction:,.2f}**")

        # ======================================
        # BUY / SELL LOGIC
        # ======================================
        price_diff_percent = ((prediction - last_close) / last_close) * 100

        if price_diff_percent > 0.1:
            signal = "BUY 📈"
            color = "green"
        elif price_diff_percent < -0.1:
            signal = "SELL 📉"
            color = "red"
        else:
            signal = "HOLD ⏸"
            color = "orange"

        st.markdown(
            f"""
            <h2 style='color:{color}; text-align:center;'>
                {signal}
            </h2>
            <p style='text-align:center; font-size:16px;'>
                Difference: {price_diff_percent:.2f}%
            </p>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error("❌ Model error. Please upload a valid trained model.")

else:
    st.info("⬆ Upload model.pkl to activate prediction & signals")

# ======================================
# BTC PRICE CHART
# ======================================
st.subheader("📉 BTC Price Chart")

fig = go.Figure()

time_col = "Datetime" if "Datetime" in df.columns else "Date"

fig.add_trace(go.Scatter(
    x=df[time_col],
    y=df["Close"],
    mode="lines",
    name="BTC Close Price"
))

# Prediction point
if prediction is not None:
    fig.add_trace(go.Scatter(
        x=[df[time_col].iloc[-1]],
        y=[prediction],
        mode="markers+text",
        text=[signal],
        textposition="top center",
        marker=dict(size=10, color=color),
        name="Prediction"
    ))

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    height=450,
    template="plotly_white",
    margin=dict(l=20, r=20, t=40, b=80)
)

st.plotly_chart(fig, use_container_width=True)

# ======================================
# FOOTER
# ======================================
st.markdown("---")
st.caption("🔹 Made with ❤️ by Ravi Ganjir")


