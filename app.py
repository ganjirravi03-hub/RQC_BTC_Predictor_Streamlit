import streamlit as st
import yfinance as yf
import pandas as pd
import pickle
import plotly.graph_objects as go

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="BTC Price Predictor", layout="centered")

st.title("💰 BTC Price Predictor")
st.caption("Live BTC price data and prediction app powered by AI/ML")

# -------------------------------
# TIMEFRAME SELECT
# -------------------------------
st.subheader("⏱ Select Timeframe")

timeframe_map = {
    "1 Hour": "1h",
    "4 Hours": "4h",
    "1 Day": "1d"
}

selected_timeframe = st.selectbox(
    "Choose timeframe",
    list(timeframe_map.keys())
)

interval = timeframe_map[selected_timeframe]

# -------------------------------
# FETCH BTC DATA
# -------------------------------
@st.cache_data
def load_btc_data(interval):
    df = yf.download(
        "BTC-USD",
        period="7d",
        interval=interval
    )
    df.reset_index(inplace=True)
    return df

df = load_btc_data(interval)

# -------------------------------
# SHOW LIVE DATA
# -------------------------------
st.subheader("📊 Live BTC Data")
st.dataframe(df.tail(10), use_container_width=True)

# -------------------------------
# MODEL UPLOAD
# -------------------------------
st.subheader("🤖 Predict BTC Price")

uploaded_model = st.file_uploader(
    "Upload your trained model (model.pkl)",
    type=["pkl"]
)

prediction = None

if uploaded_model:
    model = pickle.load(uploaded_model)

    last_close = df["Close"].iloc[-1]
    prediction = model.predict([[last_close]])[0]

    st.success(f"📈 Predicted Next Price: **${prediction:,.2f}**")

else:
    st.info("⬆ Upload model.pkl to activate prediction")

# -------------------------------
# PRICE CHART
# -------------------------------
st.subheader("📉 BTC Price Chart")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Datetime"] if "Datetime" in df.columns else df["Date"],
    y=df["Close"],
    mode="lines",
    name="BTC Price"
))

if prediction:
    fig.add_trace(go.Scatter(
        x=[df.iloc[-1, 0]],
        y=[prediction],
        mode="markers",
        marker=dict(size=10),
        name="Prediction"
    ))

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("🔹 Made with ❤️ by **Ravi Ganjir**")

