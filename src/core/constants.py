"""
Constants used across the project.
"""

# Numeric columns suitable for statistical operations
NUMERIC_COLUMNS = [
    'popularity', 'duration_ms', 'danceability', 'energy', 'key',
    'loudness', 'mode', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'
]

# Normalized audio features (all in [0,1] range)
NORMALIZED_AUDIO_COLUMNS = [
    'danceability', 'energy', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence'
]

# Columns that should be excluded from KNN imputation
NON_NUMERIC_COLUMNS = ['track_id', 'artists', 'album_name', 'track_name', 'track_genre']

# Columns that should be preserved as-is during cleaning
IDENTITY_COLUMNS = ['track_id', 'artists', 'album_name', 'track_name', 'track_genre']

# Default KNN parameters
DEFAULT_KNN_NEIGHBORS = 5

# Z-Score threshold for outlier detection
ZSCORE_THRESHOLD = 3.0

# IQR multiplier
IQR_MULTIPLIER = 1.5