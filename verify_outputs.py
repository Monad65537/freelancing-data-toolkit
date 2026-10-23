
from pathlib import Path

import pandas as pd


def read_output(folder, filename):
    return pd.read_csv(
        Path(folder) / filename,
        dtype={"customer_id": "string"},
    )


csv_dir = "outputs/large_csv"
excel_dir = "outputs/large_excel"

for filename in [
    "cleaned_customers.csv",
    "flagged_rows.csv",
]:
    csv_data = read_output(csv_dir, filename)
    excel_data = read_output(excel_dir, filename)

    # Every input record has a source-row identifier.
    csv_rows = set(csv_data["source_row"])
    excel_rows = set(excel_data["source_row"])

    assert csv_rows == excel_rows, (
        f"Different records in {filename}"
    )

    assert len(csv_data) == len(excel_data)

    print(f"Verified: {filename}")

print("CSV and Excel classify the same source rows.")
