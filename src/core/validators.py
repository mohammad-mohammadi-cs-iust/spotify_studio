"""
Validation utilities for data integrity.
"""

from typing import Any, Union
import pandas as pd


def validate_numeric_range(value: Union[int, float], min_val: float, max_val: float, field_name: str) -> None:
    """
    Validate that a numeric value falls within a specified range.

    Raises ValueError if validation fails.
    """
    if not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number, got {type(value).__name__}")
    if not (min_val <= value <= max_val):
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}, got {value}")


def validate_positive(value: Union[int, float], field_name: str) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{field_name} must be positive, got {value}")


def validate_non_empty_string(value: str, field_name: str) -> None:
    """Validate that a string is non-empty."""
    if not value or not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")


def validate_dataframe_columns(df: pd.DataFrame, required_columns: list) -> None:
    """Validate that a DataFrame contains all required columns."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def is_numeric_column(df: pd.DataFrame, col: str) -> bool:
    """Check if a column is numeric (int or float)."""
    return pd.api.types.is_numeric_dtype(df[col])