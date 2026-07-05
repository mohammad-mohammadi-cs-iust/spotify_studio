"""
DataVisualizer - Creates plots and visualizations for analysis and reporting.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple

from core.constants import NUMERIC_COLUMNS, NORMALIZED_AUDIO_COLUMNS
from core.exceptions import VisualizationError


class DataVisualizer:
    """
    Generates visualizations for data analysis and reporting.
    Saves plots to the reports directory.
    """

    def __init__(self, df: pd.DataFrame, output_dir: str = "reports/generated_plots"):
        """
        Initialize the visualizer with a DataFrame.

        Args:
            df: Input DataFrame
            output_dir: Directory to save generated plots
        """
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Set plotting style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)

    def _save_plot(self, filename: str) -> str:
        """Save the current plot to the output directory."""
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        return filepath

    def plot_missing_values_bar(self, missing_report: pd.DataFrame) -> str:
        """
        Plot a bar chart of missing values per column.

        Args:
            missing_report: DataFrame with missing counts (from DataLoader)

        Returns:
            Path to saved plot file
        """
        try:
            plt.figure(figsize=(14, 8))

            # Filter columns with missing values
            missing_data = missing_report[missing_report['Missing_Count'] > 0]

            if missing_data.empty:
                plt.text(0.5, 0.5, 'No Missing Values Found!',
                         ha='center', va='center', fontsize=16)
                plt.title('Missing Values Report')
                filepath = self._save_plot('missing_values_bar.png')
                plt.close()
                return filepath

            bars = plt.bar(missing_data['Column'], missing_data['Missing_Count'],
                           color='skyblue', edgecolor='navy')

            # Add percentage labels
            for bar, pct in zip(bars, missing_data['Missing_Percent']):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                         f'{pct:.1f}%', ha='center', va='bottom', fontsize=10)

            plt.title('Missing Values by Column', fontsize=16)
            plt.xlabel('Columns', fontsize=12)
            plt.ylabel('Number of Missing Values', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            filepath = self._save_plot('missing_values_bar.png')
            plt.close()
            return filepath

        except Exception as e:
            raise VisualizationError(f"Failed to plot missing values: {str(e)}")

    def plot_genre_popularity_bar(self, top_n: int = 10) -> str:
        """
        Plot a bar chart of average popularity by genre.

        Args:
            top_n: Number of top genres to display

        Returns:
            Path to saved plot file
        """
        try:
            if 'track_genre' not in self.df.columns or 'popularity' not in self.df.columns:
                raise VisualizationError("Required columns missing for genre popularity plot")

            genre_avg = self.df.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).head(top_n)

            plt.figure(figsize=(14, 8))
            bars = plt.bar(genre_avg.index, genre_avg.values,
                           color=plt.cm.viridis(np.linspace(0, 1, len(genre_avg))))

            plt.title(f'Top {top_n} Genres by Average Popularity', fontsize=16)
            plt.xlabel('Genre', fontsize=12)
            plt.ylabel('Average Popularity', fontsize=12)
            plt.xticks(rotation=45, ha='right')

            # Add value labels
            for bar, val in zip(bars, genre_avg.values):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2., height + 0.3,
                         f'{val:.1f}', ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            filepath = self._save_plot('genre_popularity_bar.png')
            plt.close()
            return filepath

        except Exception as e:
            raise VisualizationError(f"Failed to plot genre popularity: {str(e)}")

    def plot_correlation_heatmap(self, columns: Optional[List[str]] = None) -> str:
        """
        Plot a heatmap of correlation matrix.

        Args:
            columns: Specific columns to include (None = all numeric)

        Returns:
            Path to saved plot file
        """
        try:
            if columns is None:
                columns = [col for col in NUMERIC_COLUMNS if col in self.df.columns]
            else:
                columns = [col for col in columns if col in self.df.columns]

            corr_matrix = self.df[columns].corr()

            plt.figure(figsize=(14, 12))
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

            heatmap = sns.heatmap(
                corr_matrix,
                mask=mask,
                annot=True,
                fmt='.2f',
                cmap='RdBu_r',
                vmin=-1,
                vmax=1,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8}
            )

            plt.title('Correlation Matrix of Audio Features', fontsize=16)
            plt.tight_layout()

            filepath = self._save_plot('correlation_heatmap.png')
            plt.close()
            return filepath

        except Exception as e:
            raise VisualizationError(f"Failed to plot correlation heatmap: {str(e)}")

    def plot_feature_scatter(
            self,
            x: str,
            y: str,
            hue: Optional[str] = None,
            title: Optional[str] = None
    ) -> str:
        """
        Create a scatter plot between two features.

        Args:
            x: X-axis column name
            y: Y-axis column name
            hue: Optional column for color coding
            title: Optional custom title

        Returns:
            Path to saved plot file
        """
        try:
            if x not in self.df.columns or y not in self.df.columns:
                raise VisualizationError(f"Columns '{x}' or '{y}' not found in data")

            plt.figure(figsize=(12, 8))

            if hue and hue in self.df.columns:
                # For hue, we need to handle categorical data
                if pd.api.types.is_categorical_dtype(self.df[hue]) or pd.api.types.is_object_dtype(self.df[hue]):
                    # Use a subset of top categories to keep plot readable
                    top_cats = self.df[hue].value_counts().head(10).index
                    plot_df = self.df[self.df[hue].isin(top_cats)]
                    sns.scatterplot(data=plot_df, x=x, y=y, hue=hue, alpha=0.6, palette='tab10')
                else:
                    sns.scatterplot(data=self.df, x=x, y=y, hue=hue, alpha=0.6)
            else:
                sns.scatterplot(data=self.df, x=x, y=y, alpha=0.5, color='steelblue')

            plt.title(title or f'{y} vs {x}', fontsize=14)
            plt.xlabel(x, fontsize=12)
            plt.ylabel(y, fontsize=12)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            filepath = self._save_plot(f'scatter_{x}_vs_{y}.png')
            plt.close()
            return filepath

        except Exception as e:
            raise VisualizationError(f"Failed to create scatter plot: {str(e)}")

    def plot_boxplot_before_after(
            self,
            before_data: pd.Series,
            after_data: pd.Series,
            column_name: str
    ) -> str:
        """
        Create a side-by-side boxplot comparing before and after cleaning.

        Args:
            before_data: Original series before cleaning
            after_data: Cleaned series after cleaning
            column_name: Name of the column for labeling

        Returns:
            Path to saved plot file
        """
        try:
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Before
            axes[0].boxplot(before_data.dropna(), vert=True, patch_artist=True,
                            boxprops=dict(facecolor='lightcoral'))
            axes[0].set_title(f'Before Cleaning - {column_name}', fontsize=14)
            axes[0].set_ylabel(column_name, fontsize=12)
            axes[0].grid(True, alpha=0.3)

            # After
            axes[1].boxplot(after_data.dropna(), vert=True, patch_artist=True,
                            boxprops=dict(facecolor='lightgreen'))
            axes[1].set_title(f'After Cleaning - {column_name}', fontsize=14)
            axes[1].set_ylabel(column_name, fontsize=12)
            axes[1].grid(True, alpha=0.3)

            plt.suptitle(f'Outlier Handling Comparison: {column_name}', fontsize=16)
            plt.tight_layout()

            filepath = self._save_plot(f'boxplot_before_after_{column_name}.png')
            plt.close()
            return filepath

        except Exception as e:
            raise VisualizationError(f"Failed to create boxplot comparison: {str(e)}")

    def plot_radar_chart(self, genre: str, features: Optional[List[str]] = None) -> str:
        """
        Create a radar chart comparing audio features for a specific genre.

        Args:
            genre: Genre to visualize
            features: List of features to include (default: NORMALIZED_AUDIO_COLUMNS)

        Returns:
            Path to saved plot file
        """
        try:
            if features is None:
                features = [col for col in NORMALIZED_AUDIO_COLUMNS if col in self.df.columns]

            if not features:
                raise VisualizationError("No valid audio features found")

            genre_df = self.df[self.df['track_genre'] == genre]
            if genre_df.empty:
                raise VisualizationError(f"Genre '{genre}' not found in dataset")

            # Calculate average features for the genre
            avg_features = genre_df[features].mean().values

            # Also get overall average for comparison
            overall_avg = self.df[features].mean().values

            # Create radar chart
            angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
            angles += angles[:1]  # Close the loop

            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

            # Plot genre averages
            values = avg_features.tolist() + avg_features[:1].tolist()
            ax.plot(angles, values, 'o-', linewidth=2, label=genre, color='blue')
            ax.fill(angles, values, alpha=0.25, color='blue')

            # Plot overall averages
            overall_values = overall_avg.tolist() + overall_avg[:1].tolist()
            ax.plot(angles, overall_values, 'o-', linewidth=2, label='Overall Average', color='red')
            ax.fill(angles, overall_values, alpha=0.15, color='red')

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(features, fontsize=10)
            ax.set_ylim(0, 1)
            ax.set_title(f'Audio Features Comparison: {genre}', fontsize=16, pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            ax.grid(True)

            filepath = self._save_plot(f'radar_{genre}.png')
            plt.close()
            return filepath

        except Exception as e:
            raise VisualizationError(f"Failed to create radar chart: {str(e)}")