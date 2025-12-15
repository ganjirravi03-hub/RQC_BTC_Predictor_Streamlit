import streamlit as st
import numpy as np

st.set_page_config(
    page_title="BTC Predictor",
    page_icon="₿",
    layout="centered"
)

st.title("₿ BTC Price Predictor (Stable Demo)")
st.write("Manual input → Prediction (Cloud-safe version)")

st.sidebar.header("Market Inputs")

open_price = st.sidebar.number_input("Open Price", value=50000.0)
high_price = st.sidebar.number_input("High Price", value=51000.0)
low_price = st.sidebar.number_input("Low Price", value=49500.0)
volume = st.sidebar.number_input("Volume", value=1000.0)

input_data = np.array([open_price, high_price, low_price, volume])

st.subheader("Input Data")
st.write(input_data)

if st.button("Predict BTC Price"):
    # Dummy prediction logic (safe for cloud)
    predicted_price = (open_price + high_price + low_price) / 3
    st.success(f"📈 Predicted BTC Price: ${predicted_price:,.2f}")
    
