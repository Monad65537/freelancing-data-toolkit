
import pandas as pd


def validate_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separate accepted and invalid customer records."""

    required = {
        "customer_id", "name", "email",
        "amount", "order_date"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    data = df.copy().reset_index(drop=True)

    # Record the original CSV line number.
    # Assumes one header row and no skipped lines.
    data["source_row"] = data.index + 2

    ids = data["customer_id"].astype("string").str.strip()
    emails = data["email"].astype("string").str.strip()
    amounts = pd.to_numeric(data["amount"], errors="coerce")

    date_text = data["order_date"].astype("string").str.strip()
    dates = pd.to_datetime(
        date_text,
        format="%Y-%m-%d",
        errors="coerce",
    )

    # A basic format check, not proof of email deliverability.
    valid_emails = emails.str.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        na=False,
    )

    duplicate_ids = ids.duplicated(keep="first")

    reasons = []

    for i in range(len(data)):
        errors = []

        if pd.isna(ids.iloc[i]) or ids.iloc[i] == "":
            errors.append("Missing customer ID")

        if duplicate_ids.iloc[i] and pd.notna(ids.iloc[i]):
            errors.append("Duplicate customer ID")

        if not valid_emails.iloc[i]:
            errors.append("Invalid or missing email")

        if pd.isna(amounts.iloc[i]):
            errors.append("Invalid amount")
        elif amounts.iloc[i] < 0:
            errors.append("Negative amount")

        if pd.isna(dates.iloc[i]):
            errors.append("Invalid date")

        reasons.append("; ".join(errors))

    data["rejection_reasons"] = reasons

    invalid_mask = data["rejection_reasons"] != ""

    accepted = data.loc[~invalid_mask].copy()
    flagged = data.loc[invalid_mask].copy()

    accepted = accepted.drop(columns=["rejection_reasons"])

    return (
        accepted.reset_index(drop=True),
        flagged.reset_index(drop=True),
    )
