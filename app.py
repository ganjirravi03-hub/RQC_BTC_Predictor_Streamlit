import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# --- Configuration ---
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
LIMIT = 120
REFRESH_SECONDS = 10
BASE_URL = "https://fapi.binance.com/fapi/v1/klines"

# --- Fetch Data from Binance ---
def get_binance_klines():
    params = {'symbol': SYMBOL, 'interval': INTERVAL, 'limit': LIMIT}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            st.error("Binance API returned empty data.")
            return None

        df = pd.DataFrame(data, columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close time', 'Quote asset volume', 'Number of trades',
            'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
        ])

        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

        return df

    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# --- Simple ML Prediction (No Training) ---
def predict_signal(df):
    close_prices = df["Close"]

    last_close = close_prices.iloc[-1]
    avg_change = close_prices.diff().tail(10).mean()

    if avg_change > 0.05:
        return "BUY (Strong Signal)", last_close
    elif avg_change < -0.05:
        return "SELL (Strong Signal)", last_close
    else:
        return "H HOLD (Neutral)", last_close

# --- Streamlit App ---
def run_app():
    st.title("⚡ RQC BTC Predictor LIVE")
    st.subheader(f"Real-time {SYMBOL} Price & Prediction")

    df = get_binance_klines()

    if df is not None:
        latest_close = df["Close"].iloc[-1]

        prediction, last_close = predict_signal(df)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Current Price (USDT)",
                f"{latest_close:.2f}",
                f"{df['Close'].diff().iloc[-1]:.2f}"
            )

        with col2:
            st.metric(
                "Next 1 Min Prediction",
                prediction,
                "Based on last 120 mins"
            )

        fig = go.Figure(data=[go.Candlestick(
            x=df["Close time"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])

        fig.update_layout(
            title=f"{SYMBOL} Candlestick Chart (1m)",
            xaxis_title="Time",
            yaxis_title="Price (USDT)",
            xaxis_rangeslider_visible=False,
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Unable to fetch data from Binance.")

    st.info(f"Auto-refresh every {REFRESH_SECONDS} seconds…")

    time.sleep(REFRESH_SECONDS)
    st.rerun()

if __name__ == "__main__":
    run_app()

