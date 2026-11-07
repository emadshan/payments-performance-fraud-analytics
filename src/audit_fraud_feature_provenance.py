
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "transactions_enriched.csv"

df = pd.read_csv(DATA_PATH)

target = "is_fraud"

features_to_audit = [
    "failed_attempts_last_24h",
    "transaction_velocity",
    "amount_deviation_score",
    "new_device_flag",
    "ip_location_mismatch",
    "recurring_payment_flag",
    "transaction_frequency_score",
    "user_avg_txn_value",
    "user_avg_monthly_txn",
    "user_loyalty_score",
    "balance_after_transaction",
]

required = [target] + features_to_audit
missing_columns = [col for col in required if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

df[target] = (
    df[target]
    .astype("string")
    .str.strip()
    .str.lower()
    .map({"true": 1, "false": 0, "1": 1, "0": 0})
)

df = df.dropna(subset=[target]).copy()
df[target] = df[target].astype(int)

print("=== DATASET ===")
print(f"Rows audited: {len(df):,}")
print(f"Fraud-labelled rows: {df[target].sum():,}")
print(f"Fraud-label prevalence: {df[target].mean():.2%}")

print("\n=== MISSINGNESS ===")
print(
    df[features_to_audit]
    .isna()
    .sum()
    .sort_values(ascending=False)
    .to_string()
)

print("\n=== NUMERIC FEATURE SUMMARY BY LABEL ===")
numeric_features = [
    "failed_attempts_last_24h",
    "transaction_velocity",
    "amount_deviation_score",
    "transaction_frequency_score",
    "user_avg_txn_value",
    "user_avg_monthly_txn",
    "user_loyalty_score",
    "balance_after_transaction",
]

for col in numeric_features:
    values = pd.to_numeric(df[col], errors="coerce")
    print(f"\n{col}")
    print(
        df.assign(_value=values)
        .groupby(target)["_value"]
        .agg(["count", "mean", "median", "min", "max"])
        .rename(index={0: "Non-fraud-labelled", 1: "Fraud-labelled"})
        .round(4)
        .to_string()
    )

print("\n=== BINARY FEATURE RATES BY LABEL ===")
binary_features = [
    "new_device_flag",
    "ip_location_mismatch",
    "recurring_payment_flag",
]

for col in binary_features:
    values = (
        df[col]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({"true": 1, "false": 0, "1": 1, "0": 0})
    )
    summary = (
        df.assign(_value=values)
        .groupby(target)["_value"]
        .mean()
        .rename(index={0: "Non-fraud-labelled", 1: "Fraud-labelled"})
    )
    print(f"\n{col} — proportion flagged")
    print((summary * 100).round(2).astype(str).add("%").to_string())

print("\n=== CAUTION ===")
print(
    "Differences between label groups do not establish causality, "
    "valid labels, feature timing, or the absence of target leakage."
)
print(
    "The source dataset's feature-generation and fraud-label-generation "
    "logic remains unverified."
)
