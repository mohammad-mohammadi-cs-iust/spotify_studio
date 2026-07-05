"""
Outlier handling strategies.
Using polymorphism with BaseOutlierHandler abstract class.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
import numpy as np

from core.constants import NUMERIC_COLUMNS, IQR_MULTIPLIER, ZSCORE_THRESHOLD
from core.exceptions import CleanerError


class BaseOutlierHandler(ABC):
    """
    Abstract base class for outlier handling strategies.
    All concrete handlers must implement the handle method.
    """

    @abstractmethod
    def handle(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Detect and handle outliers in the DataFrame.

        Args:
            df: Input DataFrame
            columns: List of columns to process (None = all numeric columns)

        Returns:
            DataFrame with outliers handled
        """
        pass


class IQROutlierHandler(BaseOutlierHandler):
    """
    Detect outliers using Inter-Quartile Range (IQR) method.
    Outliers are clipped to [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    """

    def __init__(self, multiplier: float = IQR_MULTIPLIER):
        self.multiplier = multiplier

    def handle(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        result = df.copy()

        if columns is None:
            columns = [col for col in NUMERIC_COLUMNS if
                       col in result.columns and pd.api.types.is_numeric_dtype(result[col])]
        else:
            columns = [col for col in columns if col in result.columns and pd.api.types.is_numeric_dtype(result[col])]

        for col in columns:
            if result[col].isnull().all():
                continue

            Q1 = result[col].quantile(0.25)
            Q3 = result[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - self.multiplier * IQR
            upper_bound = Q3 + self.multiplier * IQR

            # Clip outliers to bounds
            result[col] = result[col].clip(lower=lower_bound, upper=upper_bound)

        return result


class ZScoreOutlierHandler(BaseOutlierHandler):
    """
    Detect outliers using Z-Score method.
    Values with |z| > threshold are replaced with column median.
    """

    def __init__(self, threshold: float = ZSCORE_THRESHOLD):
        self.threshold = threshold

    def handle(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        result = df.copy()

        if columns is None:
            columns = [col for col in NUMERIC_COLUMNS if
                       col in result.columns and pd.api.types.is_numeric_dtype(result[col])]
        else:
            columns = [col for col in columns if col in result.columns and pd.api.types.is_numeric_dtype(result[col])]

        for col in columns:
            if result[col].isnull().all():
                continue

            mean_val = result[col].mean()
            std_val = result[col].std()

            # If std is 0, skip (all values are identical)
            if std_val == 0:
                continue

            # Calculate Z-scores
            z_scores = np.abs((result[col] - mean_val) / std_val)

            # Replace outliers with median
            median_val = result[col].median()
            mask = z_scores > self.threshold
            result.loc[mask, col] = median_val

        return result