
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Paths
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "transactions_enriched.csv"
REPORT_PATH = ROOT / "reports" / "fraud_threshold_analysis.md"

RANDOM_STATE = 42
BASELINE_THRESHOLD = 0.50
THRESHOLDS = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]

# Load data
df = pd.read_csv(DATA_PATH)

target = "is_fraud"

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

X = df[features].copy()
y = df[target].astype(int)

# Reproduce the three-way split used by the validation script:
# 20% test holdout, then 75/25 split of the remaining 80%.
X_remaining, X_test_reserved, y_remaining, y_test_reserved = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=RANDOM_STATE,
)

X_train, X_validation, y_train, y_validation = train_test_split(
    X_remaining,
    y_remaining,
    test_size=0.25,
    stratify=y_remaining,
    random_state=RANDOM_STATE,
)

# Explicitly do not fit, predict, score, or tune on the reserved test set.
del X_test_reserved, y_test_reserved

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]
)

binary_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features),
        ("binary", binary_pipeline, binary_features),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=RANDOM_STATE,
            ),
        ),
    ]
)

# Fit only on training data; obtain probabilities only for validation data.
model.fit(X_train, y_train)
validation_probabilities = model.predict_proba(X_validation)[:, 1]

print("Threshold analysis — validation set only")
print(f"Training rows: {len(X_train):,}")
print(f"Validation rows: {len(X_validation):,}")
print(f"Validation fraud-labelled rows: {int(y_validation.sum()):,}")
print(f"Validation fraud prevalence: {y_validation.mean():.2%}")
print(f"Validation PR-AUC: {average_precision_score(y_validation, validation_probabilities):.4f}")
print(f"Validation ROC-AUC: {roc_auc_score(y_validation, validation_probabilities):.4f}")
print()
print(
    f"{'Threshold':>9} {'Precision':>10} {'Recall':>10} "
    f"{'F1':>8} {'TP':>6} {'FP':>7} {'FN':>6} {'TN':>7} {'Alerts':>8}"
)

results = []

for threshold in THRESHOLDS:
    predictions = (validation_probabilities >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(
        y_validation, predictions, labels=[0, 1]
    ).ravel()

    precision = precision_score(
        y_validation, predictions, zero_division=0
    )
    recall = recall_score(
        y_validation, predictions, zero_division=0
    )
    f1 = f1_score(y_validation, predictions, zero_division=0)

    row = {
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "tn": int(tn),
        "alerts": int(tp + fp),
    }
    results.append(row)

    print(
        f"{threshold:>9.2f} {precision:>10.4f} {recall:>10.4f} "
        f"{f1:>8.4f} {tp:>6} {fp:>7} {fn:>6} {tn:>7} {tp + fp:>8}"
    )

results_df = pd.DataFrame(results)
results_df.to_csv(ROOT / "reports" / "fraud_threshold_analysis.csv", index=False)

baseline = next(
    row for row in results if row["threshold"] == BASELINE_THRESHOLD
)

report_lines = [
    "# Fraud Detection Threshold Analysis",
    "",
    "## Scope and methodology",
    "",
    "- Dataset: synthetic transaction data; not actual Razorpay internal data.",
    "- Model: class-weighted logistic regression with the same feature pipeline as the validation baseline.",
    "- Training set: 60% of the full dataset.",
    "- Validation set: 20% of the full dataset.",
    "- Reserved test set: 20%; not used for fitting, threshold selection, or evaluation.",
    "- Thresholds compared: 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80.",
    "- The 0.50 threshold remains the baseline; no final threshold is selected automatically.",
    "",
    "## Validation metrics",
    "",
    f"- Validation PR-AUC: {average_precision_score(y_validation, validation_probabilities):.4f}",
    f"- Validation ROC-AUC: {roc_auc_score(y_validation, validation_probabilities):.4f}",
    f"- Validation fraud-labelled rows: {int(y_validation.sum()):,} of {len(y_validation):,}",
    "",
    "| Threshold | Precision | Recall | F1 | TP | FP | FN | TN | Alerts |",
    "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
]

for row in results:
    report_lines.append(
        f"| {row['threshold']:.2f} | {row['precision']:.4f} | "
        f"{row['recall']:.4f} | {row['f1']:.4f} | {row['tp']} | "
        f"{row['fp']} | {row['fn']} | {row['tn']} | {row['alerts']} |"
    )

report_lines += [
    "",
    "## Baseline threshold (0.50)",
    "",
    f"- Precision: {baseline['precision']:.4f}",
    f"- Recall: {baseline['recall']:.4f}",
    f"- F1: {baseline['f1']:.4f}",
    f"- True positives: {baseline['tp']}",
    f"- False positives: {baseline['fp']}",
    f"- False negatives: {baseline['fn']}",
    f"- Total alerts: {baseline['alerts']}",
    "",
    "## Interpretation cautions",
    "",
    "Lower thresholds typically increase the number of alerts and may catch more "
    "fraud-labelled cases, but can increase false positives. Higher thresholds "
    "typically reduce alerts but may miss more fraud-labelled cases. Use the "
    "measured results above rather than assuming these effects for any particular "
    "threshold.",
    "",
    "Threshold choice should reflect review capacity and the relative costs of "
    "missed fraud versus false alerts. These results do not establish production "
    "performance: the dataset is synthetic and label-generation methodology, "
    "feature timing, and potential target leakage remain unresolved.",
    "",
    "The reserved test set must remain untouched until the threshold and evaluation "
    "approach have been finalized.",
]

REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

print()
print(f"Saved CSV: {ROOT / 'reports' / 'fraud_threshold_analysis.csv'}")
print(f"Saved report: {REPORT_PATH}")
print("Reserved test set was not evaluated.")
