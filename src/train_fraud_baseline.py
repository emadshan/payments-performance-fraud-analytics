
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "transactions_enriched.csv"

df = pd.read_csv(DATA_PATH)

# Keep only features that may be available at transaction assessment time.
# Exclude status, fraud labels, IDs, and post-transaction balance.
numeric_features = [
    "amount",
    "hour_of_day",
    "failed_attempts_last_24h",
    "transaction_velocity",
    "amount_deviation_score",
]

categorical_features = [
    "receiver_type",
    "transaction_type",
    "payment_app",
    "device_type",
    "user_city_tier",
    "user_kyc_status",
]

binary_features = [
    "is_weekend",
    "is_night_transaction",
    "new_device_flag",
    "ip_location_mismatch",
    "recurring_payment_flag",
]

features = numeric_features + categorical_features + binary_features

required = features + ["is_fraud"]
missing_columns = sorted(set(required) - set(df.columns))

if missing_columns:
    raise ValueError(f"Missing expected columns: {missing_columns}")

df = df[required].copy()

# Convert numeric columns safely.
for col in numeric_features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Normalize common Boolean representations.
for col in binary_features + ["is_fraud"]:
    df[col] = (
        df[col]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({
            "true": 1,
            "false": 0,
            "1": 1,
            "0": 0,
        })
    )

df = df.dropna(subset=["is_fraud"])
df["is_fraud"] = df["is_fraud"].astype(int)

X = df[features]
y = df["is_fraud"]

print(f"Rows used: {len(df):,}")
print(f"Fraud-labelled rows: {int(y.sum()):,}")
print(f"Fraud-label rate: {y.mean():.2%}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

binary_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
    ("binary", binary_pipeline, binary_features),
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42,
    )),
])

model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)[:, 1]

# 0.50 is a baseline threshold, not necessarily the best business threshold.
predictions = (probabilities >= 0.50).astype(int)

print("\n--- Test-set evaluation ---")
print(f"Test rows: {len(y_test):,}")
print(f"PR-AUC / Average precision: {average_precision_score(y_test, probabilities):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, probabilities):.4f}")
print(f"Precision at threshold 0.50: {precision_score(y_test, predictions, zero_division=0):.4f}")
print(f"Recall at threshold 0.50: {recall_score(y_test, predictions, zero_division=0):.4f}")

print("\nConfusion matrix [ [TN, FP], [FN, TP] ]:")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Non-fraud-labelled", "Fraud-labelled"],
    zero_division=0,
))

# Compare with a simple model that always predicts the majority class.
majority_predictions = [0] * len(y_test)

print("\n--- Majority-class baseline ---")
print(
    "Accuracy:",
    f"{(y_test.to_numpy() == majority_predictions).mean():.4f}",
)
print(
    "Fraud recall:",
    f"{recall_score(y_test, majority_predictions, zero_division=0):.4f}",
)
