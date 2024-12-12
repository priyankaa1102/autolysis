# Automated Analysis Report

## The Story Behind the Data

We started with an unfamiliar dataset, unsure of its structure or content. Our goal was to uncover its hidden narratives through systematic analysis and compelling visualizations. Here's what we discovered:

### The Dataset at a Glance

The dataset consists of 10000 rows and 23 columns. Below are the details of the columns:

- **book_id** (int64)
- **goodreads_book_id** (int64)
- **best_book_id** (int64)
- **work_id** (int64)
- **books_count** (int64)
- **isbn** (object)
- **isbn13** (float64)
- **authors** (object)
- **original_publication_year** (float64)
- **original_title** (object)
- **title** (object)
- **language_code** (object)
- **average_rating** (float64)
- **ratings_count** (int64)
- **work_ratings_count** (int64)
- **work_text_reviews_count** (int64)
- **ratings_1** (int64)
- **ratings_2** (int64)
- **ratings_3** (int64)
- **ratings_4** (int64)
- **ratings_5** (int64)
- **image_url** (object)
- **small_image_url** (object)

We identified missing values in the following columns, indicating areas for potential data imputation:

- book_id: 0 missing values
- goodreads_book_id: 0 missing values
- best_book_id: 0 missing values
- work_id: 0 missing values
- books_count: 0 missing values
- isbn: 700 missing values
- isbn13: 585 missing values
- authors: 0 missing values
- original_publication_year: 21 missing values
- original_title: 585 missing values
- title: 0 missing values
- language_code: 1084 missing values
- average_rating: 0 missing values
- ratings_count: 0 missing values
- work_ratings_count: 0 missing values
- work_text_reviews_count: 0 missing values
- ratings_1: 0 missing values
- ratings_2: 0 missing values
- ratings_3: 0 missing values
- ratings_4: 0 missing values
- ratings_5: 0 missing values
- image_url: 0 missing values
- small_image_url: 0 missing values

### The Analysis Journey

We performed the following analyses to understand the dataset better:

- Calculated summary statistics to identify ranges, means, and variances.
- Detected outliers using Z-scores, revealing potential anomalies or extreme values.
- Conducted correlation analysis, highlighting relationships between numerical columns.
- Clustered data points into groups based on similarity, using K-means clustering.

### Insights Unveiled

Here are the significant insights we discovered:

- **goodreads_book_id** contains 78 potential outliers, suggesting anomalies worth investigating.
- **best_book_id** contains 87 potential outliers, suggesting anomalies worth investigating.
- **work_id** contains 254 potential outliers, suggesting anomalies worth investigating.
- **books_count** contains 178 potential outliers, suggesting anomalies worth investigating.
- **isbn13** contains 33 potential outliers, suggesting anomalies worth investigating.
- **original_publication_year** contains 53 potential outliers, suggesting anomalies worth investigating.
- **average_rating** contains 72 potential outliers, suggesting anomalies worth investigating.
- **ratings_count** contains 108 potential outliers, suggesting anomalies worth investigating.
- **work_ratings_count** contains 119 potential outliers, suggesting anomalies worth investigating.
- **work_text_reviews_count** contains 151 potential outliers, suggesting anomalies worth investigating.
- **ratings_1** contains 73 potential outliers, suggesting anomalies worth investigating.
- **ratings_2** contains 121 potential outliers, suggesting anomalies worth investigating.
- **ratings_3** contains 135 potential outliers, suggesting anomalies worth investigating.
- **ratings_4** contains 134 potential outliers, suggesting anomalies worth investigating.
- **ratings_5** contains 108 potential outliers, suggesting anomalies worth investigating.

From the correlation heatmap, we observed several strong and weak relationships between numerical columns, offering clues about dependencies in the dataset.
The clustering analysis revealed distinct groupings, providing a deeper understanding of inherent data patterns.

### Implications of the Findings

The findings from the analysis suggest actionable steps:
- Address missing data in key columns to improve dataset completeness.
- Investigate detected outliers to identify errors or opportunities.
- Leverage identified correlations for predictive modeling or optimization.
- Use clustering insights for targeted marketing, segmentation, or resource allocation.

## Visualizations

The following visualizations support our analysis:

![correlation_heatmap.png](./correlation_heatmap.png)
![correlation_matrix.png](./correlation_matrix.png)
![overall_histogram.png](./overall_histogram.png)
![clustering_plot.png](./clustering_plot.png)
