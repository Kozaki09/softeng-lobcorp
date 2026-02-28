import joblib
import numpy as np

bundle = joblib.load("models/full/model_bundle.pkl")
model = bundle["model"]
scaler = bundle["scaler"]
feature_order = bundle["feature_order"]

# [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

form = {
        "age": "63",
        "sex": "1",
        "cp": "4",
        "trestbps": "160",
        "chol": "280",
        "fbs": "1",
        "restecg": "2",
        "thalach": "110",
        "exang": "1",
        "oldpeak": "3.0",
        "slope": "2",
        "ca": "3",
        "thal": "7",
    }

# samples = [
#     # Likely no disease (healthy profile)
#     [45, 0, 2, 120, 210, 0, 0, 165, 0, 0.5, 1, 0, 3],
#     # Likely disease (high risk profile)
#     [63, 1, 4, 160, 280, 1, 2, 110, 1, 3.0, 2, 3, 7],
#     # Borderline
#     [55, 1, 3, 140, 250, 0, 0, 145, 0, 1.5, 2, 1, 3],
#     # Young, low risk
#     [35, 0, 1, 110, 190, 0, 0, 175, 0, 0.2, 1, 0, 3],
#     # Older, high risk
#     [70, 1, 4, 170, 310, 1, 2, 95, 1, 4.0, 2, 3, 7],
# ]



X = scaler.transform(samples)
probs = model.predict_proba(X)

print(f"{'Sample':<10} {'No Disease':>12} {'Disease':>12} {'Prediction':>12}")
print("-" * 48)
for i, prob in enumerate(probs):
    no_disease, disease = prob
    prediction = "Disease" if disease >= 0.5 else "No Disease"
    print(f"{i+1:<10} {no_disease*100:>11.1f}% {disease*100:>11.1f}% {prediction:>12}")

def explain(sample_scaled, feature_order, model):
    coefficients = model.coef_[0]
    contributions = sample_scaled * coefficients
    paired = sorted(zip(feature_order, contributions), key=lambda x: abs(x[1]), reverse=True)
    print("  Top contributing factors:")
    for feature, contrib in paired[:3]:
        direction = "↑ risk" if contrib > 0 else "↓ risk"
        print(f"    {feature:<12} {direction}  ({contrib:+.3f})")

print(f"{'Sample':<10} {'No Disease':>12} {'Disease':>12} {'Prediction':>12}")
print("-" * 48)
for i, (sample_scaled, prob) in enumerate(zip(X, probs)):
    no_disease, disease = prob
    prediction = "Disease" if disease >= 0.5 else "No Disease"
    print(f"{i+1:<10} {no_disease*100:>11.1f}% {disease*100:>11.1f}% {prediction:>12}")
    explain(sample_scaled, feature_order, model)
    print()