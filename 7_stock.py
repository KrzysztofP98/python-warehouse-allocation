# Import necessary libraries for working with dates, Elasticsearch, data manipulation, plotting, etc.
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import mean  # Used for calculating mean values
import seaborn as sns  # Used for data visualization
from math import sqrt  # Used to calculate square root, for standard deviation adjustments

# Load the CSV files into a pandas DataFrame
dem = pd.read_csv('stats.csv')
pt = pd.read_csv('product_classes.csv')

# Display the contents of the 'dem' DataFrame to check the loaded data
print(dem)

# --- Calculating weekly demand and standard deviation intervals ---

# Calculate the weekly demand by multiplying average daily demand by 7 (since 7 days in a week)
demand_int = dem['averageDemand'] * 7

# Calculate the standard deviation over the 7-day interval by multiplying the standard deviation by sqrt(7)
std_int = dem['StandardDeviation'] * sqrt(7)

# Add new columns to the 'dem' DataFrame for weekly demand and standard deviation intervals
dem['demand_interval'] = demand_int
dem['std_interval'] = std_int

# Remove any columns that have 'Unnamed' in their name, often artifacts from CSV imports (like index columns)
dem = dem.loc[:, ~dem.columns.str.contains('^Unnamed')]

# Rename columns for better clarity (renaming 'key' to 'product_id' and 'doc_count' to 'sales')
dem.rename(columns={'key': 'product_id', 'doc_count': 'sales'}, inplace=True)

# Sort the 'dem' DataFrame by 'product_id' for proper alignment with the product class data
dem = dem.sort_values(by=['product_id'])

# Display the updated 'dem' DataFrame to verify the changes
print(dem)

# --- Preparing the product class DataFrame ---

# Sort the 'pt' DataFrame (product classes) by 'product_id' to ensure alignment with 'dem'
pt = pt.sort_values(by=['product_id'])

# Remove any columns that have 'Unnamed' in their name from the 'pt' DataFrame as well
pt = pt.loc[:, ~pt.columns.str.contains('^Unnamed')]

# Display the 'pt' DataFrame to verify its contents
print(pt)

# --- Merging product class into the 'dem' DataFrame ---

# Extract the 'product_class' column from 'pt' and assign it to a new column in 'dem'
col = pt['product_class']
dem['product_class'] = col

# --- Base stock level calculation based on product class ---

# For products in class 1, base stock is the weekly demand interval + 0.99 * standard deviation interval
dem.loc[dem['product_class'] == 1, 'base_stock'] = dem['demand_interval'] + 0.99 * dem['std_interval']

# For products in class 2, base stock is the weekly demand interval + 0.95 * standard deviation interval
dem.loc[dem['product_class'] == 2, 'base_stock'] = dem['demand_interval'] + 0.95 * dem['std_interval']

# For products in class 3, base stock is the weekly demand interval + 0.9 * standard deviation interval
dem.loc[dem['product_class'] == 3, 'base_stock'] = dem['demand_interval'] + 0.9 * dem['std_interval']

# --- Final DataFrame adjustments and export ---

# Reset the index of the DataFrame, removing the old index and replacing it with a default one
dem = dem.reset_index()

# Drop the 'index' column created during the index reset process
dem.drop(labels='index', axis=1, inplace=True)

# Display the final 'dem' DataFrame with calculated base stock levels
print(dem)

# Save the final 'dem' DataFrame to a new CSV file named 'Base_stock_levels.csv'
dem.to_csv('Base_stock_levels.csv')
