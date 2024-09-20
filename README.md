# python-warehouse-allocation

### Elasticsearch Data Ingestion

This project contains scripts to ingest CSV and JSON data into an Elasticsearch index. It uses Python and the elasticsearch library for interacting with Elasticsearch.
Prerequisites

Elasticsearch: Ensure Elasticsearch is installed and running on your local machine. The scripts are configured to connect to http://localhost:9201.

Python Packages: Install the necessary Python packages using pip. You'll need:
- elasticsearch
- pandas

You can install these using:
    pip install elasticsearch pandas

### Configuration
Elasticsearch Security

If you encounter connection issues due to security settings in Elasticsearch, you may need to disable security. To do this:

Open the Elasticsearch configuration file (elasticsearch.yml).

Locate and modify the following settings to disable security: yaml

    xpack.security.enabled: false

Save the configuration file and restart Elasticsearch for the changes to take effect.

### CSV Data Ingestion into Elasticsearch

This script ingests data from CSV files into an Elasticsearch instance, creating or updating specific indices. The following files are processed:

    sales.csv → Index: sales_dapom1
    margins.csv → Index: profits_dapom1
    dimensions.csv → Index: dimensions_dapom1

##### Prerequisites

Before running this script, ensure that you have an Elasticsearch instance running and properly configured. You must also have the necessary credentials to connect to your instance.
How the Script Works

    Elasticsearch Client Initialization: The script connects to the Elasticsearch instance using the credentials provided.
    CSV Ingestion: Data from each CSV file is ingested into its corresponding Elasticsearch index. The ingestion is processed in chunks of 5000 records at a time to optimize memory usage and performance.

##### Important: One-Time Run Limitation

This script is not designed to be run more than once without modification. Here’s why:

- Duplicate Data: If you run the script multiple times, the same data will be re-ingested into Elasticsearch, potentially causing duplicate records in the indices.

- Existing Indices: Elasticsearch will retain the indices (sales_dapom1, profits_dapom1, dimensions_dapom1) from the first run. Subsequent runs will add new records or cause errors unless the indices are deleted or modified before re-running the script.

- Schema Conflicts: If the structure of the data in the CSV files changes between runs, Elasticsearch might encounter schema conflicts that can lead to ingestion errors.

##### To Run the Script Multiple Times

If you need to run this script multiple times, consider one of the following approaches:

- Delete Existing Indices: Before re-running the script, delete the existing indices in Elasticsearch to prevent duplicate data and potential conflicts:


    if es.indices.exists(index="sales_dapom1"):
        es.indices.delete(index="sales_dapom1")

- Use Unique Indices: Modify the index names to create new indices on each run (e.g., sales_dapom_v2, profits_dapom_v2).

- Avoid Duplicates: Implement a mechanism to check for and avoid duplicate records during ingestion, such as using unique document IDs for each record.
