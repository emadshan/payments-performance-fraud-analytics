
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_DIR / "transactions.csv")

# Preserve the original supplied feature.
df["supplied_time_since_last_txn_min"] = (
    df["time_since_last_txn_min"]
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="raise"
)

# Sort chronologically per user; transaction_id breaks timestamp ties.
df = df.sort_values(
    ["user_id", "timestamp", "transaction_id"]
).copy()

# Recalculate using only the previous observed transaction
# for the same user in this dataset.
df["recalculated_time_since_last_txn_min"] = (
    df.groupby("user_id")["timestamp"]
    .diff()
    .dt.total_seconds()
    .div(60)
)

# Validate the reconstructed feature.
negative_count = (
    df["recalculated_time_since_last_txn_min"] < 0
).sum()

print("Rows:", len(df))
print("Negative reconstructed intervals:", negative_count)
print(
    "Missing reconstructed intervals:",
    df["recalculated_time_since_last_txn_min"].isna().sum()
)

assert negative_count == 0

# Save the derived dataset without overwriting the raw source.
output_path = OUTPUT_DIR / "transactions_enriched.csv"
df.to_csv(output_path, index=False)

print("Saved:", output_path)
print("Original source CSV remains unchanged.")
