
from pathlib import Path
import pandas as pd

# Locate the project and source dataset
project_dir = Path.home() / "Documents" / "Ecommerce-Revenue-Intelligence"
file_path = project_dir / "data" / "raw" / "Online Retail.xlsx"
output_dir = project_dir / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

print("Loading dataset...")
df = pd.read_excel(file_path)

# Calculate data-quality findings
invoice_text = df["InvoiceNo"].astype(str)
quality_report = {
    "Metric": [
        "Total rows",
        "Total columns",
        "Missing descriptions",
        "Missing customer IDs",
        "Duplicate rows",
        "Zero or negative unit prices",
        "Negative quantities",
        "Zero quantities",
        "Invoice rows starting with C",
        "Earliest transaction date",
        "Latest transaction date",
        "Net line value before cleaning"
    ],
    "Value": [
        len(df),
        len(df.columns),
        int(df["Description"].isna().sum()),
        int(df["CustomerID"].isna().sum()),
        int(df.duplicated().sum()),
        int((df["UnitPrice"] <= 0).sum()),
        int((df["Quantity"] < 0).sum()),
        int((df["Quantity"] == 0).sum()),
        int(invoice_text.str.startswith("C").sum()),
        str(pd.to_datetime(df["InvoiceDate"]).min()),
        str(pd.to_datetime(df["InvoiceDate"]).max()),
        round((df["Quantity"] * df["UnitPrice"]).sum(), 2)
    ]
}

report_df = pd.DataFrame(quality_report)

# Save the report, leaving the original Excel file untouched
report_path = output_dir / "data_quality_report.csv"
report_df.to_csv(report_path, index=False)

print("\n--- DATA QUALITY REPORT ---")
print(report_df.to_string(index=False))
print(f"\nReport saved to: {report_path}")
print("\nInspection completed successfully.")
