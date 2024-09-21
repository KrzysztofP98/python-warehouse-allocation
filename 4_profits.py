from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize the Elasticsearch connection
es = Elasticsearch(hosts="http://localhost:9200")

# Elasticsearch query
search_body2 = {
    'size': 0,
    'aggs': {
        'products1': {
            'terms': {
                'field': 'product_id',
                'size': 10000
            },
            'aggs': {
                'profits': {
                    'sum': {
                        'field': 'margin'
                    }
                }
            }
        }
    }
}

# Execute search query and convert the result to a dictionary
result2 = es.search(index="profits_dapom", body=search_body2)

# Access the body of the result to make it serializable
result2_dict = result2.body

# Print the formatted JSON output of the result
print(json.dumps(result2_dict, indent=4))

# Normalize the aggregation response into a DataFrame
dfProfits = pd.json_normalize(result2_dict['aggregations']['products1']['buckets'])

# Load additional data from CSV
new = pd.read_csv("C:/Users/krzys/Desktop/final/stats.csv")

# Calculate the 'Average_daily_profit'
co = new['averageDemand'] * dfProfits['profits.value']
print(co)

# Insert the new calculated column into the DataFrame
dfProfits.insert(3, 'Average_daily_profit', co)

# Sort the DataFrame by the 'Average_daily_profit' column
dfProfits_sorted = dfProfits.sort_values(by=['Average_daily_profit'], ascending=False)
print(dfProfits_sorted)

# Rename columns for better readability
dfProfits_sorted.rename(columns={'key': 'product_id', 'profits.value': 'margin'}, inplace=True)

# Reset the index and drop unnecessary columns
dfProfits_sorted = dfProfits_sorted.reset_index()
dfProfits_sorted.drop(['index', 'doc_count'], axis=1, inplace=True)

# Save the sorted DataFrame to a CSV file
dfProfits_sorted.to_csv('average_daily_profits.csv')

# Load the saved CSV
ok = pd.read_csv("average_daily_profits.csv")

# Create a histogram of the 'Average_daily_profit' column
plt.xlabel('average daily profits')
plt.ylabel('frequency of given profits')
plt.title('histogram of average daily profits')


# Plot the histogram
plt.hist(ok['Average_daily_profit'], bins=1263, histtype='stepfilled')

plt.savefig("average_daily_profits_histogram.png")
