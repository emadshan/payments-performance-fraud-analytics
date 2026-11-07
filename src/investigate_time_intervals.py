
from pathlib import Path
import pandas as pd

path = Path("data/transactions.csv")
df = pd.read_csv(path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce"
)

# Preserve original row order for diagnostics.
df["original_row"] = range(len(df))

# Sort each user's transactions chronologically.
df = df.sort_values(
    ["user_id", "timestamp", "transaction_id"]
).copy()

# Calculate the actual gap from the previous transaction
# for the same user.
df["previous_timestamp"] = (
    df.groupby("user_id")["timestamp"].shift(1)
)

df["actual_gap_minutes"] = (
    df["timestamp"] - df["previous_timestamp"]
).dt.total_seconds() / 60

# Compare supplied feature with independently calculated gap.
df["supplied_negative"] = df["time_since_last_txn_min"] < 0

df["gap_difference"] = (
    df["time_since_last_txn_min"] - df["actual_gap_minutes"]
).abs()

print("=" * 70)
print("TRANSACTION INTERVAL INVESTIGATION")
print("=" * 70)

print("\n1. OVERALL COMPARISON")
print("Transaction rows:", len(df))
print("Rows with no previous transaction for that user:",
      df["previous_timestamp"].isna().sum())
print("Negative supplied intervals:",
      df["supplied_negative"].sum())
print("Valid independently calculated intervals:",
      df["actual_gap_minutes"].notna().sum())

comparable = df[
    df["time_since_last_txn_min"].notna()
    & df["actual_gap_minutes"].notna()
]

print("Comparable rows:", len(comparable))

if len(comparable):
    print("Supplied interval negative:",
          (comparable["time_since_last_txn_min"] < 0).sum())
    print("Actual interval negative:",
          (comparable["actual_gap_minutes"] < 0).sum())
    print("Exact matches within 0.01 minute:",
          (comparable["gap_difference"] <= 0.01).sum())
    print("Median absolute difference:",
          comparable["gap_difference"].median())
    print("Maximum actual gap in minutes:",
          comparable["actual_gap_minutes"].max())

print("\n2. EXAMPLE ROWS WITH NEGATIVE SUPPLIED VALUES")
columns = [
    "transaction_id",
    "user_id",
    "timestamp",
    "time_since_last_txn_min",
    "previous_timestamp",
    "actual_gap_minutes",
]

print(
    df.loc[df["supplied_negative"], columns]
    .head(15)
    .to_string(index=False)
)

print("\n3. MISSING SUPPLIED VALUES")
print(
    df.loc[
        df["time_since_last_txn_min"].isna(),
        columns
    ].head(10).to_string(index=False)
)

print("\n4. STATUS COUNTS")
print(df["status"].value_counts(dropna=False).to_string())

print("\nDiagnostic complete. Raw data has not been modified.")
