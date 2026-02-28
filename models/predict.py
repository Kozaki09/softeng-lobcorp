from flask import jsonify
import joblib
import numpy as np

def load_models(mode):
    bundle = joblib.load(f"{mode}/model_bundle.pkl")
    return bundle

def predict_risk(input_data, mode):
    """
    input_data: dictionary of 13 values corresponding to the features
    """

    # Load appropriate model bundle
    bundle = load_models(mode)
    feature_order = bundle["feature_order"]
    model = bundle["model"]
    scaler = bundle["scaler"]

    # Check for missing fields
    missing = [f for f in feature_order if not input_data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Ensure correct ordering and numeric casting
    try:
        ordered_values = [float(input_data[f]) for f in feature_order]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e}")

    input_array = np.array(ordered_values).reshape(1, -1)
    input_scaled = scaler.transform(input_array)

    probability = model.predict_proba(input_scaled)[0][1]
    prediction = model.predict(input_scaled)[0]

    return {
        "prediction": int(prediction),
        "risk_probability": float(probability)
    }