
from pathlib import Path

import pandas as pd


def load_data(path: str | Path) -> pd.DataFrame:
    """Load CSV or Excel data while preserving customer IDs."""

    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Input file does not exist: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".csv":
        df = pd.read_csv(
            file_path,
            dtype={"customer_id": "string"}
        )

    elif extension == ".xlsx":
        df = pd.read_excel(
            file_path,
            dtype={"customer_id": "string"}
        )

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean customer data without modifying the original."""

    cleaned = df.copy()

    # Standardize column names.
    cleaned.columns = (
        cleaned.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Ensure that required columns exist.
    required = {
        "customer_id",
        "name",
        "email",
        "amount",
        "order_date",
    }

    missing = required - set(cleaned.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # Remove surrounding whitespace from customer IDs.
    cleaned["customer_id"] = (
        cleaned["customer_id"]
        .astype("string")
        .str.strip()
    )

    # Normalize customer names.
    cleaned["name"] = (
        cleaned["name"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # Normalize email addresses.
    cleaned["email"] = (
        cleaned["email"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    return cleaned
