# =========================================================
# RQC – AIMO LIVE PREDICTOR (FINAL PRODUCTION VERSION)
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="RQC AIMO Predictor",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 RQC – AI Mathematical Olympiad Predictor")
st.write("TF-IDF + Linear Regression (Kaggle Inspired Model)")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_reference_data():
    try:
        df = pd.read_csv("reference.csv")
        return df
    except Exception as e:
        st.error("❌ reference.csv not found. Upload it to GitHub.")
        st.stop()

reference = load_reference_data()

# ---------------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------------
@st.cache_resource
def train_model(df):
    X = df["problem"].astype(str)
    y = df["answer"]

    vectorizer = TfidfVectorizer(stop_words="english")
    X_vec = vectorizer.fit_transform(X)

    model = LinearRegression()
    model.fit(X_vec, y)

    return vectorizer, model

vectorizer, model = train_model(reference)

st.success("✅ Model trained successfully")

# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------
st.subheader("✍️ Enter a Math Problem")
user_problem = st.text_area(
    "Example: Solve 4 + x = 4 for x",
    height=100
)

# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------
if st.button("🔮 Predict Answer"):
    if user_problem.strip() == "":
        st.warning("⚠️ Please enter a problem first.")
    else:
        input_vec = vectorizer.transform([user_problem])
        prediction = model.predict(input_vec)[0]

        st.success(f"📌 Predicted Answer: **{int(round(prediction))}**")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.caption("Built by RQC | Kaggle ➜ GitHub ➜ Live App 🚀")
    
