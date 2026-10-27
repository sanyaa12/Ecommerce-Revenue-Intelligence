
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading e-commerce dataset...")

df = pd.read_excel(RAW_FILE)

print("Original rows:", len(df))

# Remove rows without essential information
df = df.dropna(subset=["InvoiceNo", "StockCode", "Description",
                       "Quantity", "InvoiceDate", "UnitPrice"])

# Remove duplicate rows
df = df.drop_duplicates()

# Convert data types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# Remove rows with invalid numeric values
df = df.dropna(subset=["Quantity", "UnitPrice"])

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Save cleaned data
OUTPUT_FILE = OUTPUT_DIR / "cleaned_retail.csv"
df.to_csv(OUTPUT_FILE, index=False)

print("Cleaned rows:", len(df))
print("Saved cleaned dataset to:", OUTPUT_FILE)
print("Data cleaning completed successfully!")
