import pandas as pd


def remove_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove identical rows without modifying the input DataFrame."""
    return df.drop_duplicates().reset_index(drop=True)