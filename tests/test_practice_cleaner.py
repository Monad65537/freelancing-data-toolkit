import pandas as pd

from practice_cleaner import remove_exact_duplicates


def test_removes_exact_duplicates():
    df = pd.DataFrame({
        "customer_id": ["00123", "00123", "00456"],
        "amount": [100, 100, 200],
    })

    result = remove_exact_duplicates(df)

    assert len(result) == 2


def test_preserves_different_records_with_same_id():
    df = pd.DataFrame({
        "customer_id": ["00456", "00456"],
        "amount": [100, 200],
    })

    result = remove_exact_duplicates(df)

    assert len(result) == 2


def test_does_not_modify_original():
    df = pd.DataFrame({
        "customer_id": ["00123", "00123"],
        "amount": [100, 100],
    })

    remove_exact_duplicates(df)

    assert len(df) == 2

def test_preserves_leading_zeros():
    df = pd.DataFrame({
        "customer_id": ["00123", "00123"],
        "amount": [100, 100],
    })

    result = remove_exact_duplicates(df)

    assert result["customer_id"].iloc[0] == "00123"