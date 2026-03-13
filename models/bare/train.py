import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Bare minimum model
# Fields: age, sex, cp (chest pain type), exang (exercise-induced chest pain)
# All self-reported, no equipment needed

FEATURES = ["age", "sex", "cp", "exang"]

column_names = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak",
    "slope", "ca", "thal", "target"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(
    os.path.join(BASE_DIR, "..", "processed.cleveland.data"),
    sep=",",
    header=None,
    names=column_names,
    engine="python"
)

df.replace("?", np.nan, inplace=True)
df = df.apply(pd.to_numeric)

# Only drop rows missing our selected features or target
df = df.dropna(subset=FEATURES + ["target"])
df["target"] = df["target"].apply(lambda x: 1 if x > 0 else 0)

X = df[FEATURES]
y = df["target"]

print(f"Dataset size after filtering: {X.shape}")
print(f"Features: {FEATURES}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print("\nSample probability outputs:")
for i, prob in enumerate(y_proba[:5]):
    print(f"  Sample {i+1}: No Disease {prob[0]*100:.1f}% | Disease {prob[1]*100:.1f}%")

bundle = {
    "model":         model,
    "scaler":        scaler,
    "feature_order": FEATURES,
}

out_dir = os.path.join(BASE_DIR)
os.makedirs(out_dir, exist_ok=True)
joblib.dump(bundle, os.path.join(out_dir, "model_bundle.pkl"))
print(f"\nBare minimum model saved to {out_dir}/model_bundle.pkl")