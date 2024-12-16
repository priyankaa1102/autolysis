# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "scikit-learn"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data(file_path):
    """
    Load a CSV file with support for multiple encodings.

    Args:
        file_path (str): Path to the dataset.

    Returns:
        DataFrame: Loaded dataset.
    """
    try:
        data = pd.read_csv(file_path, encoding="utf-8")
        print(f"Data loaded successfully with UTF-8 encoding. Shape: {data.shape}")
        return data
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(file_path, encoding="ISO-8859-1")
            print(f"Data loaded successfully with ISO-8859-1 encoding. Shape: {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading CSV with fallback encoding: {e}")
            sys.exit(1)

# Analyze the dataset
def analyze_data(data):
    """
    Perform basic analysis on the dataset.

    Args:
        data (DataFrame): The dataset to analyze.

    Returns:
        dict: Summary of the analysis.
    """
    analysis_summary = {
        "shape": data.shape,
        "columns": data.dtypes.to_dict(),
        "missing_values": data.isnull().sum().to_dict(),
        "summary_statistics": data.describe(include="all").to_dict(),
        "outliers": identify_outliers(data),
    }
    return analysis_summary

# Identify outliers using Z-score
def identify_outliers(data):
    """
    Identify potential outliers using Z-score.

    Args:
        data (DataFrame): Dataset to check for outliers.

    Returns:
        dict: Number of outliers in each numeric column.
    """
    outlier_summary = {}
    numeric_data = data.select_dtypes(include=["number"])
    if not numeric_data.empty:
        z_scores = (numeric_data - numeric_data.mean()) / numeric_data.std()
        outlier_summary = (z_scores.abs() > 3).sum().to_dict()
    return outlier_summary

# Perform clustering analysis
def perform_clustering(data):
    """
    Apply K-Means clustering to the dataset.

    Args:
        data (DataFrame): Dataset to cluster.

    Returns:
        np.array: Cluster assignments.
    """
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.shape[1] < 2:
        print("Insufficient numeric columns for clustering.")
        return None

    numeric_data = numeric_data.fillna(numeric_data.mean())
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    data["Cluster"] = clusters
    return clusters

# Generate visualizations
def generate_visualizations(data, output_dir):
    """
    Generate visualizations such as heatmaps, histograms, and scatter plots.

    Args:
        data (DataFrame): The dataset to visualize.
        output_dir (str): Directory to save the visualizations.

    Returns:
        list: Paths to the saved visualizations.
    """
    charts = []
    try:
        numeric_data = data.select_dtypes(include=["number"])

        # Correlation Heatmap
        if numeric_data.shape[1] > 1:
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
            heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
            plt.savefig(heatmap_path)
            charts.append(heatmap_path)
            plt.close()

        # Scatter Matrix
        scatter_matrix_path = os.path.join(output_dir, "scatter_matrix.png")
        pd.plotting.scatter_matrix(numeric_data, figsize=(12, 12))
        plt.savefig(scatter_matrix_path)
        charts.append(scatter_matrix_path)
        plt.close()

        # Histograms
        histogram_path = os.path.join(output_dir, "histograms.png")
        numeric_data.hist(figsize=(12, 10), bins=30)
        plt.tight_layout()
        plt.savefig(histogram_path)
        charts.append(histogram_path)
        plt.close()

        # Clustering Scatter Plot
        if "Cluster" in data.columns and numeric_data.shape[1] > 1:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(
                x=numeric_data.columns[0],
                y=numeric_data.columns[1],
                hue="Cluster",
                data=data,
                palette="viridis"
            )
            clustering_path = os.path.join(output_dir, "clustering_plot.png")
            plt.savefig(clustering_path)
            charts.append(clustering_path)
            plt.close()

    except Exception as e:
        print(f"Visualization error: {e}")
    return charts

# Write README.md
def write_readme(analysis_summary, charts, output_dir):
    """
    Generate a narrative-driven README.md summarizing the analysis.

    Args:
        analysis_summary (dict): Analysis summary.
        charts (list): Paths to visualizations.
        output_dir (str): Directory to save README.md.
    """
    readme_content = f"""
# Automated Analysis Report

## Dataset Summary
- **Rows**: {analysis_summary['shape'][0]}
- **Columns**: {analysis_summary['shape'][1]}

### Missing Values
{analysis_summary['missing_values']}

### Insights
- Outliers detected: {analysis_summary['outliers']}

## Visualizations
"""
    for chart in charts:
        chart_name = os.path.basename(chart)
        readme_content += f"![{chart_name}]({chart})\n"

    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"README.md written to {readme_path}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    output_dir = "."
    data = load_data(file_path)
    analysis_summary = analyze_data(data)

    perform_clustering(data)
    charts = generate_visualizations(data, output_dir)
    write_readme(analysis_summary, charts, output_dir)
