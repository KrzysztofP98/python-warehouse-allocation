from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import matplotlib.pyplot as plt
from _10_corr_matrix1 import couples

# Load product loss and stock level data from CSV files
loss = pd.read_csv('C:/Users/krzys/Desktop/final/Average_daily_profit_loss.csv')
stock = pd.read_csv('C:/Users/krzys/Desktop/final/Base_stock_levels.csv')

# Clean data by removing any columns that contain 'Unnamed' (usually extra index columns)
loss = loss.loc[:, ~loss.columns.str.contains('^Unnamed')]
stock = stock.loc[:, ~stock.columns.str.contains('^Unnamed')]

# Sort the loss data by 'product_id' for consistent ordering
loss = loss.sort_values(by=['product_id'])

# Save the sorted loss data to a new CSV file and reload it
loss.to_csv('C:/Users/krzys/Desktop/final/loss_sorted_id.csv')
loss_s = pd.read_csv('C:/Users/krzys/Desktop/final/loss_sorted_id.csv')

# Add the 'Average_daily_profit_loss' column from loss to the stock dataframe
column = loss_s['Average_daily_profit_loss']
stock.insert(8, 'Average_daily_profit_loss', column)  # Insert at column position 8

# Print the updated stock dataframe with profit/loss
print("Updated stock dataframe with 'Average_daily_profit_loss' column:")
print(stock)

# Load box data, which contains the number of boxes each product takes up
box = pd.read_csv('C:/Users/krzys/Desktop/final/boxes.csv')

# Print the box data
print("\nBox data (number of boxes per product):")
print(box)

# Add the 'boxes' column from the box dataframe to the loss_s dataframe
column1 = box['boxes']
loss_s.insert(5, 'boxes', column1)  # Insert the boxes data at column position 5

# Clean the data again by removing 'Unnamed' columns and sort by 'Average_daily_profit_loss' (descending)
loss_s = loss_s.loc[:, ~loss_s.columns.str.contains('^Unnamed')]
loss_s = loss_s.sort_values(by=['Average_daily_profit_loss'], ascending=False)

# Calculate the cumulative sum of boxes and add it as a new column
loss_s['cumsum'] = loss_s['boxes'].cumsum()

# Filter products where the cumulative boxes is less than 960 (capacity constraint)
cond = loss_s.where(loss_s['cumsum'] < 960).dropna()

# Save the filtered products and print them
cond.to_csv('C:/Users/krzys/Desktop/final/cond.csv')
print("\nFiltered products where the cumulative sum of boxes is less than 960:")
print(cond)

# Initialize lists to store results
list = []  # Store pairs (couples) of products
list_y = []  # Store product 'y' from the pair when only 'x' is in 'cond'
list_x = []  # Store product 'x' from the pair when only 'y' is in 'cond'
boxes = []  # Store the boxes corresponding to unselected products in pairs
loss_y = []  # Store the profit/loss of 'y' from pairs where only 'x' is in 'cond'
loss_x = []  # Store the profit/loss of 'x' from pairs where only 'y' is in 'cond'

# Loop over each pair (x, y) in the 'couples' list
for x, y in couples:
    # Check if 'x' is in the filtered set (cond) but 'y' is not
    if x in cond['product_id'].values and y not in cond['product_id'].values:
        print(f"\nProduct pair (x in cond, y not in cond): {x}, {y}")
        list.append((x, y))  # Append the pair to the list
        # Calculate and print the total profit/loss of the pair
        pair_profit_loss = int(loss_s[loss_s['product_id'] == x]['Average_daily_profit_loss']) + \
                           int(loss_s[loss_s['product_id'] == y]['Average_daily_profit_loss'])
        print(f"Total profit/loss for this pair: {pair_profit_loss}")
        # Store the number of boxes for product 'y' (not in 'cond')
        boxes.append(int(loss_s[loss_s['product_id'] == y]['boxes']))
        list_y.append(y)  # Append 'y' to the list of y-products
        loss_y.append(int(loss_s[loss_s['product_id'] == y]['Average_daily_profit_loss']))  # Add 'y' loss

    # Check if 'y' is in the filtered set (cond) but 'x' is not
    if y in cond['product_id'].values and x not in cond['product_id'].values:
        print(f"\nProduct pair (y in cond, x not in cond): {x}, {y}")
        list.append((x, y))  # Append the pair to the list
        # Calculate and print the total profit/loss of the pair
        pair_profit_loss = int(loss_s[loss_s['product_id'] == x]['Average_daily_profit_loss']) + \
                           int(loss_s[loss_s['product_id'] == y]['Average_daily_profit_loss'])
        print(f"Total profit/loss for this pair: {pair_profit_loss}")
        # Store the number of boxes for product 'x' (not in 'cond')
        boxes.append(int(loss_s[loss_s['product_id'] == x]['boxes']))
        list_x.append(x)  # Append 'x' to the list of x-products
        loss_x.append(int(loss_s[loss_s['product_id'] == x]['Average_daily_profit_loss']))  # Add 'x' loss

# Print the number of valid pairs and the pairs themselves
print(f"\nTotal number of product pairs found: {len(list)}")
print("List of product pairs:")
print(list)

# Print the number of boxes for unselected products in the pairs
print("\nBoxes corresponding to unselected products in the pairs:")
print(boxes)

# Print the total number of boxes for unselected products
print(f"\nTotal boxes for unselected products: {sum(boxes)}")

# Further refine the filtered set by focusing on products with cumulative boxes > 921
cond1 = cond.where(loss_s['cumsum'] > 921).dropna()  # Products with cumsum > 921
cond2 = cond.where(loss_s['cumsum'] < 921).dropna()  # Products with cumsum < 921
cond1 = cond1.reset_index()  # Reset index of cond1

# Print the refined products in cond1 (cumsum > 921)
print("\nProducts with cumulative boxes greater than 921:")
print(cond1)

# Loop over each pair (m, n) and check if one of them is in cond1
for m, n in list:
    if (m or n) in cond1['product_id'].values:
        print(f"\nPair where one product is in cond1 (cumsum > 921): {m}, {n}")

# Filter products in loss_s with cumsum > 921 and print them
cond3 = loss_s.where(loss_s['cumsum'] > 921).dropna()
print("\nProducts with cumulative sum of boxes greater than 921:")
print(cond3)

# Calculate the remaining profit/loss excluding certain pairs (subtract sums of loss_x and loss_y)
remaining_profit_loss = cond3['Average_daily_profit_loss'].sum() - sum(loss_y) - sum(loss_x)

# Print the final adjusted profit/loss
print(f"\nRemaining profit/loss after adjustments: {remaining_profit_loss}")