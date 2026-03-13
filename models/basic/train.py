import pandas as pd
import numpy as np
import joblib
import os
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline

# Basic model
# Required fields:  age, sex, cp, exang, trestbps, thalach
# Optional fields:  fbs (fasting blood sugar)
# Missing optionals are imputed — model can predict without them

REQUIRED_FEATURES = ["age", "sex", "cp", "exang", "trestbps", "thalach"]
OPTIONAL_FEATURES = ["fbs"]
ALL_FEATURES      = REQUIRED_FEATURES + OPTIONAL_FEATURES

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

# Only drop rows missing required features or target — optionals can be NaN
df = df.dropna(subset=REQUIRED_FEATURES + ["target"])
df["target"] = df["target"].apply(lambda x: 1 if x > 0 else 0)

X = df[ALL_FEATURES].copy()
y = df["target"]

print(f"Dataset size after filtering: {X.shape}")
print(f"Required features:  {REQUIRED_FEATURES}")
print(f"Optional features:  {OPTIONAL_FEATURES}")
print(f"Missing value counts:\n{X.isnull().sum()}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# IterativeImputer fills missing optional values using patterns from other features
imputer = IterativeImputer(random_state=42, max_iter=10)
scaler  = StandardScaler()

X_train_imp    = imputer.fit_transform(X_train)
X_train_scaled = scaler.fit_transform(X_train_imp)

X_test_imp    = imputer.transform(X_test)
X_test_scaled = scaler.transform(X_test_imp)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred  = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print("\nSample probability outputs:")
for i, prob in enumerate(y_proba[:5]):
    print(f"  Sample {i+1}: No Disease {prob[0]*100:.1f}% | Disease {prob[1]*100:.1f}%")

bundle = {
    "model":            model,
    "scaler":           scaler,
    "imputer":          imputer,        # saved so predict.py can impute at inference time
    "feature_order":    ALL_FEATURES,
    "required":         REQUIRED_FEATURES,
    "optional":         OPTIONAL_FEATURES,
}

out_dir = os.path.join(BASE_DIR)
os.makedirs(out_dir, exist_ok=True)
joblib.dump(bundle, os.path.join(out_dir, "model_bundle.pkl"))
print(f"\nBasic model saved to {out_dir}/model_bundle.pkl")