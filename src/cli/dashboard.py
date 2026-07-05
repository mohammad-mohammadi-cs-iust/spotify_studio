"""
CLI Dashboard - Main interactive menu for the Spotify Data Studio.
"""

import os
import sys
import pandas as pd
from typing import Optional

from services import DataLoader, DataCleaner, DataAnalyzer, DataVisualizer, InputService
from strategies import MeanImputer, MedianImputer, KNNValueImputer
from strategies import IQROutlierHandler, ZScoreOutlierHandler
from core.exceptions import SpotifyStudioError, DatasetNotLoadedError
from core.constants import NUMERIC_COLUMNS


class SpotifyStudioCLI:
    """
    Main interactive command-line interface for the Spotify Data Studio.
    """

    def __init__(self, data_path: str):
        """
        Initialize the CLI with the data file path.

        Args:
            data_path: Path to the CSV data file
        """
        self.data_path = data_path
        self.loader = DataLoader(data_path)
        self.cleaner: Optional[DataCleaner] = None
        self.analyzer: Optional[DataAnalyzer] = None
        self.visualizer: Optional[DataVisualizer] = None
        self._running = True

        # Store original data for before/after comparisons
        self._original_df: Optional[pd.DataFrame] = None

    def _ensure_data_loaded(self) -> bool:
        """Ensure dataset is loaded. Returns True if successful."""
        try:
            if self.loader._df is None:
                self.loader.load_data()
                # Initialize analyzer and visualizer
                df = self.loader.get_data()
                self.analyzer = DataAnalyzer(df)
                self.visualizer = DataVisualizer(df)
                self.cleaner = DataCleaner(df)
                self._original_df = df.copy()
                print(f"\n✅ Dataset loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
                return True
            return True
        except Exception as e:
            print(f"\n❌ Error loading dataset: {str(e)}")
            return False

    def _refresh_services(self):
        """Refresh analyzer, visualizer, and cleaner with current data."""
        try:
            df = self.loader.get_data()
            self.analyzer = DataAnalyzer(df)
            self.visualizer = DataVisualizer(df)
            self.cleaner = DataCleaner(df)
        except DatasetNotLoadedError:
            pass

    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("  🎵 SPOTIFY DATA STUDIO & MANAGEMENT SYSTEM  🎵")
        print("=" * 60)
        print("  1. Load Dataset & View Missing Values Report")
        print("  2. Clean Missing Values (Mean / Median / KNN)")
        print("  3. Handle Outliers (IQR / Z-Score)")
        print("  4. Add a New Song to the Dataset")
        print("  5. Calculate Genre Insights & Correlation Matrix")
        print("  6. Generate Advanced Visualizations")
        print("  7. Show Dataset Summary")
        print("  8. Exit")
        print("=" * 60)

    def _load_dataset_menu(self):
        """Handle option 1: Load dataset and show missing values report."""
        try:
            df = self.loader.load_data()
            self.analyzer = DataAnalyzer(df)
            self.visualizer = DataVisualizer(df)
            self.cleaner = DataCleaner(df)
            self._original_df = df.copy()

            print(f"\n✅ Dataset loaded successfully!")
            print(f"   Total rows: {len(df)}")
            print(f"   Total columns: {len(df.columns)}")

            # Missing values report
            report = self.loader.get_missing_values_report()
            missing_total = report['Missing_Count'].sum()

            print("\n📊 Missing Values Report:")
            print("-" * 50)
            if missing_total == 0:
                print("   ✅ No missing values found!")
            else:
                for _, row in report.iterrows():
                    if row['Missing_Count'] > 0:
                        print(f"   {row['Column']:<20} {row['Missing_Count']:>8} ({row['Missing_Percent']:.2f}%)")
                print(f"\n   Total missing values: {missing_total}")

            # Try to plot missing values
            try:
                plot_path = self.visualizer.plot_missing_values_bar(report)
                print(f"\n📈 Missing values plot saved to: {plot_path}")
            except Exception as e:
                print(f"\n⚠️ Could not generate missing values plot: {str(e)}")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

    def _clean_missing_menu(self):
        """Handle option 2: Clean missing values."""
        if not self._ensure_data_loaded():
            return

        print("\n" + "-" * 40)
        print("  CLEAN MISSING VALUES")
        print("-" * 40)
        print("Choose imputation method:")
        print("  1. Mean Imputation")
        print("  2. Median Imputation")
        print("  3. KNN Imputation (using sklearn)")
        print("  4. Cancel")

        choice = input("\nEnter your choice (1-4): ").strip()

        try:
            if choice == '1':
                imputer = MeanImputer()
                method = "Mean"
            elif choice == '2':
                imputer = MedianImputer()
                method = "Median"
            elif choice == '3':
                try:
                    n_neighbors = int(input("Number of neighbors (default 5): ").strip() or "5")
                    imputer = KNNValueImputer(n_neighbors=n_neighbors)
                    method = f"KNN (k={n_neighbors})"
                except ValueError:
                    print("Invalid input. Using default k=5.")
                    imputer = KNNValueImputer(n_neighbors=5)
                    method = "KNN (k=5)"
            elif choice == '4':
                print("Cancelled.")
                return
            else:
                print("Invalid choice.")
                return

            print(f"\n⏳ Applying {method} imputation...")

            # Get current data and apply imputation
            df = self.loader.get_data()
            cleaner = DataCleaner(df)
            cleaned_df = cleaner.clean_missing(imputer)

            # Update the loader with cleaned data
            self.loader.set_data(cleaned_df)
            self._refresh_services()

            # Show updated missing report
            report = self.loader.get_missing_values_report()
            remaining = report['Missing_Count'].sum()

            print(f"\n✅ {method} imputation completed!")
            print(f"   Remaining missing values: {remaining}")

        except Exception as e:
            print(f"\n❌ Error during imputation: {str(e)}")

    def _handle_outliers_menu(self):
        """Handle option 3: Handle outliers."""
        if not self._ensure_data_loaded():
            return

        print("\n" + "-" * 40)
        print("  HANDLE OUTLIERS")
        print("-" * 40)
        print("Choose outlier handling method:")
        print("  1. IQR Method (clip to bounds)")
        print("  2. Z-Score Method (replace with median)")
        print("  3. Cancel")

        choice = input("\nEnter your choice (1-3): ").strip()

        try:
            if choice == '1':
                handler = IQROutlierHandler()
                method = "IQR"
            elif choice == '2':
                threshold = float(input("Z-Score threshold (default 3.0): ").strip() or "3.0")
                handler = ZScoreOutlierHandler(threshold=threshold)
                method = f"Z-Score (threshold={threshold})"
            elif choice == '3':
                print("Cancelled.")
                return
            else:
                print("Invalid choice.")
                return

            # Save original data for visualization
            original_df = self.loader.get_data().copy()

            print(f"\n⏳ Applying {method} outlier handling...")

            # Apply outlier handling
            df = self.loader.get_data()
            cleaner = DataCleaner(df)
            cleaned_df = cleaner.handle_outliers(handler)

            # Update the loader
            self.loader.set_data(cleaned_df)
            self._refresh_services()

            print(f"\n✅ {method} outlier handling completed!")

            # Offer to show boxplot comparison
            show_plot = input("\nShow boxplot comparison for a column? (y/n): ").strip().lower()
            if show_plot in ('y', 'yes'):
                print("\nAvailable numeric columns:")
                numeric_cols = [col for col in NUMERIC_COLUMNS if col in df.columns]
                for i, col in enumerate(numeric_cols, 1):
                    print(f"  {i}. {col}")

                col_choice = input("Enter column number (or name): ").strip()
                try:
                    idx = int(col_choice) - 1
                    if 0 <= idx < len(numeric_cols):
                        col_name = numeric_cols[idx]
                    else:
                        col_name = col_choice
                except ValueError:
                    col_name = col_choice

                if col_name in original_df.columns:
                    before_series = original_df[col_name]
                    after_series = cleaned_df[col_name]

                    try:
                        plot_path = self.visualizer.plot_boxplot_before_after(
                            before_series, after_series, col_name
                        )
                        print(f"\n📈 Boxplot comparison saved to: {plot_path}")
                    except Exception as e:
                        print(f"\n⚠️ Could not generate boxplot: {str(e)}")
                else:
                    print(f"Column '{col_name}' not found.")

        except Exception as e:
            print(f"\n❌ Error during outlier handling: {str(e)}")

    def _add_song_menu(self):
        """Handle option 4: Add a new song."""
        if not self._ensure_data_loaded():
            return

        print("\n" + "-" * 40)
        print("  ADD NEW SONG")
        print("-" * 40)
        print("Please enter the song details. You can skip optional fields by pressing Enter.")
        print()

        try:
            # Collect song data interactively
            song = InputService.collect_song_from_user()

            # Confirm before adding
            print("\n📝 Song details:")
            print(f"   Title: {song.track_name}")
            print(f"   Artist: {song.artists}")
            print(f"   Genre: {song.track_genre}")
            print(f"   Popularity: {song.popularity}")

            confirm = input("\nAdd this song to the dataset? (y/n): ").strip().lower()
            if confirm not in ('y', 'yes'):
                print("Cancelled.")
                return

            # Append the song
            self.loader.append_song(song)
            self._refresh_services()

            print(f"\n✅ Song '{song.track_name}' added successfully!")
            print(f"   Total tracks now: {len(self.loader.get_data())}")

        except Exception as e:
            print(f"\n❌ Error adding song: {str(e)}")

    def _analysis_menu(self):
        """Handle option 5: Calculate genre insights and correlation matrix."""
        if not self._ensure_data_loaded():
            return

        try:
            df = self.loader.get_data()

            print("\n" + "-" * 40)
            print("  GENRE INSIGHTS & CORRELATION")
            print("-" * 40)

            # Genre popularity summary
            print("\n📊 Top 10 Genres by Average Popularity:")
            print("-" * 50)
            genre_summary = self.analyzer.genre_popularity_summary(top_n=10)
            for _, row in genre_summary.iterrows():
                print(f"   {row['Genre']:<20} | Avg: {row['Avg_Popularity']:.1f} | Count: {row['Track_Count']}")

            # Feature summary
            print("\n📊 Genre Feature Averages (Top 5):")
            print("-" * 60)
            feature_summary = self.analyzer.genre_feature_summary(top_n=5)
            if not feature_summary.empty:
                print(feature_summary.to_string(index=False))

            # Correlation matrix
            print("\n📊 Correlation Matrix (Top 10 numeric columns):")
            print("-" * 50)
            corr_matrix = self.analyzer.correlation_matrix()
            if not corr_matrix.empty:
                # Show a compact view
                print(corr_matrix.round(2).to_string())

            # Option to save correlation plot
            save_plot = input("\nSave correlation heatmap? (y/n): ").strip().lower()
            if save_plot in ('y', 'yes'):
                try:
                    plot_path = self.visualizer.plot_correlation_heatmap()
                    print(f"\n📈 Correlation heatmap saved to: {plot_path}")
                except Exception as e:
                    print(f"\n⚠️ Could not generate heatmap: {str(e)}")

        except Exception as e:
            print(f"\n❌ Error during analysis: {str(e)}")

    def _visualization_menu(self):
        """Handle option 6: Generate advanced visualizations."""
        if not self._ensure_data_loaded():
            return

        print("\n" + "-" * 40)
        print("  ADVANCED VISUALIZATIONS")
        print("-" * 40)
        print("Choose visualization:")
        print("  1. Genre Popularity Bar Chart")
        print("  2. Correlation Heatmap")
        print("  3. Scatter Plot (choose features)")
        print("  4. Radar Chart (compare a genre)")
        print("  5. All Visualizations")
        print("  6. Cancel")

        choice = input("\nEnter your choice (1-6): ").strip()

        try:
            plot_paths = []

            if choice == '1':
                plot_path = self.visualizer.plot_genre_popularity_bar(top_n=10)
                print(f"\n📈 Genre popularity chart saved to: {plot_path}")

            elif choice == '2':
                plot_path = self.visualizer.plot_correlation_heatmap()
                print(f"\n📈 Correlation heatmap saved to: {plot_path}")

            elif choice == '3':
                # Get available numeric columns
                numeric_cols = [col for col in NUMERIC_COLUMNS if col in self.loader.get_data().columns]
                print("\nAvailable numeric columns:")
                for i, col in enumerate(numeric_cols, 1):
                    print(f"  {i}. {col}")

                x_col = input("X-axis column (name or number): ").strip()
                y_col = input("Y-axis column (name or number): ").strip()

                # Try to resolve by index
                try:
                    idx = int(x_col) - 1
                    if 0 <= idx < len(numeric_cols):
                        x_col = numeric_cols[idx]
                except ValueError:
                    pass

                try:
                    idx = int(y_col) - 1
                    if 0 <= idx < len(numeric_cols):
                        y_col = numeric_cols[idx]
                except ValueError:
                    pass

                if x_col not in self.loader.get_data().columns:
                    print(f"Column '{x_col}' not found.")
                    return
                if y_col not in self.loader.get_data().columns:
                    print(f"Column '{y_col}' not found.")
                    return

                # Ask for hue
                hue = input("Optional hue column (press Enter to skip): ").strip() or None

                plot_path = self.visualizer.plot_feature_scatter(x_col, y_col, hue)
                print(f"\n📈 Scatter plot saved to: {plot_path}")

            elif choice == '4':
                # Get available genres
                genres = self.loader.get_data()['track_genre'].unique().tolist()
                print("\nAvailable genres:")
                for i, g in enumerate(sorted(genres)[:20], 1):
                    print(f"  {i}. {g}")
                if len(genres) > 20:
                    print(f"  ... and {len(genres) - 20} more")

                genre_name = input("\nEnter genre name: ").strip()
                if genre_name not in genres:
                    print(f"Genre '{genre_name}' not found.")
                    return

                plot_path = self.visualizer.plot_radar_chart(genre_name)
                print(f"\n📈 Radar chart saved to: {plot_path}")

            elif choice == '5':
                print("\n⏳ Generating all visualizations...")

                # Genre popularity
                p1 = self.visualizer.plot_genre_popularity_bar(top_n=10)
                plot_paths.append(p1)
                print(f"✅ {p1}")

                # Correlation heatmap
                p2 = self.visualizer.plot_correlation_heatmap()
                plot_paths.append(p2)
                print(f"✅ {p2}")

                # Scatter: energy vs popularity
                p3 = self.visualizer.plot_feature_scatter('energy', 'popularity', hue='track_genre')
                plot_paths.append(p3)
                print(f"✅ {p3}")

                # Radar: pick a genre with enough data
                df = self.loader.get_data()
                genre_counts = df['track_genre'].value_counts()
                top_genres = genre_counts[genre_counts > 100].index.tolist()
                if top_genres:
                    genre_name = top_genres[0]
                    p4 = self.visualizer.plot_radar_chart(genre_name)
                    plot_paths.append(p4)
                    print(f"✅ {p4}")

                print(f"\n📊 All visualizations saved to: {self.visualizer.output_dir}")
                for path in plot_paths:
                    print(f"   - {path}")

            elif choice == '6':
                print("Cancelled.")
                return
            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"\n❌ Error generating visualization: {str(e)}")

    def _summary_menu(self):
        """Handle option 7: Show dataset summary."""
        if not self._ensure_data_loaded():
            return

        try:
            summary = self.analyzer.dataset_summary()

            print("\n" + "=" * 50)
            print("  DATASET SUMMARY")
            print("=" * 50)
            print(f"   Total rows:        {summary['total_rows']}")
            print(f"   Total columns:     {summary['total_columns']}")
            print(f"   Memory usage:      {summary['memory_usage']:.2f} MB")
            print(f"   Numeric columns:   {len(summary['numeric_columns'])}")
            print(f"   Categorical cols:  {len(summary['categorical_columns'])}")

            # Show descriptive stats
            print("\n📊 Descriptive Statistics (numeric columns):")
            print("-" * 50)
            desc = self.analyzer.descriptive_stats()
            print(desc.round(2).to_string())

            # Top tracks
            print("\n🏆 Top 5 Tracks by Popularity:")
            print("-" * 50)
            top = self.analyzer.top_tracks_by_popularity(5)
            for _, row in top.iterrows():
                print(f"   {row['track_name']:<30} | {row['artists']:<20} | Pop: {row['popularity']}")

            # Missing values
            report = self.loader.get_missing_values_report()
            missing_total = report['Missing_Count'].sum()
            print(f"\n🔍 Missing values: {missing_total} total")
            if missing_total > 0:
                missing_cols = report[report['Missing_Count'] > 0]
                for _, row in missing_cols.iterrows():
                    print(f"   {row['Column']}: {row['Missing_Count']} ({row['Missing_Percent']:.2f}%)")

        except Exception as e:
            print(f"\n❌ Error showing summary: {str(e)}")

    def run(self):
        """Run the main CLI loop."""
        print("\n🎵 Welcome to Spotify Data Studio!")
        print("Type the option number and press Enter.\n")

        while self._running:
            try:
                self.show_menu()
                choice = input("Enter your choice (1-8): ").strip()

                if choice == '1':
                    self._load_dataset_menu()
                elif choice == '2':
                    self._clean_missing_menu()
                elif choice == '3':
                    self._handle_outliers_menu()
                elif choice == '4':
                    self._add_song_menu()
                elif choice == '5':
                    self._analysis_menu()
                elif choice == '6':
                    self._visualization_menu()
                elif choice == '7':
                    self._summary_menu()
                elif choice == '8':
                    print("\n👋 Thank you for using Spotify Data Studio. Goodbye!")
                    self._running = False
                else:
                    print("\n❌ Invalid choice. Please enter a number between 1 and 8.")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n👋 Exiting gracefully...")
                self._running = False
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
                input("\nPress Enter to continue...")