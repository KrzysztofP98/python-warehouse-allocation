# Import necessary libraries for working with date, Elasticsearch, JSON, pandas and plotting.
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
import matplotlib.pyplot as plt

# Connect to Elasticsearch running on localhost at port 9200
es = Elasticsearch(hosts="http://localhost:9200")

# Define the search query to retrieve aggregated data for products.
# The query will aggregate the sum of length, width, and height fields for each unique product_id.
search_body3 = {
    'size': 0,  # 'size': 0 means we don't want to retrieve individual documents, only the aggregation result.
    'aggs': {
        'products2': {
            'terms': {
                'field': 'product_id',  # Aggregating by product_id.
                'size': 10000  # Retrieve up to 10,000 unique product_ids.
            },
            'aggs': {  # Nested aggregations to sum up dimensions for each product.
                'Length': {
                    'sum': {
                        'field': 'length'  # Sum the 'length' field for each product_id.
                    }
                },
                'Width': {
                    'sum': {
                        'field': 'width'  # Sum the 'width' field for each product_id.
                    }
                },
                'Height': {
                    'sum': {
                        'field': 'height'  # Sum the 'height' field for each product_id.
                    }
                }
            }
        }
    }
}

# Execute the search query against the Elasticsearch index 'dimensions_dapom'.
result3 = es.search(index="dimensions_dapom", body=search_body3)

# Access the body of the result to make it serializable (convert it to a Python dict).
result3_dict = result3.body

# Print the formatted JSON output of the result to inspect the structure.
print(json.dumps(result3_dict, indent=4))

# Normalize the JSON data into a pandas DataFrame for easier manipulation.
# 'buckets' contains the aggregation results for each product.
dm = pd.json_normalize(result3['aggregations']['products2']['buckets'])

# Display the DataFrame to check the results.
print(dm)

# Calculate the volume for each product using the aggregated dimensions (Length, Width, and Height).
# This assumes that the dimensions are independent and calculated per product.
volume = dm['Length.value'] * dm['Height.value'] * dm['Width.value']

# Insert a new 'Volume' column in the DataFrame at position 2, containing the calculated volumes.
dm.insert(2, 'Volume', volume)

# Display the updated DataFrame with the new 'Volume' column.
print(dm)

# Save the DataFrame with volumes to a CSV file for further analysis.
dm.to_csv('volumes.csv')

# Plot a histogram of the volume distribution for the products.
plt.hist(dm['Volume'], bins=1263, histtype='stepfilled')  # 'bins=1263' represents the number of bins in the histogram.
plt.title('Histogram of Product Volumes')  # Title for the plot.
plt.ylabel('Frequency of Given Volume')  # Label for the y-axis (frequency).
plt.xlabel('Volume')  # Label for the x-axis (volume).


# Save the histogram plot as a PNG file for future reference.
plt.savefig("volumes_histogram.png")
