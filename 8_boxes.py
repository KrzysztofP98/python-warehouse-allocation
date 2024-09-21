from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import mean
import seaborn as sns

# --- Volume Calculation for Box Packing ---

# Define the volume of a single box (length=40, width=40, height=20)
box_volume = 40 * 40 * 20
print(box_volume)  # Print the volume of a single box for reference

# Load the CSV files into the DataFrame (this file contains product volume & stock information)
pt = pd.read_csv('C:/Users/krzys/Desktop/final/volumes.csv')
stock = pd.read_csv('C:/Users/krzys/Desktop/final/Base_stock_levels.csv')

# Remove any columns in 'pt' that have 'Unnamed' in their name (artifact of CSV import)
pt = pt.loc[:, ~pt.columns.str.contains('^Unnamed')]

# Rename 'key' column in 'pt' to 'product_id' for consistency with the stock data
pt.rename(columns={'key': 'product_id'}, inplace=True)

# Drop the 'doc_count' column from 'pt' if it is irrelevant for further calculations
pt = pt.drop(labels='doc_count', axis=1)

# Print 'pt' DataFrame to check the updated data after cleaning
print(pt)

# Print 'stock' DataFrame to check its content
print(stock)

# Insert the 'base_stock' column from 'stock' DataFrame into the 'pt' DataFrame
column = stock['base_stock']
pt.insert(5, 'base_stock', column)

# --- Box Calculation for Each Product ---

# Calculate the required number of boxes for each product by dividing product volume by box volume,
# and multiplying by the base stock. The result is rounded to 2 decimal places.
pt['boxes'] = round((pt['Volume'] * round(pt['base_stock'])) / box_volume, 2)

# --- Adjusting the Number of Boxes into Whole Numbers ---

# The following lines map fractional box counts to whole numbers based on thresholds.
# For example, if the number of boxes is between 7.2 and 8.1, it is rounded to 9 boxes.
pt.loc[(pt['boxes'] > 7.2) & (pt['boxes'] <= 8.1), 'boxes'] = 9
pt.loc[(pt['boxes'] > 6.3) & (pt['boxes'] <= 7.2), 'boxes'] = 8
pt.loc[(pt['boxes'] > 5.4) & (pt['boxes'] <= 6.3), 'boxes'] = 7
pt.loc[(pt['boxes'] > 4.5) & (pt['boxes'] <= 5.4), 'boxes'] = 6
pt.loc[(pt['boxes'] > 3.6) & (pt['boxes'] <= 4.5), 'boxes'] = 5
pt.loc[(pt['boxes'] > 2.7) & (pt['boxes'] <= 3.6), 'boxes'] = 4
pt.loc[(pt['boxes'] > 1.8) & (pt['boxes'] <= 2.7), 'boxes'] = 3
pt.loc[(pt['boxes'] > 0.9) & (pt['boxes'] <= 1.8), 'boxes'] = 2
pt.loc[pt['boxes'] <= 0.9, 'boxes'] = 1  # Assign 1 box if the calculated boxes are less than or equal to 0.9

# Print the updated 'pt' DataFrame to see the calculated number of boxes for each product
print(pt)

# --- Plotting the Histogram ---

# Create a histogram to show the distribution of the number of boxes across products
plt.hist(pt['boxes'], bins=1263, histtype='step', linewidth=5)

# Set the labels for the Y-axis (frequency) and X-axis (number of boxes) and give a title to the plot
plt.ylabel('Frequency of a given number of boxes')
plt.xlabel('Number of Boxes')
plt.title('Histogram of number of boxes')

# Display the histogram plot
plt.savefig("histogram_number_boxes.png")

# --- Saving the Results ---
# Save the updated 'pt' DataFrame (with the calculated number of boxes) to a CSV file named 'boxes.csv'
pt.to_csv('boxes.csv')
