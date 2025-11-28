import streamlit as st
import time
from utils_api import fetch_btc_price
from utils_charts import plot_price_chart

st.set_page_config(page_title="RQC BTC Predictor", layout="wide")

st.title("🔮 RQC Real-Time BTC/USDT Price Predictor")

placeholder = st.empty()
prices = []

st.info("Fetching real-time BTC price from Binance...")

while True:
    price = fetch_btc_price()

    if price:
        prices.append(price)

        with placeholder.container():
            st.subheader(f"💰 Live BTC Price: **${price:,.2f}**")
            chart = plot_price_chart(prices)
            st.plotly_chart(chart, use_container_width=True)
    else:
        st.error("Failed to fetch price. Trying again...")

    time.sleep(3)  # हर 3 सेकंड मे अपडेट
    

