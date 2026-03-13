import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_models(mode):
    path = os.path.join(BASE_DIR, mode, "model_bundle.pkl")
    return joblib.load(path)


def get_value(data, key, default=0, cast=float):
    """Safely extract numeric value from input dictionary"""
    value = data.get(key)

    if value is None or value == "":
        return default

    try:
        return cast(value)
    except:
        return default


def predict_risk(input_data, mode):
    """
    input_data: dict of feature name -> value
    mode: "bare", "basic", or "advanced"
    """

    try:
        bundle = load_models(mode)
    except Exception as e:
        return {"error": f"Model loading failed: {str(e)}"}

    feature_order = bundle["feature_order"]
    model = bundle["model"]
    scaler = bundle["scaler"]

    # Convert input values according to trained feature order
    try:
        ordered_values = [
            get_value(input_data, feature)
            for feature in feature_order
        ]
    except Exception as e:
        return {"error": f"Invalid input values: {str(e)}"}

    try:
        input_array = np.array(ordered_values).reshape(1, -1)

        if scaler is not None:
            input_array = scaler.transform(input_array)

        probability = model.predict_proba(input_array)[0][1]
        prediction = model.predict(input_array)[0]

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

    return {
        "prediction": int(prediction),
        "risk_probability": float(probability),
    }