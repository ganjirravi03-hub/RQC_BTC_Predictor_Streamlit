import streamlit as st
import time
from utils_api import fetch_btc_price
import plotly.express as px  # ✅ Plotly Express import
from utils_charts import plot_price_chart  # अगर original में chart function अलग है तो नीचे fix किया गया

st.set_page_config(page_title="RQC BTC Predictor", layout="wide")

st.title("🔮 RQC Real-Time BTC/USDT Price Predictor")

placeholder = st.empty()
prices = []

st.info("Fetching real-time BTC price from Binance...")

# Helper function to create Plotly Express chart
def plot_price_chart_px(prices_list):
    import pandas as pd
    df = pd.DataFrame({"Price": prices_list, "Time": range(1, len(prices_list)+1)})
    fig = px.line(df, x="Time", y="Price", title="Live BTC Price", markers=True)
    fig.update_layout(yaxis_title="Price (USD)", xaxis_title="Updates")
    return fig

while True:
    price = fetch_btc_price()

    if price:
        prices.append(price)

        with placeholder.container():
            st.subheader(f"💰 Live BTC Price: **${price:,.2f}**")
            chart = plot_price_chart_px(prices)  # ✅ Updated chart function
            st.plotly_chart(chart, use_container_width=True)
    else:
        st.error("Failed to fetch price. Trying again...")

    time.sleep(3)  # हर 3 सेकंड में अपडेट
