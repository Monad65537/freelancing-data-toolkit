import pandas as pd
import pytest

from client_pipeline import (
    clean_data,
    validate_data,
    load_data,
    save_data,
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