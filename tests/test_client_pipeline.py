import pandas as pd
import pytest

from client_pipeline import (
    clean_data,
    load_data,
    save_data,
    validate_data,
)


def test_cleaning_preserves_original_data():
    df = pd.DataFrame({
        "customer_id": ["00123", "00123"],
        "name": [" Anna ", " Anna "],
        "amount": ["100", "100"],
        "city": ["Warsaw", "Warsaw"],
    })

    original = df.copy(deep=True)

    cleaned = clean_data(df)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "name"] == "Anna"
    assert cleaned.loc[0, "customer_id"] == "00123"

    pd.testing.assert_frame_equal(df, original)


def test_invalid_amount_is_rejected():
    df = pd.DataFrame({
        "customer_id": ["00123"],
        "amount": ["unknown"],
    })

    with pytest.raises(ValueError):
        validate_data(df)


def test_zero_and_blank_amounts_are_accepted():
    df = pd.DataFrame({
        "customer_id": ["00123", "00456"],
        "amount": ["0", ""],
    })

    validate_data(df)


def test_export_preserves_customer_ids(tmp_path):
    df = pd.DataFrame({
        "customer_id": ["00123", "00456"],
        "name": ["Anna", "Bob"],
        "amount": ["100", "200"],
        "city": ["Warsaw", "Krakow"],
    })

    output_path = tmp_path / "cleaned.csv"

    save_data(df, str(output_path))

    loaded = load_data(str(output_path))

    assert output_path.exists()
    assert loaded["customer_id"].tolist() == ["00123", "00456"]
    assert len(loaded) == 2


@pytest.mark.parametrize(
    "invalid_id",
    ["", "   ", None, pd.NA],
)
def test_validate_data_rejects_blank_customer_ids(invalid_id):
    df = pd.DataFrame(
        {
            "customer_id": [invalid_id],
            "name": ["Alice"],
            "email": ["alice@example.com"],
            "amount": ["100.00"],
            "order_date": ["2026-10-15"],
        }
    )

    with pytest.raises(ValueError, match="Customer IDs cannot be blank"):
        validate_data(df)


def test_validate_data_preserves_leading_zero_ids():
    df = pd.DataFrame(
        {
            "customer_id": ["000123"],
            "name": ["Alice"],
            "email": ["alice@example.com"],
            "amount": ["100.00"],
            "order_date": ["2026-10-15"],
        }
    )

    validate_data(df)

    assert df.loc[0, "customer_id"] == "000123"


def test_load_data_preserves_literal_na_and_leading_zeros(tmp_path):
    input_file = tmp_path / "customers.csv"
    input_file.write_text(
        "customer_id,name,amount\n"
        "000123,Alice,100.00\n"
        "NA,Bob,50.00\n",
        encoding="utf-8",
    )

    df = load_data(str(input_file))

    assert df["customer_id"].tolist() == ["000123", "NA"]
