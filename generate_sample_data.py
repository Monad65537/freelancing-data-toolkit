
from pathlib import Path
import random

import pandas as pd


def generate_dataset(
    rows: int = 1000,
    seed: int = 42,
) -> pd.DataFrame:
    rng = random.Random(seed)

    first_names = [
        "Alice", "Bob", "Charlie",
        "Diana", "Eve", "Frank",
    ]

    last_names = [
        "Smith", "Jones", "Brown",
        "Green", "White", "Miller",
    ]

    records = []

    for i in range(rows):
        customer_id = f"{i + 1:06d}"

        first = rng.choice(first_names)
        last = rng.choice(last_names)

        record = {
            "customer_id": customer_id,
            "name": f"  {first.upper()} {last.lower()}  ",
            "email": (
                f"{first.lower()}.{last.lower()}{i}"
                "@example.com"
            ),
            "amount": str(round(rng.uniform(10, 500), 2)),
            "order_date": "2026-10-15",
        }

        # Introduce one controlled error in
        # approximately 15% of records.
        if rng.random() < 0.15:
            error = rng.choice([
                "duplicate",
                "invalid_amount",
                "negative_amount",
                "invalid_email",
                "invalid_date",
            ])

            if error == "duplicate" and i > 0:
                record["customer_id"] = records[-1]["customer_id"]

            elif error == "invalid_amount":
                record["amount"] = "unknown"

            elif error == "negative_amount":
                record["amount"] = "-50"

            elif error == "invalid_email":
                record["email"] = "invalid-email"

            elif error == "invalid_date":
                record["order_date"] = "not-a-date"

        records.append(record)

    return pd.DataFrame(records)


if __name__ == "__main__":
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    df = generate_dataset()

    df.to_csv(
        output_dir / "large_customers.csv",
        index=False,
    )

    df.to_excel(
        output_dir / "large_customers.xlsx",
        index=False,
    )

    print(f"Generated {len(df)} records.")
