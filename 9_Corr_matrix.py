# Import necessary libraries for data manipulation and interaction with Elasticsearch
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

# Initialize the Elasticsearch client
es = Elasticsearch(hosts="http://localhost:9200")

# Define the search query to aggregate total sales by product_id
search_body4 = {
    "size": 0,  # No hits returned, only aggregation results
    "aggs": {
        "products": {
            "terms": {
                "field": "product_id",  # Field to aggregate on
                "size": 10000,  # Limit to the top 10,000 products
            }
        }
    }
}

# Execute the search query against the 'sales_dapom' index
result4 = es.search(index="sales_dapom", body=search_body4)
result4_dict = result4.body  # Get the response body

# Print the full response for debugging purposes
print(json.dumps(result4_dict, indent=4))

# Normalize the aggregation results into a DataFrame
dfWithProducts = pd.DataFrame(json_normalize(result4_dict['aggregations']['products']['buckets']))

# Save the DataFrame to a CSV file
dfWithProducts.to_csv('Products.csv')

# Rename columns for better clarity
dfWithProducts.rename(columns={'key': 'product id', 'doc_count': 'total sales'}, inplace=True)

# Iterate over each product in the DataFrame to get daily sales data
for index, row in dfWithProducts.iterrows():
    # Define the search query to aggregate daily sales for the current product
    search_body5 = {
        'size': 0,  # No hits returned, only aggregation results
        'query': {
            'bool': {
                'must': {
                    'term': {'product_id': row['product id']}  # Use product id from the current row
                }
            }
        },
        'aggs': {
            'days': {
                'histogram': {
                    'field': 'day',  # Field to histogram over (days)
                    'interval': 1,  # Interval of 1 day
                    'extended_bounds': {
                        'min': 1,  # Minimum bound for the histogram
                        'max': 730  # Maximum bound for the histogram (2 years)
                    }
                }
            },
            'test': {
                'extended_stats_bucket': {
                    'buckets_path': 'days>_count'  # Calculate extended stats on the histogram counts
                }
            }
        }
    }

    # Execute the second search query for daily sales data
    result5 = es.search(index="sales_dapom", body=search_body5)
    result5_dict = result5.body  # Get the response body

    # Print the full response for debugging purposes
    print(json.dumps(result5_dict, indent=4))

    # Normalize the daily sales data into a DataFrame
    df = json_normalize(result5_dict['aggregations']['days']['buckets'])

    # Add the product_id to the DataFrame for later reference
    df.loc[df.index, 'product_id'] = row['product id']

    # Rename columns for clarity
    df.rename(columns={'key': 'day', 'doc_count': 'sales'}, inplace=True)

    # Rearrange columns to have 'product_id' first
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]  # Move 'product_id' to the front
    df = df[cols]  # Reorder DataFrame based on the new column order
    print(df)  # Print the DataFrame for debugging

    # Create an array to hold daily sales data for 730 days
    Array = np.zeros((1, 730))

    # Populate the array with sales data from the histogram buckets
    for bucket in result5['aggregations']['days']['buckets']:
        Array[0, int(bucket['key'] - 1)] = bucket['doc_count']  # Adjust for 0-based index

    # Append the daily sales data to a CSV file
    pd.DataFrame(Array).to_csv("Array.csv", encoding='utf-8', mode='a', header=False)
