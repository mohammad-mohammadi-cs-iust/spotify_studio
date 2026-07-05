"""
DataCleaner - Orchestrator for cleaning operations.
Delegates to strategy classes for specific cleaning algorithms.
"""

import pandas as pd
from typing import Optional, List

from core.exceptions import CleanerError
from strategies import BaseImputer, BaseOutlierHandler
from core.constants import NUMERIC_COLUMNS


class DataCleaner:
    """
    Orchestrates data cleaning operations.
    Uses strategy pattern for imputation and outlier handling.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the cleaner with a DataFrame.

        Args:
            df: Input DataFrame to clean
        """
        self._original_df = df.copy()
        self._df = df.copy()

    def get_data(self) -> pd.DataFrame:
        """Return the current cleaned DataFrame."""
        return self._df

    def reset(self) -> None:
        """Reset to the original DataFrame."""
        self._df = self._original_df.copy()

    def missing_report(self) -> pd.DataFrame:
        """
        Generate a report of missing values.

        Returns:
            DataFrame with missing count and percentage per column
        """
        missing_count = self._df.isnull().sum()
        total_rows = len(self._df)
        missing_percent = (missing_count / total_rows) * 100

        report = pd.DataFrame({
            'Column': missing_count.index,
            'Missing_Count': missing_count.values,
            'Missing_Percent': missing_percent.values
        })
        return report

    def clean_missing(
            self,
            imputer: BaseImputer,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Clean missing values using the provided imputation strategy.

        Args:
            imputer: Imputation strategy instance
            columns: Columns to impute (None = all numeric)

        Returns:
            Cleaned DataFrame

        Raises:
            CleanerError: If imputation fails
        """
        try:
            self._df = imputer.impute(self._df, columns)
            return self._df
        except Exception as e:
            raise CleanerError(f"Missing value cleaning failed: {str(e)}")

    def handle_outliers(
            self,
            handler: BaseOutlierHandler,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Handle outliers using the provided strategy.

        Args:
            handler: Outlier handling strategy instance
            columns: Columns to process (None = all numeric)

        Returns:
            Cleaned DataFrame

        Raises:
            CleanerError: If outlier handling fails
        """
        try:
            self._df = handler.handle(self._df, columns)
            return self._df
        except Exception as e:
            raise CleanerError(f"Outlier handling failed: {str(e)}")

    def get_before_after(self, column: str) -> tuple:
        """
        Get original and cleaned data for a column (for visualization).

        Args:
            column: Column name

        Returns:
            Tuple of (original_series, cleaned_series)
        """
        if column not in self._original_df.columns:
            raise CleanerError(f"Column '{column}' not found in data")
        return self._original_df[column], self._df[column]