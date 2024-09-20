from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

# Initialize Elasticsearch client
es = Elasticsearch(hosts="http://localhost:9200")

# Define search body to aggregate products
search_body = {
    "size": 0,
    "aggs": {
        "products": {
            "terms": {
                "field": "product_id",
                "size": 10000,
            }
        }
    }
}

# Execute search query
result = es.search(index="sales_dapom", body=search_body)

# Convert response to JSON serializable format
result_dict = {
    "took": result.get('took'),
    "timed_out": result.get('timed_out'),
    "_shards": result.get('_shards'),
    "aggregations": result.get('aggregations')
}

# Print JSON formatted response
print(json.dumps(result_dict, indent=4))

# Normalize the aggregations to create a DataFrame
dfWithProducts = pd.DataFrame(json_normalize(result_dict['aggregations']['products']['buckets']))

# Rename columns for better readability
dfWithProducts.rename(columns={'key': 'product_id', 'doc_count': 'total_sales'}, inplace=True)

# Print the DataFrame
print(dfWithProducts)

# Save DataFrame to CSV
dfWithProducts.to_csv('count.csv', index=False)

# Initialize a list to hold final product statistics
final_stats = []

# Iterate over each product to perform further analysis
for _, row in dfWithProducts.iterrows():
    product_id = row['product_id']

    # Define search body to aggregate sales data by day
    search_body1 = {
        'size': 0,
        'query': {
            'bool': {
                'must': [
                    {'term': {'product_id': product_id}}
                ]
            }
        },
        'aggs': {
            'days': {
                'histogram': {
                    'field': 'day',
                    'interval': 1,
                    'extended_bounds': {
                        'min': 1,
                        'max': 730
                    }
                }
            }
        }
    }

    # Execute search query
    result1 = es.search(index="sales_dapom", body=search_body1)

    # Convert response to JSON serializable format
    result1_dict = {
        "took": result1.get('took'),
        "timed_out": result1.get('timed_out'),
        "_shards": result1.get('_shards'),
        "aggregations": result1.get('aggregations')
    }

    # Normalize the days aggregation to create a DataFrame
    df = pd.DataFrame(json_normalize(result1_dict['aggregations']['days']['buckets']))

    # Create an array to hold daily sales data
    Array = np.zeros(730)
    for bucket in result1_dict['aggregations']['days']['buckets']:
        Array[int(bucket['key']) - 1] = bucket['doc_count']

    # Calculate average demand and standard deviation for this product
    averageDemand = Array.mean()
    standardDeviation = Array.std()

    # Append product-level stats to final list
    final_stats.append({
        'product_id': product_id,
        'averageDemand': averageDemand,
        'StandardDeviation': standardDeviation
    })

# Create a DataFrame from the product statistics
final_stats_df = pd.DataFrame(final_stats)

# Merge the product stats with the initial product data
final_result = pd.merge(dfWithProducts, final_stats_df, on='product_id', how='left')

# Print the final result DataFrame
print(final_result)

# Save final result to CSV
final_result.to_csv('demand_final.csv', encoding='utf-8', index=False)
