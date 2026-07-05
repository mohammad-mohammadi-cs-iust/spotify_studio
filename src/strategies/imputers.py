"""
Imputation strategies for handling missing values.
Using polymorphism with BaseImputer abstract class.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer as SklearnKNNImputer

from core.constants import NUMERIC_COLUMNS, IDENTITY_COLUMNS
from core.exceptions import CleanerError


class BaseImputer(ABC):
    """
    Abstract base class for imputation strategies.
    All concrete imputers must implement the impute method.
    """

    @abstractmethod
    def impute(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Impute missing values in the DataFrame.

        Args:
            df: Input DataFrame
            columns: List of columns to impute (None = all numeric columns)

        Returns:
            DataFrame with missing values imputed
        """
        pass


class MeanImputer(BaseImputer):
    """Impute missing values with column mean."""

    def impute(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        result = df.copy()

        # If no columns specified, use all numeric columns
        if columns is None:
            columns = [col for col in NUMERIC_COLUMNS if col in result.columns]
        else:
            # Filter to only numeric columns that exist
            columns = [col for col in columns if col in result.columns and pd.api.types.is_numeric_dtype(result[col])]

        for col in columns:
            if result[col].isnull().any():
                mean_val = result[col].mean()
                if pd.isna(mean_val):
                    mean_val = 0.0
                result[col].fillna(mean_val, inplace=True)

        return result


class MedianImputer(BaseImputer):
    """Impute missing values with column median."""

    def impute(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        result = df.copy()

        if columns is None:
            columns = [col for col in NUMERIC_COLUMNS if col in result.columns]
        else:
            columns = [col for col in columns if col in result.columns and pd.api.types.is_numeric_dtype(result[col])]

        for col in columns:
            if result[col].isnull().any():
                median_val = result[col].median()
                if pd.isna(median_val):
                    median_val = 0.0
                result[col].fillna(median_val, inplace=True)

        return result


class KNNValueImputer(BaseImputer):
    """
    Impute missing values using K-Nearest Neighbors.
    Only applied to numeric columns.
    """

    def __init__(self, n_neighbors: int = 5):
        self.n_neighbors = n_neighbors

    def impute(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        result = df.copy()

        # Determine which columns to impute
        if columns is None:
            impute_cols = [col for col in NUMERIC_COLUMNS if
                           col in result.columns and pd.api.types.is_numeric_dtype(result[col])]
        else:
            impute_cols = [col for col in columns if
                           col in result.columns and pd.api.types.is_numeric_dtype(result[col])]

        if not impute_cols:
            return result

        # Check if any missing values exist in these columns
        if not result[impute_cols].isnull().any().any():
            return result

        # Create a copy of only the numeric columns for KNN
        numeric_data = result[impute_cols].copy()

        try:
            # Scale the data for better KNN performance
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data)

            # Apply KNN imputation
            knn_imputer = SklearnKNNImputer(n_neighbors=self.n_neighbors)
            imputed_scaled = knn_imputer.fit_transform(scaled_data)

            # Inverse transform back to original scale
            imputed_data = scaler.inverse_transform(imputed_scaled)

            # Update the result DataFrame
            for i, col in enumerate(impute_cols):
                result[col] = imputed_data[:, i]

        except Exception as e:
            raise CleanerError(f"KNN imputation failed: {str(e)}")

        return result