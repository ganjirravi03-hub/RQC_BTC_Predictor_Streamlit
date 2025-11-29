# app.py
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils_api import fetch_btc_price
import random

# ---------------------------
# App UI Setup
# ---------------------------
st.set_page_config(page_title="RQC Superhero BTC Live App", layout="wide")

# ---------------------------
# CSS Superhero Styling (Step 3)
# ---------------------------
st.markdown("""
<style>

body {
    background-color: #0e0e0e;
}

/* HERO TITLE */
.title-hero {
    font-size: 45px;
    font-weight: 900;
    text-shadow: 0 0 25px #00eaff, 0 0 40px #00bcd4;
    color: #00eaff;
    text-align: center;
    padding: 20px 0;
}

/* LIVE PRICE CARD */
.live-card {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(0, 255, 255, 0.4);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 0 22px #00eaff88;
    backdrop-filter: blur(8px);
}

/* EARNINGS CARDS */
.earn-card {
    background: linear-gradient(135deg, #1d1d1d, #000000);
    border: 2px solid gold;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    color: gold;
    font-weight: 700;
    box-shadow: 0 0 15px gold;
}

/* BLINK DOT */
.blink {
    height: 12px;
    width: 12px;
    background-color: red;
    border-radius: 50%;
    display: inline-block;
    animation: blinkAnimation 1s infinite;
}

@keyframes blinkAnimation {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Hero Title (Step 4)
# ---------------------------
st.markdown('<div class="title-hero">🚀 RQC SUPERHERO BTC PREDICTOR</div>', unsafe_allow_html=True)

# ---------------------------
# Helper Functions
# ---------------------------
def plot_live_chart(prices):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=prices,
        mode='lines',
        line=dict(width=3),
        name="BTC Price"
    ))
    fig.update_layout(
        template="plotly_dark",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#00eaff"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig

def get_direction_arrow(prices):
    if len(prices) < 2:
        return "⏳"
    if prices[-1] > prices[-2]:
        return "🟢⬆ UP Trend"
    elif prices[-1] < prices[-2]:
        return "🔻🔴 DOWN Trend"
    else:
        return "⚪ Stable"

def ai_prediction_box(prediction_value):
    color = "#00eaff" if prediction_value >= 0 else "#ff4444"
    return f"""
    <div style="
        background: rgba(0, 0, 0, 0.45);
        border: 2px solid {color};
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 30px {color}99;
        text-align: center;
        margin-top: 25px;
    ">
        <h2 style="color:{color}; text-shadow:0 0 12px {color};">
            🔮 AI Prediction: {prediction_value:.2f}%
        </h2>
        <p style="color:white;">Next 10s trend probability</p>
    </div>
    """

def earning_calculator(prices, investment=10):
    if len(prices) < 2:
        return 0
    change = prices[-1] - prices[-2]
    profit = (change / prices[-2]) * investment * 5
    return profit

# ---------------------------
# Earning Panel (Step 5)
# ---------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#ffcc00; text-align:center;'>💸 RQC Earning Center</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="earn-card">Today Earnings</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="earn-card">Weekly Earnings</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="earn-card">Total Earnings</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------
# FINAL LIVE LOOP (Step 6)
# ---------------------------
placeholder = st.empty()
prices = []

while True:
    price = fetch_btc_price()

    if price:
        prices.append(price)

        with placeholder.container():

            # CHART CONTAINER STYLING (Step 8A)
            st.markdown("""
            <div style="
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid #00eaff66;
            padding: 10px 20px;
            border-radius: 15px;
            box-shadow: 0 0 25px #00eaff88;
            margin-top: 25px;">
            <h3 style="color:#00eaff; text-align:center; text-shadow:0 0 18px #00eaff;">
            📈 AI Price Prediction Chart
            </h3>
            </div>
            """, unsafe_allow_html=True)

            # LIVE PRICE CARD
            st.markdown('<div class="live-card">', unsafe_allow_html=True)
            st.markdown(
                f"<h2 style='color:#00eaff; text-shadow:0 0 18px #00eaff;'>💰 Live Price: ${price:,.2f} <span class='blink'></span></h2>",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # CHART
            fig = plot_live_chart(prices)
            st.plotly_chart(fig, use_container_width=True)

            # TREND ARROW
            arrow = get_direction_arrow(prices)
            st.markdown(
                f"<h3 style='color:gold; text-align:center; font-size:32px;'>{arrow}</h3>",
                unsafe_allow_html=True
            )

            # AI PREDICTION %
            pred = random.uniform(-1, 1) * 5
            st.markdown(ai_prediction_box(pred), unsafe_allow_html=True)

            # EARNING SYSTEM
            earning = earning_calculator(prices)
            st.markdown(f"""
            <div style="
                background:#00000055;
                border:1px solid #00ff88aa;
                padding:15px;
                border-radius:12px;
                margin-top:20px;
                text-align:center;
                box-shadow:0 0 20px #00ff8899;
            ">
                <h3 style="color:#00ff88;">💹 Estimated Earning: ${earning:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("Failed to fetch price. Retrying...")

    time.sleep(1)
    
