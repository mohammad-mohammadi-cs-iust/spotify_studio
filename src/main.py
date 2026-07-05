#!/usr/bin/env python3
"""
Spotify Data Studio - Main Entry Point
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.dashboard import SpotifyStudioCLI


def main():
    """Main entry point for the application."""
    # Define the default data path
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data',
        'spotify_tracks.csv'
    )

    # If data file doesn't exist, try to create an empty one
    if not os.path.exists(data_path):
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        # Create an empty CSV with headers
        import pandas as pd
        empty_df = pd.DataFrame(columns=[
            'track_id', 'artists', 'album_name', 'track_name', 'popularity',
            'duration_ms', 'explicit', 'danceability', 'energy', 'key',
            'loudness', 'mode', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence', 'tempo',
            'time_signature', 'track_genre'
        ])
        empty_df.to_csv(data_path, index=False)
        print(f"📁 Created empty dataset at: {data_path}")
        print("   Please replace it with your actual Spotify dataset.")

    # Run the CLI
    cli = SpotifyStudioCLI(data_path)
    cli.run()


if __name__ == "__main__":
    main()