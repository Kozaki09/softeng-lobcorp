import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
column_names = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak",
    "slope", "ca", "thal", "target"
]

df = pd.read_csv(
    "processed.cleveland.data",
    sep=",",
    header=None,
    names=column_names,
    engine="python"
)

print(df.head())
print(df.shape)

#
df.replace("?", np.nan, inplace=True)

df = df.apply(pd.to_numeric)

df.dropna(inplace=True)

print(df.shape)

# Binarize target
df["target"] = df["target"].apply(lambda x: 1 if x > 0 else 0)

# Split features and label
X = df.drop("target", axis=1)
y = df["target"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Export model
joblib.dump(model, "heart_model.pkl")
joblib.dump(scaler, "scaler.pk1")

print("Model and scaler saved.")