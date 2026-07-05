"""
DataLoader - Handles reading/writing CSV and managing the in-memory dataset.
"""

import os
import pandas as pd
from typing import Optional

from models.song import Song
from core.exceptions import FileOperationError, DatasetNotLoadedError
from core.constants import NUMERIC_COLUMNS


class DataLoader:
    """
    Manages the dataset lifecycle:
    - Load from CSV
    - Maintain in-memory DataFrame
    - Append new songs
    - Provide data access to other services
    """

    def __init__(self, file_path: str):
        """
        Initialize the DataLoader with a file path.

        Args:
            file_path: Path to the CSV file
        """
        self.file_path = file_path
        self._df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """
        Load the dataset from CSV file.

        Returns:
            Loaded DataFrame

        Raises:
            FileOperationError: If file cannot be read
        """
        try:
            if not os.path.exists(self.file_path):
                # Try to create an empty dataset with proper columns
                self._df = self._create_empty_dataset()
                return self._df

            self._df = pd.read_csv(self.file_path)

            # Ensure proper data types
            self._df = self._clean_dtypes(self._df)

            return self._df

        except Exception as e:
            raise FileOperationError(f"Failed to load dataset: {str(e)}")

    def _create_empty_dataset(self) -> pd.DataFrame:
        """Create an empty DataFrame with the required schema."""
        columns = [
            'track_id', 'artists', 'album_name', 'track_name', 'popularity',
            'duration_ms', 'explicit', 'danceability', 'energy', 'key',
            'loudness', 'mode', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence', 'tempo',
            'time_signature', 'track_genre'
        ]
        return pd.DataFrame(columns=columns)

    def _clean_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure proper data types for all columns."""
        df = df.copy()

        # Convert numeric columns
        for col in NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convert explicit to boolean
        if 'explicit' in df.columns:
            df['explicit'] = df['explicit'].astype(bool)

        return df

    def get_data(self) -> pd.DataFrame:
        """
        Get the current in-memory DataFrame.

        Returns:
            Current DataFrame

        Raises:
            DatasetNotLoadedError: If dataset hasn't been loaded yet
        """
        if self._df is None:
            raise DatasetNotLoadedError("Dataset not loaded. Call load_data() first.")
        return self._df

    def set_data(self, df: pd.DataFrame) -> None:
        """
        Replace the current in-memory DataFrame.
        Used after cleaning operations.

        Args:
            df: New DataFrame to use
        """
        self._df = df.copy()

    def append_song(self, song: Song) -> None:
        """
        Append a new song to both the in-memory DataFrame and the CSV file.

        Args:
            song: Song instance to append

        Raises:
            FileOperationError: If append operation fails
        """
        try:
            # Ensure dataset is loaded
            if self._df is None:
                self.load_data()

            # Convert song to dictionary
            song_dict = song.to_dict()

            # Append to DataFrame
            new_row = pd.DataFrame([song_dict])
            self._df = pd.concat([self._df, new_row], ignore_index=True)

            # Append to CSV file
            file_exists = os.path.exists(self.file_path)

            # Write with proper mode
            if file_exists and os.path.getsize(self.file_path) > 0:
                # Append mode - write header only if file is empty
                new_row.to_csv(self.file_path, mode='a', header=False, index=False)
            else:
                # Create new file with header
                new_row.to_csv(self.file_path, mode='w', header=True, index=False)

        except Exception as e:
            raise FileOperationError(f"Failed to append song: {str(e)}")

    def get_missing_values_report(self) -> pd.DataFrame:
        """
        Generate a report of missing values in the dataset.

        Returns:
            DataFrame with missing counts and percentages
        """
        if self._df is None:
            raise DatasetNotLoadedError("Dataset not loaded. Call load_data() first.")

        missing_count = self._df.isnull().sum()
        total_rows = len(self._df)
        missing_percent = (missing_count / total_rows) * 100

        report = pd.DataFrame({
            'Column': missing_count.index,
            'Missing_Count': missing_count.values,
            'Missing_Percent': missing_percent.values
        })

        return report

    def save_data(self, file_path: Optional[str] = None) -> None:
        """
        Save the current DataFrame to CSV.

        Args:
            file_path: Optional custom path (defaults to original file_path)
        """
        if self._df is None:
            raise DatasetNotLoadedError("No data to save. Load or create dataset first.")

        save_path = file_path or self.file_path
        try:
            self._df.to_csv(save_path, index=False)
        except Exception as e:
            raise FileOperationError(f"Failed to save data: {str(e)}")