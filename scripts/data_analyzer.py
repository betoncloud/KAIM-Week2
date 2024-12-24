import pandas as pd
import numpy as np
# Function to get top 10, bottom 10, and most frequent values
def compute_top_bottom_most_frequent(column):
    top_10 = column.nlargest(10)
    bottom_10 = column.nsmallest(10)
    most_frequent = column.mode().head(10)  # Get top 10 most frequent values, in case there are multiple modes
    
    return top_10, bottom_10, most_frequent

def calculate_dispersion(column):
    try:
        # 1. Range
        data_range = column.max() - column.min()

        # 2. Variance
        data_variance = column.var()

        # 3. Standard Deviation
        data_std_dev = column.std()

        # 4. Interquartile Range (IQR)
        Q1 = column.quantile(0.25)
        Q3 = column.quantile(0.75)
        data_iqr = Q3 - Q1

        # 5. Coefficient of Variation (CV)
        mean = column.mean()
        data_cv = data_std_dev / mean
        # Return results as a dictionary
        return {
            "Data Range": data_range,
            "Data Variance": data_variance,
            "Data STD DEV": data_std_dev,
            "Data IQR": data_iqr,
            "Data CV": data_cv,
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Calculate Engagement Score & Experience Score
def euclidean_distance(point, centroid):
    return np.sqrt(np.sum((point - centroid) ** 2))