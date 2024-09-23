# Python Warehouse Allocation: Optimizing Inventory for Belsimpel

### Case Description
The case study is inspired by real-life challenges faced by Belsimpel, an online store for mobile phones and contracts. Belsimpel is facing operational bottlenecks due to a rapidly expanding product assortment. The current warehouse, although efficient, can only accommodate a limited collection of products. The challenge is to determine which products to store to minimize profit losses, considering delivery times, demand patterns, and space constraints. The code addresses the decision-making processes and methodologies used to solve the allocation problem of products in a warehouse. 

##### Key Concepts

- Product Classes: Products are classified into three categories based on profitability.
- Inventory Management: A periodic-review base-stock policy will be used for inventory management.
- Storage Constraints: The warehouse has a capacity of 960 pick-up boxes, each with a specified volume.
- Delivery Impact: Delays in delivery can significantly affect sales, especially for high-profit products.

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

Requirements

- Python 3.x
    Libraries:
    - `datetime`: For handling date and time.
    - `elasticsearch`: For interacting with Elasticsearch.
    - `json`: For parsing JSON data.
    - `pandas`: For data manipulation and analysis.
    - `numpy`: For numerical operations.
    - `matplotlib`: For data visualization.
    - `csv`: For handling CSV file operations.
    - `statistics`: For basic statistical operations.
    - `seaborn`: For advanced data visualizations.
    - `math`: For mathematical functions.
    - `adjustText`: For adjusting text in plots.
    - `gurobipy`: For optimization modeling.

Data Sources
- Sales Data: Indexed in Elasticsearch under sales_dapom.
- Profit Data: Indexed in Elasticsearch under profits_dapom.
- Dimensions Data: Indexed in Elasticsearch under dimensions_dapom.

Key Steps

- Data Aggregation:
    - Aggregate product sales by product ID and calculate total sales.
    - Further analyze sales data by day to compute average demand and standard deviation.
- Statistics Calculation:
    - Combine sales and demand statistics into a final dataset.
- Visualization:
    - Create error bar plots for average daily demand.
    - Generate histograms for average daily profits.

- Retrieving Product Dimensions
    - We aggregate product dimensions (length, width, height) from the dimensions_dapom index:

- Volume Calculation
    - After retrieving the dimensions, we calculate the volume for each product:
- Product Classification
Products are categorized based on their average daily profits, with three classes defined:
    - Class 1: Top 20% of products
    - Class 2: Middle range products
    - Class 3: Bottom products
Classifications are saved to product_classes.csv.
Visualizations
Box Calculation:

    Calculate the required number of boxes for each product based on volume and base stock.
    Adjust fractional box counts to whole numbers using specific thresholds.

Data Visualization:

    Create a histogram to visualize the distribution of the number of boxes across products.

- Elasticsearch Querying:

    Query Elasticsearch to aggregate product sales data and normalize it into DataFrames.

- Correlation Analysis:

    Calculate and visualize the correlation matrix of products based on sales data.
    Identify pairs of products with significant correlations.

- Profit and Loss Calculations:

Calculate daily profit/loss based on product classes and average daily profits.
    Filter products based on cumulative box counts to assess capacity constraints.

- Optimization: Set up a linear programming model to maximize profit while adhering to box capacity constraints.

We generate various plots, including:

    Volume Histogram: Shows the distribution of product volumes.
    Average Profits per Product: Displays profits color-coded by class.
    Bar Plots: Illustrate the number of products in each class and average profits per class.


Output Files

    count.csv: Contains total sales and demand statistics.
    demand_final.csv: Merged dataset of sales and demand statistics.
    stats.csv: Sorted dataset by average daily demand.
    average_daily_profits.csv: Sorted dataset by average daily profits.
    errorbar.png: Error bar plot of average daily demand.
    average_daily_profits_histogram.png: Histogram of average daily profits.
    volumes.csv: Contains calculated product volumes.
    product_classes.csv: Lists products classified by profit category.
    Base_stock_levels.csv: Final stock level recommendations.
        volumes.csv: Contains calculated product volumes.
    product_classes.csv: Lists products classified by profit category.
    Base_stock_levels.csv: Final stock level recommendations.



Usage

To run the analysis:
- Ensure Elasticsearch is running and accessible.
- Execute the Python script in an environment where the required libraries are installed.
- Check the output files for results.
