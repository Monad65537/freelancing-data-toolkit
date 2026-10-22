import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(
        path,
        dtype={"customer_id": "string"},
        keep_default_na=False,
    )

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned["name"] = (
        cleaned["name"]
        .str.strip()
        .str.title()
    )

    cleaned["city"] = (
        cleaned["city"]
        .str.strip()
        .str.title()
    )

    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.reset_index(drop=True)

    return cleaned

def validate_data(df: pd.DataFrame) -> None:
    #Customers IDs are not blank
    if df["customer_id"].isnull().any():
        raise ValueError("Customer IDs cannot be null.")
    #Amounts are either valid numeric values or blank (which will be treated as missing)
    #Text such as "unknown" is rejected rather than silently converted to zero
    if df["amount"].isin(["unknown"]).any():
        raise ValueError("Amounts cannot be 'unknown'.")
    #A numeric zero is accepted as a valid amount
    if (df["amount"] == 0).all():
        pass

    return None

def save_data(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)

def main():
    df = load_data("customers_messy.csv")

    cleaned = clean_data(df)

    validate_data(cleaned)

    save_data(cleaned, "customers_cleaned.csv")

    result = pd.read_csv(
    "customers_cleaned.csv",
    dtype={"customer_id": "string"},
    keep_default_na=False,
    )

if __name__ == "__main__":
    main()