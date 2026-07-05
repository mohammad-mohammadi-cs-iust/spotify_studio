"""
Custom exceptions for the Spotify Data Studio.
"""


class SpotifyStudioError(Exception):
    """Base exception for all project-specific errors."""
    pass


class DatasetNotLoadedError(SpotifyStudioError):
    """Raised when trying to access dataset before loading."""
    pass


class InvalidSongDataError(SpotifyStudioError):
    """Raised when song validation fails."""
    pass


class VisualizationError(SpotifyStudioError):
    """Raised when a visualization operation fails."""
    pass


class ModelNotTrainedError(SpotifyStudioError):
    """Raised when trying to use an untrained ML model."""
    pass


class CleanerError(SpotifyStudioError):
    """Raised when data cleaning operation fails."""
    pass


class FileOperationError(SpotifyStudioError):
    """Raised when file operations fail."""
    pass