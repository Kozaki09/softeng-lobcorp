import joblib
import numpy as np

model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_heart_risk(input_data):
    """
    input_data: list of 13 values in correct order
    """

    input_array = np.array(input_data).reshape(1, -1)
    input_scaled = scaler.transform(input_array)

    probability = model.predict_proba(input_scaled)[0][1]
    prediction = model.predict(input_scaled)[0]

    return {
        "prediciton": int(prediction),
        "risk_probability": float(probability)  
    }