
import json
from pathlib import Path

import pandas as pd


def generate_report(
    accepted: pd.DataFrame,
    flagged: pd.DataFrame,
) -> dict:
    """Generate statistics describing data quality."""

    reasons = flagged["rejection_reasons"].fillna("")

    report = {
        "input_rows": len(accepted) + len(flagged),
        "accepted_rows": len(accepted),
        "flagged_rows": len(flagged),
        "duplicate_id_rows": int(
            reasons.str.contains(
                "Duplicate customer ID",
                regex=False,
            ).sum()
        ),
        "invalid_amount_rows": int(
            reasons.str.contains(
                "Invalid amount",
                regex=False,
            ).sum()
        ),
        "negative_amount_rows": int(
            reasons.str.contains(
                "Negative amount",
                regex=False,
            ).sum()
        ),
        "invalid_email_rows": int(
            reasons.str.contains(
                "Invalid or missing email",
                regex=False,
            ).sum()
        ),
        "invalid_date_rows": int(
            reasons.str.contains(
                "Invalid date",
                regex=False,
            ).sum()
        ),
        "missing_id_rows": int(
            reasons.str.contains(
                "Missing customer ID",
                regex=False,
            ).sum()
        ),
    }

    return report


def save_report(report: dict, path: str | Path) -> None:
    """Save a quality report as JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def save_results(
    accepted: pd.DataFrame,
    flagged: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    """Export accepted and flagged records to CSV."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    accepted.to_csv(
        directory / "cleaned_customers.csv",
        index=False,
    )

    flagged.to_csv(
        directory / "flagged_rows.csv",
        index=False,
    )
