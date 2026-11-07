
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

transactions = pd.read_csv(DATA_DIR / "transactions.csv")
fraud = pd.read_csv(DATA_DIR / "fraud_labels.csv")
users = pd.read_csv(DATA_DIR / "users.csv")
merchants = pd.read_csv(DATA_DIR / "merchants.csv")

print("=" * 70)
print("RAZORPAY PAYMENTS INTELLIGENCE: DATA QUALITY CHECKS")
print("=" * 70)

# 1. Primary key uniqueness
print("\n1. PRIMARY KEY CHECKS")
for name, df, key in [
    ("transactions", transactions, "transaction_id"),
    ("fraud_labels", fraud, "transaction_id"),
    ("users", users, "user_id"),
    ("merchants", merchants, "merchant_id"),
]:
    print(
        f"{name}: duplicate {key} values = "
        f"{df[key].duplicated().sum()}"
    )

# 2. Transaction-to-user relationships
print("\n2. USER RELATIONSHIPS")
unknown_users = ~transactions["user_id"].isin(users["user_id"])
print("Transactions with unknown users:", unknown_users.sum())

# 3. Merchant receiver relationships
merchant_receivers = transactions.loc[
    transactions["receiver_type"].eq("Merchant"), "receiver_id"
]
unknown_merchants = ~merchant_receivers.isin(merchants["merchant_id"])
print("Merchant-receiver transactions:", len(merchant_receivers))
print("Transactions with unknown merchants:", unknown_merchants.sum())

# 4. Fraud label reconciliation
print("\n3. FRAUD LABEL RECONCILIATION")
comparison = transactions[
    ["transaction_id", "is_fraud"]
].merge(
    fraud[["transaction_id", "is_fraud"]],
    on="transaction_id",
    how="outer",
    suffixes=("_txn", "_label"),
    indicator=True,
)

print("Transaction IDs missing from either file:",
      (~comparison["_merge"].eq("both")).sum())

matched = comparison[comparison["_merge"].eq("both")]
print("Fraud label mismatches:",
      (matched["is_fraud_txn"] != matched["is_fraud_label"]).sum())

print("\nFraud label distribution in transactions:")
print(transactions["is_fraud"].value_counts(dropna=False).to_string())

# 5. Status distribution
print("\n4. TRANSACTION STATUS")
print(transactions["status"].value_counts(dropna=False).to_string())

# 6. Timestamp and date validation
print("\n5. DATE VALIDATION")
timestamps = pd.to_datetime(transactions["timestamp"], errors="coerce")
dates = pd.to_datetime(transactions["date"], errors="coerce")

print("Invalid timestamps:", timestamps.isna().sum())
print("Invalid dates:", dates.isna().sum())
print("Timestamp/date mismatches:",
      (timestamps.dt.date != dates.dt.date).sum())

# 7. Numeric anomalies
print("\n6. NUMERIC CHECKS")
print("Non-positive amounts:", (transactions["amount"] <= 0).sum())

intervals = transactions["time_since_last_txn_min"]
print("Missing time intervals:", intervals.isna().sum())
print("Negative time intervals:", (intervals < 0).sum())
print("Zero time intervals:", (intervals == 0).sum())

for column in [
    "transaction_velocity",
    "amount_deviation_score",
    "transaction_frequency_score",
    "user_loyalty_score",
]:
    if column in transactions.columns:
        print(f"{column}: min={transactions[column].min()}, "
              f"max={transactions[column].max()}, "
              f"missing={transactions[column].isna().sum()}")

print("\n7. TRANSACTION DATE RANGE")
print("Start:", timestamps.min())
print("End:", timestamps.max())

print("\nChecks completed. Investigate anomalies before cleaning.")
