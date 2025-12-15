import streamlit as st
import numpy as np

# Page config
st.set_page_config(
    page_title="BTC Price Predictor",
    page_icon="₿",
    layout="centered"
)

# =========================
# BRAND LOGO
# =========================
st.image("assets/logo.png", width=180)

# =========================
# TITLE
# =========================
st.title("₿ BTC Price Predictor (Stable Demo)")
st.caption("Manual input → Prediction (Cloud-safe version)")

st.divider()

# =========================
# INPUT DATA
# =========================
st.subheader("Input Data")

values = []
for i in range(4):
    val = st.number_input(
        f"Value {i+1}",
        value=50000 + i * 1000,
        step=100
    )
    values.append(val)

# =========================
# PREDICTION BUTTON
# =========================
if st.button("Predict BTC Price"):
    data = np.array(values)
    prediction = round(data.mean(), 2)

    st.success(f"📈 Predicted BTC Price: ${prediction}")
    st.info("⚠️ Demo prediction (no live market / ML model yet)")
    
