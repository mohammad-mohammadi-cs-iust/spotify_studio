"""
InputService - Handles interactive user input for adding new songs.
"""

from typing import Optional
from models.song import Song
from core.exceptions import InvalidSongDataError


class InputService:
    """
    Provides interactive input prompts for creating Song objects.
    Handles validation and error recovery.
    """

    @staticmethod
    def get_boolean_input(prompt: str, default: Optional[bool] = None) -> bool:
        """
        Get a boolean input from the user with yes/no prompts.

        Args:
            prompt: The prompt to display
            default: Default value if user presses enter

        Returns:
            Boolean value
        """
        while True:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ('y', 'yes', 'true', '1'):
                return True
            if response in ('n', 'no', 'false', '0'):
                return False
            if response == '' and default is not None:
                return default
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    @staticmethod
    def get_float_input(prompt: str, min_val: Optional[float] = None,
                        max_val: Optional[float] = None, default: Optional[float] = None) -> float:
        """
        Get a float input with optional range validation.

        Args:
            prompt: The prompt to display
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            default: Default value if user presses enter

        Returns:
            Float value
        """
        while True:
            response = input(prompt).strip()

            if response == '' and default is not None:
                return default

            try:
                value = float(response)
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def get_int_input(prompt: str, min_val: Optional[int] = None,
                      max_val: Optional[int] = None, default: Optional[int] = None) -> int:
        """
        Get an integer input with optional range validation.

        Args:
            prompt: The prompt to display
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            default: Default value if user presses enter

        Returns:
            Integer value
        """
        while True:
            response = input(prompt).strip()

            if response == '' and default is not None:
                return default

            try:
                value = int(response)
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def get_string_input(prompt: str, required: bool = True, default: Optional[str] = None) -> str:
        """
        Get a string input from the user.

        Args:
            prompt: The prompt to display
            required: If True, the string cannot be empty
            default: Default value if user presses enter

        Returns:
            String value
        """
        while True:
            response = input(prompt).strip()

            if response == '' and default is not None:
                return default

            if required and not response:
                print("This field is required.")
                continue

            return response

    @classmethod
    def collect_song_from_user(cls) -> Song:
        """
        Collect all song data from the user through interactive prompts.

        Returns:
            Song instance with validated data

        Raises:
            InvalidSongDataError: If validation fails
        """
        print("\n" + "=" * 50)
        print("ADD NEW SONG - INTERACTIVE INPUT")
        print("=" * 50)
        print("Please enter the song details below:")
        print()

        try:
            track_id = cls.get_string_input("Track ID: ", required=True)
            artists = cls.get_string_input("Artist(s): ", required=True)
            album_name = cls.get_string_input("Album Name: ", required=True)
            track_name = cls.get_string_input("Track Name: ", required=True)
            popularity = cls.get_int_input("Popularity (0-100): ", min_val=0, max_val=100)
            duration_ms = cls.get_int_input("Duration (ms) - must be > 0: ", min_val=1)
            explicit = cls.get_boolean_input("Is Explicit?", default=False)
            danceability = cls.get_float_input("Danceability (0-1): ", min_val=0, max_val=1)
            energy = cls.get_float_input("Energy (0-1): ", min_val=0, max_val=1)
            key = cls.get_int_input("Key (-1 to 11): ", min_val=-1, max_val=11)
            loudness = cls.get_float_input("Loudness (dB): ")
            mode = cls.get_int_input("Mode (0 or 1): ", min_val=0, max_val=1)
            speechiness = cls.get_float_input("Speechiness (0-1): ", min_val=0, max_val=1)
            acousticness = cls.get_float_input("Acousticness (0-1): ", min_val=0, max_val=1)
            instrumentalness = cls.get_float_input("Instrumentalness (0-1): ", min_val=0, max_val=1)
            liveness = cls.get_float_input("Liveness (0-1): ", min_val=0, max_val=1)
            valence = cls.get_float_input("Valence (0-1): ", min_val=0, max_val=1)
            tempo = cls.get_float_input("Tempo (BPM) - must be > 0: ", min_val=0)
            time_signature = cls.get_int_input("Time Signature (0-11): ", min_val=0, max_val=11)
            track_genre = cls.get_string_input("Genre: ", required=True)

            return Song(
                track_id=track_id,
                artists=artists,
                album_name=album_name,
                track_name=track_name,
                popularity=popularity,
                duration_ms=duration_ms,
                explicit=explicit,
                danceability=danceability,
                energy=energy,
                key=key,
                loudness=loudness,
                mode=mode,
                speechiness=speechiness,
                acousticness=acousticness,
                instrumentalness=instrumentalness,
                liveness=liveness,
                valence=valence,
                tempo=tempo,
                time_signature=time_signature,
                track_genre=track_genre
            )

        except ValueError as e:
            raise InvalidSongDataError(f"Invalid input: {str(e)}")