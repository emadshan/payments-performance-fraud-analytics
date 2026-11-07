
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

THRESHOLD = 0.50
RANDOM_STATE = 42

df = pd.read_csv(DATA_PATH)

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

for col in numeric_features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in binary_features + ["is_fraud"]:
    df[col] = (
        df[col]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({"true": 1, "false": 0, "1": 1, "0": 0})
    )

df = df.dropna(subset=["is_fraud"])
df["is_fraud"] = df["is_fraud"].astype(int)

X = df[features]
y = df["is_fraud"]

# First reserve 20% for the final test set.
X_development, X_test, y_development, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y,
)

# Split the remaining 80% into 60% training and 20% validation
# of the full dataset.
X_train, X_validation, y_train, y_validation = train_test_split(
    X_development,
    y_development,
    test_size=0.25,
    random_state=RANDOM_STATE,
    stratify=y_development,
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
        random_state=RANDOM_STATE,
    )),
])

# Fit using training data only.
model.fit(X_train, y_train)

# Evaluate the fixed 50% threshold on validation data.
validation_probabilities = model.predict_proba(X_validation)[:, 1]
validation_predictions = (
    validation_probabilities >= THRESHOLD
).astype(int)

print("=== DATA SPLITS ===")
for name, labels in [
    ("Training", y_train),
    ("Validation", y_validation),
    ("Test", y_test),
]:
    print(
        f"{name}: {len(labels):,} rows | "
        f"{int(labels.sum()):,} fraud-labelled | "
        f"{labels.mean():.2%} prevalence"
    )

print(f"\n=== VALIDATION RESULTS AT {THRESHOLD:.0%} THRESHOLD ===")
print(f"PR-AUC: {average_precision_score(y_validation, validation_probabilities):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_validation, validation_probabilities):.4f}")
print(
    "Precision:",
    f"{precision_score(y_validation, validation_predictions, zero_division=0):.4f}",
)
print(
    "Recall:",
    f"{recall_score(y_validation, validation_predictions, zero_division=0):.4f}",
)
print("Confusion matrix [[TN, FP], [FN, TP]]:")
print(confusion_matrix(y_validation, validation_predictions, labels=[0, 1]))
print("\nClassification report:")
print(classification_report(
    y_validation,
    validation_predictions,
    labels=[0, 1],
    target_names=["Non-fraud-labelled", "Fraud-labelled"],
    zero_division=0,
))

# Do not evaluate or tune against the test set in this step.
print("\nThe test set is reserved for final evaluation.")
print("No threshold tuning has been performed.")
