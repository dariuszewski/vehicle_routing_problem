# this can be used for optimization
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd


def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


input_df = pd.read_csv("./orders.csv")
print(input_df)

# Create an empty distance matrix
num_cities = len(input_df)
distance_matrix = np.zeros((num_cities, num_cities))

# Calculate distances and fill in the matrix
for i in range(num_cities):
    for j in range(num_cities):
        if i != j:
            lat1 = input_df["latitude"][i]
            lng1 = input_df["longitude"][i]
            lat2 = input_df["latitude"][j]
            lng2 = input_df["longitude"][j]
            distance_matrix[i][j] = haversine(lat1, lng1, lat2, lng2)

# Display the distance matrix
print(distance_matrix)

df = pd.DataFrame(distance_matrix)

cities_map = {index: city for index, city in enumerate(list(input_df["city"]))}

df.rename(index=cities_map, columns=cities_map, inplace=True)

print(df)

df.to_csv("./distance_matrix.csv")
