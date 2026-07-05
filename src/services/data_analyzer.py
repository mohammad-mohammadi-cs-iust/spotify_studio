"""
DataAnalyzer - Statistical analysis and insights generation.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Tuple, Dict, Any

from core.constants import NUMERIC_COLUMNS, NORMALIZED_AUDIO_COLUMNS
from core.exceptions import DatasetNotLoadedError


class DataAnalyzer:
    """
    Provides statistical analysis and insights from the dataset.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the analyzer with a DataFrame.

        Args:
            df: Input DataFrame
        """
        self.df = df

    def dataset_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the dataset.

        Returns:
            Dictionary with dataset statistics
        """
        summary = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage': self.df.memory_usage(deep=True).sum() / (1024 * 1024),  # MB
            'numeric_columns': [col for col in self.df.columns if pd.api.types.is_numeric_dtype(self.df[col])],
            'categorical_columns': [col for col in self.df.columns if pd.api.types.is_object_dtype(self.df[col])],
            'missing_count': self.df.isnull().sum().to_dict(),
        }
        return summary

    def descriptive_stats(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Get descriptive statistics for numeric columns.

        Args:
            columns: Specific columns to analyze (None = all numeric)

        Returns:
            DataFrame with descriptive statistics
        """
        if columns is None:
            columns = [col for col in NUMERIC_COLUMNS if col in self.df.columns]
        else:
            columns = [col for col in columns if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col])]

        return self.df[columns].describe()

    def genre_popularity_summary(self, top_n: int = 10) -> pd.DataFrame:
        """
        Calculate average popularity per genre.

        Args:
            top_n: Number of top genres to return

        Returns:
            DataFrame with genre popularity statistics
        """
        if 'track_genre' not in self.df.columns:
            raise DatasetNotLoadedError("Dataset missing 'track_genre' column")

        genre_stats = self.df.groupby('track_genre').agg({
            'popularity': ['mean', 'count', 'std']
        }).reset_index()

        genre_stats.columns = ['Genre', 'Avg_Popularity', 'Track_Count', 'Std_Dev']
        genre_stats = genre_stats.sort_values('Avg_Popularity', ascending=False)

        return genre_stats.head(top_n)

    def genre_feature_summary(self, top_n: int = 10) -> pd.DataFrame:
        """
        Calculate average audio features per genre.

        Args:
            top_n: Number of top genres to return

        Returns:
            DataFrame with feature averages per genre
        """
        if 'track_genre' not in self.df.columns:
            raise DatasetNotLoadedError("Dataset missing 'track_genre' column")

        feature_cols = [col for col in NORMALIZED_AUDIO_COLUMNS if col in self.df.columns]
        if not feature_cols:
            return pd.DataFrame()

        genre_features = self.df.groupby('track_genre')[feature_cols].mean().reset_index()
        return genre_features.head(top_n)

    def correlation_matrix(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calculate correlation matrix for numeric columns.

        Args:
            columns: Specific columns to analyze (None = all numeric)

        Returns:
            Correlation matrix DataFrame
        """
        if columns is None:
            columns = [col for col in NUMERIC_COLUMNS if
                       col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col])]
        else:
            columns = [col for col in columns if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col])]

        return self.df[columns].corr()

    def top_tracks_by_popularity(self, n: int = 10) -> pd.DataFrame:
        """
        Get the top N tracks by popularity.

        Args:
            n: Number of top tracks to return

        Returns:
            DataFrame with top tracks
        """
        if 'popularity' not in self.df.columns:
            raise DatasetNotLoadedError("Dataset missing 'popularity' column")

        return self.df.nlargest(n, 'popularity')[['track_name', 'artists', 'popularity', 'track_genre']]

    def explicit_analysis(self) -> Dict[str, Any]:
        """
        Analyze explicit vs non-explicit tracks.

        Returns:
            Dictionary with comparison metrics
        """
        if 'explicit' not in self.df.columns:
            raise DatasetNotLoadedError("Dataset missing 'explicit' column")

        explicit_group = self.df.groupby('explicit')

        return {
            'count': explicit_group.size().to_dict(),
            'avg_popularity': explicit_group['popularity'].mean().to_dict(),
            'avg_features': explicit_group[NORMALIZED_AUDIO_COLUMNS].mean().to_dict() if all(
                col in self.df.columns for col in NORMALIZED_AUDIO_COLUMNS
            ) else {}
        }