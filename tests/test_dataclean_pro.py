
from dataclean_pro.cleaner import load_data


def test_load_csv_preserves_customer_ids():
    df = load_data("data/messy_customers.csv")

    assert len(df) == 8
    assert df.loc[0, "customer_id"] == "00101"
    assert df.loc[1, "customer_id"] == "00102"


import pandas as pd

from dataclean_pro.cleaner import clean_data


def test_clean_name_and_email():
    df = pd.DataFrame({
        "customer_id": ["00101"],
        "name": ["  aLICE SMITH  "],
        "email": [" ALICE@EXAMPLE.COM "],
        "amount": ["125.50"],
        "order_date": ["2026-10-01"],
    })

    cleaned = clean_data(df)

    assert cleaned.loc[0, "name"] == "Alice Smith"
    assert cleaned.loc[0, "email"] == "alice@example.com"


def test_clean_preserves_original_dataframe():
    df = pd.DataFrame({
        "customer_id": ["00101"],
        "name": ["  aLICE SMITH  "],
        "email": [" ALICE@EXAMPLE.COM "],
        "amount": ["125.50"],
        "order_date": ["2026-10-01"],
    })

    original = df.copy(deep=True)

    clean_data(df)

    pd.testing.assert_frame_equal(df, original)


def test_clean_does_not_delete_duplicates():
    df = pd.DataFrame({
        "customer_id": ["00102", "00102"],
        "name": ["Bob Jones", "Bob Jones"],
        "email": ["bob@example.com", "bob@example.com"],
        "amount": ["80", "90"],
        "order_date": ["2026-10-02", "2026-10-03"],
    })

    cleaned = clean_data(df)

    assert len(cleaned) == 2
    assert cleaned["customer_id"].tolist() == [
        "00102",
        "00102",
    ]


from dataclean_pro.validator import validate_data


def test_validation_separates_invalid_records():
    df = load_data("data/messy_customers.csv")
    cleaned = clean_data(df)

    accepted, flagged = validate_data(cleaned)

    assert len(accepted) == 3
    assert len(flagged) == 5
    assert len(accepted) + len(flagged) == len(df)


def test_validation_preserves_leading_zeros():
    df = load_data("data/messy_customers.csv")
    cleaned = clean_data(df)

    accepted, flagged = validate_data(cleaned)

    assert accepted.loc[0, "customer_id"] == "00101"
    assert flagged.loc[0, "customer_id"] == "00102"


def test_validation_records_error_reasons():
    df = load_data("data/messy_customers.csv")
    cleaned = clean_data(df)

    _, flagged = validate_data(cleaned)

    all_reasons = flagged["rejection_reasons"].tolist()

    assert any("Duplicate customer ID" in r for r in all_reasons)
    assert any("Invalid amount" in r for r in all_reasons)
    assert any("Negative amount" in r for r in all_reasons)
    assert any("Invalid or missing email" in r for r in all_reasons)
    assert any("Invalid date" in r for r in all_reasons)


import pytest


def test_multiple_errors_are_recorded():
    df = pd.DataFrame({
        "customer_id": ["00123"],
        "name": ["Alice"],
        "email": ["invalid-email"],
        "amount": ["-50"],
        "order_date": ["2026-10-15"],
    })

    _, flagged = validate_data(df)

    reasons = flagged.loc[0, "rejection_reasons"]

    assert "Invalid or missing email" in reasons
    assert "Negative amount" in reasons


def test_missing_customer_id_is_flagged():
    df = pd.DataFrame({
        "customer_id": [None],
        "name": ["Alice"],
        "email": ["alice@example.com"],
        "amount": ["50"],
        "order_date": ["2026-10-15"],
    })

    accepted, flagged = validate_data(df)

    assert len(accepted) == 0
    assert len(flagged) == 1
    assert "Missing customer ID" in (
        flagged.loc[0, "rejection_reasons"]
    )


def test_missing_required_column_raises_error():
    df = pd.DataFrame({
        "customer_id": ["00123"],
        "name": ["Alice"],
        "email": ["alice@example.com"],
        "amount": ["50"],
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(df)


def test_validation_does_not_modify_original():
    df = load_data("data/messy_customers.csv")
    cleaned = clean_data(df)

    original = cleaned.copy(deep=True)

    validate_data(cleaned)

    pd.testing.assert_frame_equal(cleaned, original)


import json

from dataclean_pro.report import (
    generate_report,
    save_report,
)


def test_generate_quality_report():
    df = load_data("data/messy_customers.csv")
    cleaned = clean_data(df)
    accepted, flagged = validate_data(cleaned)

    report = generate_report(accepted, flagged)

    assert report["input_rows"] == 8
    assert report["accepted_rows"] == 3
    assert report["flagged_rows"] == 5
    assert report["duplicate_id_rows"] == 1
    assert report["invalid_amount_rows"] == 1
    assert report["negative_amount_rows"] == 1
    assert report["invalid_email_rows"] == 1
    assert report["invalid_date_rows"] == 1


def test_save_quality_report(tmp_path):
    report = {
        "input_rows": 8,
        "accepted_rows": 3,
        "flagged_rows": 5,
    }

    path = tmp_path / "quality_report.json"

    save_report(report, path)

    assert path.exists()

    with path.open(encoding="utf-8") as file:
        loaded = json.load(file)

    assert loaded == report


from dataclean_pro.report import save_results


def test_save_results(tmp_path):
    df = load_data("data/messy_customers.csv")
    cleaned = clean_data(df)
    accepted, flagged = validate_data(cleaned)

    save_results(accepted, flagged, tmp_path)

    accepted_path = tmp_path / "cleaned_customers.csv"
    flagged_path = tmp_path / "flagged_rows.csv"

    assert accepted_path.exists()
    assert flagged_path.exists()

    saved_accepted = pd.read_csv(
        accepted_path,
        dtype={"customer_id": "string"},
    )

    saved_flagged = pd.read_csv(
        flagged_path,
        dtype={"customer_id": "string"},
    )

    assert len(saved_accepted) == 3
    assert len(saved_flagged) == 5
    assert saved_accepted.loc[0, "customer_id"] == "00101"


def test_excel_roundtrip_preserves_ids(tmp_path):
    original = load_data("data/messy_customers.csv")

    excel_path = tmp_path / "customers.xlsx"
    original.to_excel(excel_path, index=False)

    loaded = load_data(excel_path)

    assert len(loaded) == len(original)
    assert loaded.loc[0, "customer_id"] == "00101"
    assert loaded.loc[1, "customer_id"] == "00102"


def test_large_dataset_reconciliation():
    from generate_sample_data import generate_dataset

    original = generate_dataset(rows=1000)
    cleaned = clean_data(original)

    accepted, flagged = validate_data(cleaned)

    assert len(original) == 1000
    assert len(accepted) + len(flagged) == 1000
    assert len(flagged) > 0

    report = generate_report(accepted, flagged)

    assert report["input_rows"] == 1000
    assert report["accepted_rows"] == len(accepted)
    assert report["flagged_rows"] == len(flagged)
