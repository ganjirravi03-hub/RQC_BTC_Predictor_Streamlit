import streamlit as st
import time
import pandas as pd
import plotly.express as px
from utils_api import fetch_btc_price

# -----------------------------------------------------
# 🔥 SUPERHERO UI THEME CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="RQC BTC Predictor",
    layout="wide",
)

st.markdown("""
    <style>
        body {
            background-color: #0d0d0d !important;
        }
        .css-18e3th9 {
            background: #0d0d0d !important;
        }
        .css-1d391kg {
            background: #0d0d0d !important;
        }
        .super-title {
            font-size: 48px;
            color: #00eaff;
            text-shadow: 0px 0px 20px #00eaff;
            font-weight: 900;
            text-align: center;
        }
        .price-box {
            padding: 20px;
            border-radius: 15px;
            background: linear-gradient(120deg, #001f33, #000000);
            color: #00eaff;
            font-size: 30px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0px 0px 25px #00eaff;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# 🔥 SUPERHERO TITLE
# -----------------------------------------------------
st.markdown("<div class='super-title'>🦸‍♂️ RQC REAL-TIME BTC/USDT SUPER PREDICTOR</div>", unsafe_allow_html=True)

placeholder = st.empty()
prices = []

st.info("🚀 Fetching real-time BTC price from Binance...")

# -----------------------------------------------------
# 🔥 PLOTLY SUPERHERO CHART
# -----------------------------------------------------
def plot_price_chart_px(prices_list):
    df = pd.DataFrame({
        "Price": prices_list,
        "Time": range(1, len(prices_list)+1)
    })

    fig = px.line(
        df,
        x="Time",
        y="Price",
        title="🦸‍♂️ LIVE BTC/USDT PRICE CHART (Superhero Mode)",
        markers=True
    )

    fig.update_layout(
        title_font_size=26,
        title_font_color="#00eaff",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font_color="#00eaff",
        xaxis_title="Updates",
        yaxis_title="BTC Price (USD)",
        showlegend=False
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=6))
    return fig


# -----------------------------------------------------
# 🔥 REAL-TIME LOOP
# -----------------------------------------------------
while True:
    price = fetch_btc_price()

    if price:
        prices.append(price)

        with placeholder.container():
            st.markdown(f"<div class='price-box'>💰 LIVE PRICE: ${price:,.2f}</div>", unsafe_allow_html=True)
            chart = plot_price_chart_px(prices)
            st.plotly_chart(chart, use_container_width=True)

    else:
        st.error("❌ Failed to fetch price. Retrying...")

    time.sleep(3)
    
