import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_model(mode):
    path = os.path.join(BASE_DIR, mode, "model_bundle.pkl")
    return joblib.load(path)


def get_value(data, key, default=None, cast=float):
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
    mode: "basic", "extended", or "advanced"
    """

    # -----------------------------
    # Load model bundle
    # -----------------------------
    try:
        bundle = load_model(mode)
    except Exception as e:
        return {"error": f"Model loading failed: {str(e)}"}

    model = bundle["model"]       # This is now the pipeline
    feature_order = bundle["features"]

    # -----------------------------
    # Build input row (DataFrame)
    # -----------------------------
    try:
        row = {
            feature: get_value(input_data, feature)
            for feature in feature_order
        }

        input_df = pd.DataFrame([row])

    except Exception as e:
        return {"error": f"Invalid input values: {str(e)}"}

    # -----------------------------
    # Predict
    # -----------------------------
    try:
        probability = model.predict_proba(input_df)[0][1]
        prediction = model.predict(input_df)[0]

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

    return {
        "prediction": int(prediction),
        "risk_probability": float(probability),
    }