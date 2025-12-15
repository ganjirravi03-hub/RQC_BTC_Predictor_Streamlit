import streamlit as st
import numpy as np
import tensorflow as tf

# ===============================
# APP CONFIG
# ===============================
st.set_page_config(
    page_title="BTC Price Predictor",
    page_icon="₿",
    layout="centered"
)

st.title("₿ BTC Price Predictor")
st.write("Manual input → AI prediction (Stable version)")

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("BTC_HTM_model.h5")

try:
    model = load_model()
    st.success("✅ Model loaded successfully")
except Exception as e:
    st.error("❌ Model load failed")
    st.stop()

# ===============================
# USER INPUT
# ===============================
st.sidebar.header("Enter Market Data")

open_price = st.sidebar.number_input("Open Price", value=50000.0)
high_price = st.sidebar.number_input("High Price", value=51000.0)
low_price = st.sidebar.number_input("Low Price", value=49500.0)
volume = st.sidebar.number_input("Volume", value=1000.0)

# ===============================
# PREPARE INPUT
# ===============================
input_data = np.array([[open_price, high_price, low_price, volume]])
input_data = np.expand_dims(input_data, axis=0)  # (1, 1, 4)

st.subheader("Input Data")
st.write(input_data)

# ===============================
# PREDICTION
# ===============================
if st.button("Predict BTC Price"):
    prediction = model.predict(input_data)
    st.subheader("📈 Predicted BTC Price")
    st.success(f"${prediction[0][0]:,.2f}")
    
