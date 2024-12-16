# requires-python = ">=3.11"
# dependencies = [
#   "seaborn",
#   "pandas",
# ]

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data(file_path):
    try:
        # Attempt to read with utf-8 encoding
        data = pd.read_csv(file_path, encoding="utf-8")
        print(f"Data loaded successfully with UTF-8 encoding. Shape: {data.shape}")
        return data
    except UnicodeDecodeError:
        try:
            # Fallback to ISO-8859-1 encoding
            data = pd.read_csv(file_path, encoding="ISO-8859-1")
            print(f"Data loaded successfully with ISO-8859-1 encoding. Shape: {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading CSV with fallback encoding: {e}")
            sys.exit(1)

# Analyze the dataset
def analyze_data(data):
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
    outlier_summary = {}
    numeric_data = data.select_dtypes(include=["number"])
    if not numeric_data.empty:
        z_scores = (numeric_data - numeric_data.mean()) / numeric_data.std()
        outlier_summary = (z_scores.abs() > 3).sum().to_dict()
    return outlier_summary

# Perform clustering analysis
def perform_clustering(data):
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.shape[1] < 2:
        return None

    # Handle missing values by imputing the mean
    numeric_data = numeric_data.fillna(numeric_data.mean())

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    data["Cluster"] = clusters
    return clusters

def generate_visualizations(data, output_dir):
    charts = []
    try:
        # Select only numeric columns for correlation heatmap, scatter matrix, etc.
        numeric_data = data.select_dtypes(include=["number"])

        # Correlation Heatmap
        if numeric_data.shape[1] > 1:
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
            heatmap_path = f"{output_dir}/correlation_heatmap.png"
            plt.savefig(heatmap_path)
            charts.append(heatmap_path)
            plt.close()
            print(f"Saved heatmap at {heatmap_path}")  # Added logging

        # Correlation Matrix
        correlation_matrix_path = f"{output_dir}/correlation_matrix.png"
        pd.plotting.scatter_matrix(numeric_data, figsize=(12, 12))
        plt.savefig(correlation_matrix_path)
        charts.append(correlation_matrix_path)
        plt.close()
        print(f"Saved correlation matrix at {correlation_matrix_path}")  # Added logging

        # Overall Histogram
        overall_histogram_path = f"{output_dir}/overall_histogram.png"
        numeric_data.hist(figsize=(12, 10), bins=30)
        plt.tight_layout()
        plt.savefig(overall_histogram_path)
        charts.append(overall_histogram_path)
        plt.close()
        print(f"Saved overall histogram at {overall_histogram_path}")  # Added logging

        # Quality Histogram (if applicable column exists)
        if "quality" in numeric_data.columns:
            quality_histogram_path = f"{output_dir}/quality_histogram.png"
            numeric_data["quality"].hist(figsize=(8, 6), bins=20, color="skyblue")
            plt.title("Quality Histogram")
            plt.xlabel("Quality")
            plt.ylabel("Frequency")
            plt.savefig(quality_histogram_path)
            charts.append(quality_histogram_path)
            plt.close()
            print(f"Saved quality histogram at {quality_histogram_path}")  # Added logging

        # Clustering Scatter Plot
        if "Cluster" in data.columns:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=numeric_data.columns[0],
                            y=numeric_data.columns[1],
                            hue="Cluster", data=data, palette="viridis")
            clustering_path = f"{output_dir}/clustering_plot.png"
            plt.savefig(clustering_path)
            charts.append(clustering_path)
            plt.close()
            print(f"Saved clustering plot at {clustering_path}")  # Added logging

    except Exception as e:
        print(f"Visualization error: {e}")
    return charts

# Write README.md
def write_readme(analysis_summary, charts, output_dir):
    readme_content = "# Automated Analysis Report\n\n"
    
    # Story introduction
    readme_content += "## The Story Behind the Data\n\n"
    readme_content += "We started with an unfamiliar dataset, unsure of its structure or content. Our goal was to uncover its hidden narratives through systematic analysis and compelling visualizations. Here's what we discovered:\n\n"
    
    # Dataset description
    readme_content += "### The Dataset at a Glance\n\n"
    readme_content += f"The dataset consists of {analysis_summary['shape'][0]} rows and {analysis_summary['shape'][1]} columns. Below are the details of the columns:\n\n"
    for col, dtype in analysis_summary["columns"].items():
        readme_content += f"- **{col}** ({dtype})\n"
    readme_content += "\n"
    readme_content += "We identified missing values in the following columns, indicating areas for potential data imputation:\n\n"
    for col, missing in analysis_summary["missing_values"].items():
        readme_content += f"- {col}: {missing} missing values\n"
    
    # Analysis summary
    readme_content += "\n### The Analysis Journey\n\n"
    readme_content += "We performed the following analyses to understand the dataset better:\n\n"
    readme_content += "- Calculated summary statistics to identify ranges, means, and variances.\n"
    readme_content += "- Detected outliers using Z-scores, revealing potential anomalies or extreme values.\n"
    readme_content += "- Conducted correlation analysis, highlighting relationships between numerical columns.\n"
    readme_content += "- Clustered data points into groups based on similarity, using K-means clustering.\n"
    
    # Key insights
    readme_content += "\n### Insights Unveiled\n\n"
    readme_content += "Here are the significant insights we discovered:\n\n"
    for col, outliers in analysis_summary["outliers"].items():
        if outliers > 0:
            readme_content += f"- **{col}** contains {outliers} potential outliers, suggesting anomalies worth investigating.\n"
    readme_content += "\nFrom the correlation heatmap, we observed several strong and weak relationships between numerical columns, offering clues about dependencies in the dataset.\n"
    if "Cluster" in data.columns:
        readme_content += "The clustering analysis revealed distinct groupings, providing a deeper understanding of inherent data patterns.\n"

    # Implications
    readme_content += "\n### Implications of the Findings\n\n"
    readme_content += "The findings from the analysis suggest actionable steps:\n"
    readme_content += "- Address missing data in key columns to improve dataset completeness.\n"
    readme_content += "- Investigate detected outliers to identify errors or opportunities.\n"
    readme_content += "- Leverage identified correlations for predictive modeling or optimization.\n"
    readme_content += "- Use clustering insights for targeted marketing, segmentation, or resource allocation.\n"
    
    # Visualizations
    readme_content += "\n## Visualizations\n\n"
    readme_content += "The following visualizations support our analysis:\n\n"
    for chart in charts:
        chart_name = chart.split("/")[-1]
        readme_content += f"![{chart_name}]({chart})\n"

    # Save README
    readme_path = f"{output_dir}/README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"README.md written to {readme_path}")

if __name__ == "__main__":
    # Ensure API Token is provided via environment variable
    API_TOKEN = os.getenv("AIPROXY_TOKEN")
    if not API_TOKEN:
        print("Error: API token is missing. Set the AIPROXY_TOKEN environment variable.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)

    file_path = sys.argv[1]

    # For testing with the uploaded file:
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    output_dir = "."

    data = load_data(file_path)
    analysis_summary = analyze_data(data)

    # Perform clustering if applicable
    clusters = perform_clustering(data)

    charts = generate_visualizations(data, output_dir)
    write_readme(analysis_summary, charts, output_dir)
