
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("No CSV files found in the data folder.")
    print("Download the dataset CSV files into the data folder first.")
    raise SystemExit(1)

for file_path in csv_files:
    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    df = pd.read_csv(file_path, low_memory=False)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    print("\nColumn names and data types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).to_string())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nSample records:")
    print(df.head(5).to_string(index=False))

    print("\nUnique values per column:")
    print(df.nunique(dropna=False).to_string())
