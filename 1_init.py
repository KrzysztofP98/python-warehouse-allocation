from datetime import datetime
from elasticsearch import Elasticsearch
import json
from loaders import ingest_csv_file_into_elastic_index

# Initialize an Elasticsearch client.
# Replace the URL and credentials with your own Elasticsearch instance details.
es = Elasticsearch(hosts="http://localhost:9200")

# Ingest CSV data into Elasticsearch indices.

# Ingest data from 'sales.csv' into the 'sales_dapom' index.
# The buffer size of 5000 means the data will be processed in chunks of 5000 records at a time.
ingest_csv_file_into_elastic_index("sales.csv", es, "sales_dapom", 5000)

# Ingest data from 'margins.csv' into the 'profits_dapom' index.
# Again, using a buffer size of 5000 for chunked processing.
ingest_csv_file_into_elastic_index("margins.csv", es, "profits_dapom", 5000)

# Ingest data from 'dimensions.csv' into the 'dimensions_dapom' index.
# The same buffer size of 5000 is used for processing the data in chunks.
ingest_csv_file_into_elastic_index("dimensions.csv", es, "dimensions_dapom", 5000)
