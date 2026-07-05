"""
Utility functions for DataFrame operations.
"""

import pandas as pd
from typing import List, Optional

from ..core.constants import NUMERIC_COLUMNS


def ensure_numeric_columns(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Ensure that specified columns are numeric type.
    Coerces invalid values to NaN.

    Args:
        df: Input DataFrame
        columns: Columns to convert (None = all NUMERIC_COLUMNS)

    Returns:
        DataFrame with numeric columns
    """
    result = df.copy()

    if columns is None:
        columns = [col for col in NUMERIC_COLUMNS if col in result.columns]

    for col in columns:
        result[col] = pd.to_numeric(result[col], errors='coerce')

    return result


def get_numeric_subset(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Get a subset of the DataFrame containing only numeric columns.

    Args:
        df: Input DataFrame
        columns: Specific columns to include (None = all numeric)

    Returns:
        DataFrame with only numeric columns
    """
    if columns is None:
        columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    else:
        columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]

    return df[columns].copy()


def get_missing_count(df: pd.DataFrame) -> pd.Series:
    """Get missing value count for each column."""
    return df.isnull().sum()