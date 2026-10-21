"""DataFrame cleaning and standardization."""

import re

import pandas as pd


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with trimmed, lowercase, whitespace-normalized columns.

    Whitespace runs become underscores; all other characters are preserved.
    Empty string labels are allowed if unique. Cell values, dtypes, row index,
    column order, and the column axis name are preserved.

    Raises:
        TypeError: If the input is not a DataFrame or a column is not a string.
        ValueError: If two column names normalize to the same name.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    for position, label in enumerate(df.columns):
        if not isinstance(label, str):
            raise TypeError(
                f"Column name at position {position} must be a string; "
                f"got {type(label).__name__}."
            )

    normalized_names: list[str] = []
    seen: dict[str, int] = {}
    for position, label in enumerate(df.columns):
        normalized = re.sub(r"\s+", "_", label.strip().lower())
        if normalized in seen:
            raise ValueError(
                f"Duplicate normalized column name {normalized!r} "
                f"at positions {seen[normalized]} and {position}."
            )
        normalized_names.append(normalized)
        seen[normalized] = position

    result = df.copy(deep=True)
    if normalized_names:
        result.columns = pd.Index(normalized_names, name=df.columns.name)
    return result
