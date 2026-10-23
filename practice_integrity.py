import pandas as pd

df = pd.read_csv(
    "customers_messy.csv",
    dtype={"customer_id": "string"},
    keep_default_na=False,
)



print(df)
print(df.dtypes)
print(df["amount"])

raw_amount = df["amount"].astype("string").str.strip()

amount_numeric = pd.to_numeric(
    raw_amount.replace("", pd.NA),
    errors="coerce",
)

print(amount_numeric)
print(amount_numeric.isna().sum())
print(df[df["amount"] == "0"])