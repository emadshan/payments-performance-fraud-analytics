
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
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "transactions_enriched.csv"
REPORT_PATH = ROOT / "reports" / "fraud_model_final_evaluation.md"

RANDOM_STATE = 42
THRESHOLD = 0.50

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

df = pd.read_csv(DATA_PATH)

required = features + ["is_fraud"]
missing = sorted(set(required) - set(df.columns))
if missing:
    raise ValueError(f"Missing expected columns: {missing}")

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

df = df.dropna(subset=["is_fraud"]).copy()
df["is_fraud"] = df["is_fraud"].astype(int)

X = df[features]
y = df["is_fraud"]

# Reproduce the established split exactly.
# The test labels are not summarized or used until final scoring.
X_development, X_test, y_development, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y,
)

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

# Fit only on training data.
model.fit(X_train, y_train)

# Validation is not used to tune the model or threshold here.
# The 0.50 threshold was fixed in advance for final comparison.
test_probabilities = model.predict_proba(X_test)[:, 1]
test_predictions = (test_probabilities >= THRESHOLD).astype(int)

# Test labels are used only now, for the one-time final evaluation.
tn, fp, fn, tp = confusion_matrix(
    y_test, test_predictions, labels=[0, 1]
).ravel()

pr_auc = average_precision_score(y_test, test_probabilities)
roc_auc = roc_auc_score(y_test, test_probabilities)
precision = precision_score(y_test, test_predictions, zero_division=0)
recall = recall_score(y_test, test_predictions, zero_division=0)
f1 = f1_score(y_test, test_predictions, zero_division=0)

print("=== FINAL HELD-OUT TEST RESULTS ===")
print(f"Test rows: {len(y_test):,}")
print(f"Test fraud-labelled rows: {int(y_test.sum()):,}")
print(f"Test prevalence: {y_test.mean():.2%}")
print(f"Threshold: {THRESHOLD:.2f}")
print(f"PR-AUC: {pr_auc:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1: {f1:.4f}")
print("Confusion matrix [[TN, FP], [FN, TP]]:")
print([[int(tn), int(fp)], [int(fn), int(tp)]])
print("\nClassification report:")
print(classification_report(
    y_test,
    test_predictions,
    labels=[0, 1],
    target_names=["Non-fraud-labelled", "Fraud-labelled"],
    zero_division=0,
))

report = f"""# Fraud Model — Final Held-Out Test Evaluation

## Evaluation protocol

- Dataset: synthetic transaction data, not actual Razorpay internal data.
- Model: class-weighted Logistic Regression.
- Random state: {RANDOM_STATE}.
- Split: 60% training, 20% validation, 20% held-out test.
- Threshold: {THRESHOLD:.2f}, fixed before final test evaluation.
- The model was fitted on training data only.
- The reserved test set was evaluated once for this report.

## Final test metrics

| Metric | Result |
|---|---:|
| Test rows | {len(y_test):,} |
| Fraud-labelled test rows | {int(y_test.sum()):,} |
| Test fraud prevalence | {y_test.mean():.2%} |
| Threshold | {THRESHOLD:.2f} |
| PR-AUC | {pr_auc:.4f} |
| ROC-AUC | {roc_auc:.4f} |
| Precision | {precision:.4f} |
| Recall | {recall:.4f} |
| F1 | {f1:.4f} |

## Confusion matrix

| Actual / Predicted | Non-fraud | Fraud |
|---|---:|---:|
| Non-fraud-labelled | {int(tn)} | {int(fp)} |
| Fraud-labelled | {int(fn)} | {int(tp)} |

## Interpretation cautions

These results estimate performance on a held-out portion of the supplied synthetic dataset. They do not establish performance on real Razorpay transactions or production fraud patterns.

The original fraud-label-generation method, feature-generation timing, and potential target leakage remain unresolved. Results should therefore be treated as exploratory rather than production evidence.

The threshold was not selected using test results. No threshold comparison was performed on the test set.
"""

REPORT_PATH.write_text(report, encoding="utf-8")

print(f"\nSaved report: {REPORT_PATH}")
print("No test-threshold tuning was performed.")
