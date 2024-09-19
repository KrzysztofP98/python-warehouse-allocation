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
