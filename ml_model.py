import pickle
import numpy as np

# Load ML model
model_path = "models/btc_predictor.pkl"  # aapka model file path
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Prediction function
def predict_btc(input_data):
    data_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(data_array)
    return float(prediction[0])
  
