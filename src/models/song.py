"""
Song Model - Encapsulation and Validation of a single track.
"""

from typing import Optional, Any
from datetime import datetime


class Song:
    """
    Represents a single song/track from Spotify dataset.
    All attributes are validated through property setters.
    """

    # Required fields from the dataset
    _fields = [
        'track_id', 'artists', 'album_name', 'track_name', 'popularity',
        'duration_ms', 'explicit', 'danceability', 'energy', 'key',
        'loudness', 'mode', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo',
        'time_signature', 'track_genre'
    ]

    # Numeric fields that need range validation
    _numeric_ranges = {
        'popularity': (0, 100),
        'danceability': (0, 1),
        'energy': (0, 1),
        'speechiness': (0, 1),
        'acousticness': (0, 1),
        'instrumentalness': (0, 1),
        'liveness': (0, 1),
        'valence': (0, 1),
        'duration_ms': (1, float('inf')),
        'tempo': (0, float('inf')),
        'loudness': (-float('inf'), float('inf')),
        'key': (-1, 11),  # -1 for unknown, 0-11 for pitch
        'mode': (0, 1),
        'time_signature': (0, 11),
    }

    def __init__(
            self,
            track_id: str,
            artists: str,
            album_name: str,
            track_name: str,
            popularity: int,
            duration_ms: int,
            explicit: bool,
            danceability: float,
            energy: float,
            key: int,
            loudness: float,
            mode: int,
            speechiness: float,
            acousticness: float,
            instrumentalness: float,
            liveness: float,
            valence: float,
            tempo: float,
            time_signature: int,
            track_genre: str
    ):
        self.track_id = track_id
        self.artists = artists
        self.album_name = album_name
        self.track_name = track_name
        self.popularity = popularity
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.time_signature = time_signature
        self.track_genre = track_genre

    @staticmethod
    def _validate_range(value: Any, min_val: float, max_val: float, field_name: str) -> None:
        """Validate that value is within the specified range."""
        if not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} must be a number, got {type(value).__name__}")
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"{field_name} must be between {min_val} and {max_val}, got {value}"
            )

    @property
    def track_id(self) -> str:
        return self._track_id

    @track_id.setter
    def track_id(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("track_id must be a non-empty string")
        self._track_id = value.strip()

    @property
    def artists(self) -> str:
        return self._artists

    @artists.setter
    def artists(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("artists must be a non-empty string")
        self._artists = value.strip()

    @property
    def album_name(self) -> str:
        return self._album_name

    @album_name.setter
    def album_name(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("album_name must be a non-empty string")
        self._album_name = value.strip()

    @property
    def track_name(self) -> str:
        return self._track_name

    @track_name.setter
    def track_name(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("track_name must be a non-empty string")
        self._track_name = value.strip()

    @property
    def popularity(self) -> int:
        return self._popularity

    @popularity.setter
    def popularity(self, value: int) -> None:
        self._validate_range(value, 0, 100, "popularity")
        self._popularity = int(value)

    @property
    def duration_ms(self) -> int:
        return self._duration_ms

    @duration_ms.setter
    def duration_ms(self, value: int) -> None:
        self._validate_range(value, 1, float('inf'), "duration_ms")
        self._duration_ms = int(value)

    @property
    def explicit(self) -> bool:
        return self._explicit

    @explicit.setter
    def explicit(self, value: bool) -> None:
        if isinstance(value, str):
            value = value.lower() in ('true', '1', 'yes', 'y')
        if not isinstance(value, bool):
            raise ValueError("explicit must be a boolean value")
        self._explicit = value

    @property
    def danceability(self) -> float:
        return self._danceability

    @danceability.setter
    def danceability(self, value: float) -> None:
        self._validate_range(value, 0, 1, "danceability")
        self._danceability = float(value)

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, value: float) -> None:
        self._validate_range(value, 0, 1, "energy")
        self._energy = float(value)

    @property
    def key(self) -> int:
        return self._key

    @key.setter
    def key(self, value: int) -> None:
        self._validate_range(value, -1, 11, "key")
        self._key = int(value)

    @property
    def loudness(self) -> float:
        return self._loudness

    @loudness.setter
    def loudness(self, value: float) -> None:
        self._loudness = float(value)

    @property
    def mode(self) -> int:
        return self._mode

    @mode.setter
    def mode(self, value: int) -> None:
        self._validate_range(value, 0, 1, "mode")
        self._mode = int(value)

    @property
    def speechiness(self) -> float:
        return self._speechiness

    @speechiness.setter
    def speechiness(self, value: float) -> None:
        self._validate_range(value, 0, 1, "speechiness")
        self._speechiness = float(value)

    @property
    def acousticness(self) -> float:
        return self._acousticness

    @acousticness.setter
    def acousticness(self, value: float) -> None:
        self._validate_range(value, 0, 1, "acousticness")
        self._acousticness = float(value)

    @property
    def instrumentalness(self) -> float:
        return self._instrumentalness

    @instrumentalness.setter
    def instrumentalness(self, value: float) -> None:
        self._validate_range(value, 0, 1, "instrumentalness")
        self._instrumentalness = float(value)

    @property
    def liveness(self) -> float:
        return self._liveness

    @liveness.setter
    def liveness(self, value: float) -> None:
        self._validate_range(value, 0, 1, "liveness")
        self._liveness = float(value)

    @property
    def valence(self) -> float:
        return self._valence

    @valence.setter
    def valence(self, value: float) -> None:
        self._validate_range(value, 0, 1, "valence")
        self._valence = float(value)

    @property
    def tempo(self) -> float:
        return self._tempo

    @tempo.setter
    def tempo(self, value: float) -> None:
        self._validate_range(value, 0, float('inf'), "tempo")
        self._tempo = float(value)

    @property
    def time_signature(self) -> int:
        return self._time_signature

    @time_signature.setter
    def time_signature(self, value: int) -> None:
        self._validate_range(value, 0, 11, "time_signature")
        self._time_signature = int(value)

    @property
    def track_genre(self) -> str:
        return self._track_genre

    @track_genre.setter
    def track_genre(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("track_genre must be a non-empty string")
        self._track_genre = value.strip()

    def to_dict(self) -> dict:
        """
        Convert the Song instance to a dictionary.
        This ensures correct order for CSV writing.
        """
        return {
            'track_id': self.track_id,
            'artists': self.artists,
            'album_name': self.album_name,
            'track_name': self.track_name,
            'popularity': self.popularity,
            'duration_ms': self.duration_ms,
            'explicit': self.explicit,
            'danceability': self.danceability,
            'energy': self.energy,
            'key': self.key,
            'loudness': self.loudness,
            'mode': self.mode,
            'speechiness': self.speechiness,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'liveness': self.liveness,
            'valence': self.valence,
            'tempo': self.tempo,
            'time_signature': self.time_signature,
            'track_genre': self.track_genre
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Song':
        """Create a Song instance from a dictionary."""
        # Handle boolean conversion for explicit
        explicit = data.get('explicit', False)
        if isinstance(explicit, str):
            explicit = explicit.lower() in ('true', '1', 'yes', 'y')

        return cls(
            track_id=data.get('track_id', ''),
            artists=data.get('artists', ''),
            album_name=data.get('album_name', ''),
            track_name=data.get('track_name', ''),
            popularity=int(data.get('popularity', 0)),
            duration_ms=int(data.get('duration_ms', 0)),
            explicit=explicit,
            danceability=float(data.get('danceability', 0.0)),
            energy=float(data.get('energy', 0.0)),
            key=int(data.get('key', 0)),
            loudness=float(data.get('loudness', 0.0)),
            mode=int(data.get('mode', 0)),
            speechiness=float(data.get('speechiness', 0.0)),
            acousticness=float(data.get('acousticness', 0.0)),
            instrumentalness=float(data.get('instrumentalness', 0.0)),
            liveness=float(data.get('liveness', 0.0)),
            valence=float(data.get('valence', 0.0)),
            tempo=float(data.get('tempo', 0.0)),
            time_signature=int(data.get('time_signature', 0)),
            track_genre=data.get('track_genre', '')
        )

    def __repr__(self) -> str:
        return f"Song(track_name='{self.track_name}', artists='{self.artists}', popularity={self.popularity})"