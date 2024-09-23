from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

# Initialize the Elasticsearch client with specified host
es = Elasticsearch(hosts="http://localhost:9200")

# Define the search body to aggregate product sales
search_body5 = {
    "size": 0,  # No hits returned, only aggregations
    "aggs": {
        "products": {
            "terms": {
                "field": "product_id",  # Field to aggregate on
                "size": 10000,  # Limit to top 10,000 products
            }
        }
    }
}

# Execute the search query against the specified index
result4 = es.search(index="sales_dapom", body=search_body5)
result4_dict = result4.body  # Store the response body

# Normalize the results into a DataFrame
dfWithProducts = pd.DataFrame(json_normalize(result4_dict['aggregations']['products']['buckets']))
dfWithProducts = json_normalize(result4_dict['aggregations']['products']['buckets'])
# Save the product data to a CSV file
dfWithProducts.to_csv('Products.csv')
# Rename columns for clarity
dfWithProducts.rename(columns={'key': 'product id', 'doc_count': 'total sales'}, inplace=True)

# Clear the CSV file before starting the loop
with open("Array.csv", 'w') as f:
    pass  # Just opening in write mode clears the file

# Iterate over each product in the DataFrame
for row, index in dfWithProducts.iterrows():
    # Define the search body for sales data by product
    search_body5 = {
        'size': 0,  # No hits returned, only aggregations
        'query': {
            'bool': {
                'must': {
                    'term': {'product_id': index[0]}  # Filter by current product ID
                }
            }
        },
        'aggs': {
            'days': {
                'histogram': {
                    'field': 'day',  # Field to create histogram
                    'interval': 1,  # Interval for histogram buckets
                    'extended_bounds': {
                        'min': 1,  # Minimum day
                        'max': 730  # Maximum day
                    }
                }
            },
            'test': {
                'extended_stats_bucket': {
                    'buckets_path': 'days>_count'  # Path for additional statistics
                }
            }
        }
    }

    # Execute the search query for sales data
    result5 = es.search(index="sales_dapom", body=search_body5)
    result5_dict = result5.body  # Store the response body
    print(json.dumps(result5_dict, indent=4))  # Print the result for debugging
    df = json_normalize(result5_dict['aggregations']['days']['buckets'])  # Normalize the histogram data
    df.loc[df.index, 'product_id'] = index[0]  # Add product ID to DataFrame

    df.rename(columns={'key': 'day', 'doc_count': 'sales'}, inplace=True)  # Rename columns for clarity
    cols = df.columns.tolist()  # Get current column order
    cols = cols[-1:] + cols[:-1]  # Move 'product_id' to the front
    df = df[cols]  # Reorder columns
    print(df)  # Print the DataFrame for debugging

    # Initialize a zero array to store sales data for each day
    Array = np.zeros((1, 730))
    # Populate the array with sales data from buckets
    for bucket in result5['aggregations']['days']['buckets']:
        Array[0, int(bucket['key']-1)] = bucket['doc_count']  # Use day key as index

    # Save the array data to a CSV file, appending to existing data
    pd.DataFrame(Array).to_csv("Array.csv", encoding='utf-8', mode='a')
