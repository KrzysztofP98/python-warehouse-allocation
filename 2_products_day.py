from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

# Initialize Elasticsearch client
es = Elasticsearch(hosts="http://elastic:password@localhost:9201")

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
            },
            'test': {
                'extended_stats_bucket': {
                    'buckets_path': 'days>_count'
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

    # Print JSON formatted response
    print(json.dumps(result1_dict, indent=4))

    # Normalize the days aggregation to create a DataFrame
    df = pd.DataFrame(json_normalize(result1_dict['aggregations']['days']['buckets']))
    df['product_id'] = product_id  # Add product_id column

    # Rename columns for better readability
    df.rename(columns={'key': 'day', 'doc_count': 'sales'}, inplace=True)

    # Reorder columns
    df = df[['product_id', 'day', 'sales']]

    # Save DataFrame to CSV (append mode)
    df.to_csv('sales_product_each_row.csv', encoding='utf-8', mode='a', index=False)

    # Create an array to hold daily sales data
    Array = np.zeros(730)
    for bucket in result1_dict['aggregations']['days']['buckets']:
        Array[int(bucket['key']) - 1] = bucket['doc_count']

    # Add average demand and standard deviation to the DataFrame
    df['averageDemand'] = Array.mean()
    df['StandardDeviation'] = Array.std()

# After the loop: Aggregate and clean up final DataFrame
final_df = df[['product_id', 'averageDemand', 'StandardDeviation']]
final_df = final_df.dropna()  # Drop rows with NaN values

# Print final DataFrame
print(final_df)

# Concatenate with the initial DataFrame
final_result = pd.concat([dfWithProducts, final_df], axis=1)

# Save final result to CSV (append mode)
final_result.to_csv('demand_final.csv', encoding='utf-8', mode='a', index=False)
