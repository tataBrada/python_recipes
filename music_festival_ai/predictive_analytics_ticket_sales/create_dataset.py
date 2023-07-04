# Import libraries
import random

import numpy as np
import pandas as pd

# Define the number of samples and features
n_samples = 1000
n_features = 10

# Define the feature names
feature_names = ["artist_popularity", "genre", "ticket_price", "venue_capacity", "weather", "day_of_week", "month",
                 "distance_from_city", "promotion_budget", "previous_attendance"]

# Define the feature ranges and types
feature_ranges = [(0, 10),  # artist_popularity: a score from 0 to 100
                 (0, 5),  # genre: an integer from 0 to 5 representing different music genres
                 (10, 200),  # ticket_price: a value in dollars from 10 to 200
                 (1000, 10000),  # venue_capacity: a number from 100 to 10000
                 (0, 1),  # weather: a binary value indicating sunny (1) or rainy (0)
                 (0, 6),  # day_of_week: an integer from 0 to 6 representing Monday to Sunday
                 (1, 12),  # month: an integer from 1 to 12 representing January to December
                 (0, 50),  # distance_from_city: a value in miles from 0 to 50
                 (0, 100000),  # promotion_budget: a value in dollars from 0 to 100000
                 (0, 10000)]  # previous_attendance: a number from 0 to 10000

feature_types = [int, int, int, int, int, int, int, int, int, int]

# Generate random feature values
features = np.random.rand(n_samples, n_features)

# Scale and cast the feature values according to the ranges and types
for i in range(n_features):
    min_val, max_val = feature_ranges[i]
    features[:, i] = features[:, i] * (max_val - min_val) + min_val
    features[:, i] = features[:, i].astype(feature_types[i])


# Create a pandas dataframe with the features
df = pd.DataFrame(features, columns=feature_names)
df["ticket_sales"] = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 0.95]) * df['venue_capacity']

# Save the dataframe as a csv file
df.to_csv('ticket_sales_data.csv', index=False)

# Print the first five rows of the dataframe
print(df.head())
print(df.corr())
