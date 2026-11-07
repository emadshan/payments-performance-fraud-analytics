from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

transactions = pd.read_csv(ROOT / "data" / "transactions.csv")
labels = pd.read_csv(ROOT / "data" / "fraud_labels.csv")

columns_to_compare = [
    "is_fraud",
    "new_device_flag",
    "ip_location_mismatch",
    "failed_attempts_last_24h",
    "transaction_velocity",
    "amount_deviation_score",
]

required_txn = ["transaction_id"] + columns_to_compare
required_labels = ["transaction_id"] + columns_to_compare

for name, df, required in [
    ("transactions.csv", transactions, required_txn),
    ("fraud_labels.csv", labels, required_labels),
]:
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"{name} is missing columns: {missing}")

print("=== KEY COUNTS ===")
print("Transactions rows:", len(transactions))
print("Transactions unique IDs:", transactions["transaction_id"].nunique())
print("Fraud-label rows:", len(labels))
print("Fraud-label unique IDs:", labels["transaction_id"].nunique())

left = transactions[required_txn].copy()
right = labels[required_labels].copy()

comparison = left.merge(
    right,
    on="transaction_id",
    how="outer",
    suffixes=("_txn", "_label"),
    indicator=True,
    validate="one_to_one",
)

print("\n=== TRANSACTION ID MATCHING ===")
print(comparison["_merge"].value_counts().to_string())

matched = comparison[comparison["_merge"] == "both"]

print("\n=== FIELD MISMATCHES AMONG MATCHED IDs ===")
for col in columns_to_compare:
    a = matched[f"{col}_txn"]
    b = matched[f"{col}_label"]

    if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
        equal = a.eq(b) | (a.isna() & b.isna())
    else:
        equal = a.astype("string").eq(b.astype("string")) | (
            a.isna() & b.isna()
        )

    print(f"{col}: {(~equal).sum()} mismatches")

print("\n=== INTERPRETATION ===")
print(
    "Exact matches establish consistency between files only. "
    "They do not establish label validity, causal direction, feature timing, "
    "or absence of target leakage."
)