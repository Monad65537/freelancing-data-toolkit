"""Behavior and data integrity tests for column name normalization."""

from decimal import Decimal

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from data_toolkit.cleaner import normalize_column_names


def test_specification_example() -> None:
    df = pd.DataFrame(
        [["00123", "Ada", Decimal("12.30"), "ada@example.test"]],
        columns=[" Customer ID ", "First Name", " Total  Amount ", "EMAIL Address"],
    )
    original = df.copy(deep=True)
    expected = df.copy(deep=True)
    expected.columns = ["customer_id", "first_name", "total_amount", "email_address"]

    result = normalize_column_names(df)

    assert result is not df
    assert_frame_equal(result, expected)
    assert_frame_equal(df, original)


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        (" Customer ID ", "customer_id"),
        ("\t\r\nCustomer ID\n\t", "customer_id"),
        ("Total   Amount", "total_amount"),
        ("First\t\n\r\v\f Name", "first_name"),
        ("\u00a0Customer\u2003\u202fID\u3000", "customer_id"),
        ("UPPERCASE", "uppercase"),
        ("mIxEdCaSe", "mixedcase"),
        ("Straße ÉTÉ İ", "straße_été_i\u0307"),
        ("customer_id", "customer_id"),
        ("Price ($)/Unit-ID.Name", "price_($)/unit-id.name"),
        ("__Customer__ID__", "__customer__id__"),
        ("", ""),
        (" \t\n\u00a0", ""),
    ],
)
def test_normalization_rules(label: str, expected: str) -> None:
    df = pd.DataFrame([["0007"]], columns=[label])
    expected_df = pd.DataFrame([["0007"]], columns=[expected])

    assert_frame_equal(normalize_column_names(df), expected_df)


@pytest.mark.parametrize(
    ("labels", "duplicate"),
    [
        (["Customer ID", "customer_id"], "customer_id"),
        (["Name", "NAME"], "name"),
        (["Name", " Name "], "name"),
        (["First  Name", "First\tName"], "first_name"),
        (["same", "same"], "same"),
        (["", " \t"], ""),
        (["unrelated", "Customer ID", "customer_id"], "customer_id"),
    ],
)
@pytest.mark.parametrize("row_count", [0, 2])
def test_collisions_raise_without_mutation(
    labels: list[str], duplicate: str, row_count: int
) -> None:
    df = pd.DataFrame(
        [[f"00{row}"] * len(labels) for row in range(row_count)], columns=labels
    )
    original = df.copy(deep=True)

    with pytest.raises(ValueError) as error:
        normalize_column_names(df)

    message = str(error.value)
    assert "Duplicate normalized column name" in message
    assert repr(duplicate) in message
    assert f"positions {len(labels) - 2} and {len(labels) - 1}" in message
    assert_frame_equal(df, original)


@pytest.mark.parametrize("label", [1, 1.5, True, None, float("nan"), ("A", "B"), b"A"])
def test_non_string_labels_raise_without_mutation(label: object) -> None:
    df = pd.DataFrame([["001", "002"]], columns=[" Valid ", label])
    original = df.copy(deep=True)

    with pytest.raises(TypeError, match="position 1 must be a string"):
        normalize_column_names(df)

    assert_frame_equal(df, original)


def test_non_string_validation_includes_labels_after_a_collision() -> None:
    df = pd.DataFrame(columns=["Name", "NAME", 1])

    with pytest.raises(TypeError, match="position 2 must be a string"):
        normalize_column_names(df)


def test_multiindex_column_labels_are_rejected() -> None:
    df = pd.DataFrame([[1]], columns=pd.MultiIndex.from_tuples([("A", "B")]))
    original = df.copy(deep=True)

    with pytest.raises(TypeError, match="position 0 must be a string; got tuple"):
        normalize_column_names(df)

    assert_frame_equal(df, original)


@pytest.mark.parametrize("value", [None, "name", 42, [], {}, pd.Series([1])])
def test_non_dataframe_inputs_are_rejected(value: object) -> None:
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        normalize_column_names(value)


@pytest.mark.parametrize(
    "df",
    [
        pd.DataFrame(),
        pd.DataFrame(index=pd.Index([3, 1, 3], name="row")),
        pd.DataFrame(columns=pd.Index([], dtype="object", name="fields")),
        pd.DataFrame(
            {
                " Customer ID ": pd.Series(dtype="string"),
                " Amount ": pd.Series(dtype="Int64"),
            }
        ),
    ],
    ids=["no-rows-or-columns", "no-columns", "named-empty-columns", "no-rows"],
)
def test_empty_dataframes(df: pd.DataFrame) -> None:
    original = df.copy(deep=True)
    expected = df.copy(deep=True)
    if len(df.columns):
        expected.columns = ["customer_id", "amount"]

    result = normalize_column_names(df)

    assert result is not df
    assert result.shape == df.shape
    assert_frame_equal(result, expected)
    assert_frame_equal(df, original)


def test_preserves_values_dtypes_order_and_axes() -> None:
    df = pd.DataFrame(
        {
            " Customer ID ": pd.Series(["00123", "00000", pd.NA], dtype="string"),
            " Amount ": pd.Series([10, pd.NA, -3], dtype="Int64"),
            " Count ": pd.Series([0, 255, 1], dtype="uint8"),
            " Ratio ": pd.Series([1.25, float("nan"), -0.0], dtype="float32"),
            " Active ": pd.Series([True, pd.NA, False], dtype="boolean"),
            " Category ": pd.Categorical(
                ["B", None, "A"], categories=["B", "A"], ordered=True
            ),
            " Timestamp ": pd.to_datetime(["2026-01-01", None, "2026-01-03"], utc=True),
            " Duration ": pd.to_timedelta([1, None, 3], unit="s"),
            " Exact Price ": pd.Series(
                [Decimal("12.30"), None, Decimal("0.01")], dtype="object"
            ),
        }
    )
    df.index = pd.MultiIndex.from_tuples(
        [("B", 3), ("A", 1), ("B", 3)], names=["group", "row"]
    )
    df.columns.name = "fields"
    original = df.copy(deep=True)
    expected = df.copy(deep=True)
    expected.columns = pd.Index(
        [
            "customer_id",
            "amount",
            "count",
            "ratio",
            "active",
            "category",
            "timestamp",
            "duration",
            "exact_price",
        ],
        name="fields",
    )

    result = normalize_column_names(df)

    assert result.shape == df.shape
    assert_frame_equal(result, expected)
    assert_frame_equal(df, original)


def test_returned_dataframe_can_be_modified_independently() -> None:
    df = pd.DataFrame({" Customer ID ": ["00123", "00456"]})
    original = df.copy(deep=True)
    result = normalize_column_names(df)

    result.iloc[0, 0] = "99999"
    result.columns = ["changed"]
    result.index = [10, 20]

    assert_frame_equal(df, original)


def test_normalization_is_deterministic_and_idempotent() -> None:
    df = pd.DataFrame({" A B ": ["001"], "C\tD": [None]})
    first = normalize_column_names(df)
    second = normalize_column_names(df)
    repeated = normalize_column_names(first)

    assert first is not second
    assert repeated is not first
    assert_frame_equal(first, second)
    assert_frame_equal(first, repeated)
