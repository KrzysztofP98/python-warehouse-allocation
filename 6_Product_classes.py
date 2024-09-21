# Importing necessary libraries for working with dates, Elasticsearch, data manipulation, plotting, etc.
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import mean  # Used to calculate the mean of profits per class
import seaborn as sns  # Useful for advanced data visualizations
from adjustText import adjust_text  # Helps avoid overlapping text in plots

# Load the CSV file with average daily profits into a pandas DataFrame
new = pd.read_csv('C:/Users/krzys/Desktop/final/average_daily_profits.csv')

# Display the DataFrame to check the loaded data
print(new)

# Calculate the 80th and 50th percentiles (quantiles) for the 'Average_daily_profit' column.
top = new['Average_daily_profit'].quantile([0.8])  # Store the 80th percentile for reference
print(new['Average_daily_profit'].quantile([0.8, 0.5]))  # Print both 80th and 50th percentiles

# Categorizing products into classes based on their average daily profits.
# Class 1: Top 20% products (profit >= 165.877165)
new.loc[(new['Average_daily_profit']) >= 165.877165, 'product_class'] = 1
# Class 2: Middle range products (between 67.684317 and 165.877165)
new.loc[(165.877163 > new['Average_daily_profit']) & (new['Average_daily_profit'] >= 67.684317), 'product_class'] = 2
# Class 3: Bottom products (profit < 67.684317)
new.loc[(67.684317 > new['Average_daily_profit']), 'product_class'] = 3

# Display the DataFrame with the newly created 'product_class' column
print(new)

# Save the DataFrame with product classes to a new CSV file
new.to_csv('product_classes.csv')

# --- Creation of product class lists ---

# Extracting product IDs that belong to product class 1 (top products)
A = new[new['product_class'] == 1]
list_a = A['product_id'].values.tolist()  # Convert the product_id column to a list

# Extracting product IDs that belong to product class 2 (middle products)
B = new[new['product_class'] == 2]
list_b = B['product_id'].values.tolist()

# Extracting product IDs that belong to product class 3 (bottom products)
C = new[new['product_class'] == 3]
list_c = C['product_id'].values.tolist()

# Print the lists of product IDs for each class
print('\nlist of top products:', list_a, '\n\nlist of middle products:', list_b, '\n\nlist of bottom products:', list_c)

# Print the number of products in each class
print('length:', len(list_a), len(list_b), len(list_c))

# Create a dictionary to store the number of products in each class
dict0 = {'1': len(list_a), '2': len(list_b), '3': len(list_c)}

# Prepare data for plotting
classes = list(dict0.keys())
numbers = list(dict0.values())

# Create a bar plot to show the number of products in each class
plt.bar(classes, numbers, color='maroon', width=0.4)
plt.xlabel("Product Classes")  # Label for the x-axis
plt.ylabel("Number of products in a given class")  # Label for the y-axis
plt.title("Number of Products within product classes")  # Plot title
plt.savefig("products_class_bar.png")  # Save the plot as a PNG file

# --- Analyzing profits for each class ---

# Extract the average daily profits for class 1 products (top class)
p_a = A['Average_daily_profit'].values.tolist()
i_a = A.index.values.tolist()  # Extract the index values for class 1 products
print('index:', i_a)  # Print the indices of class 1 products

# Extract the average daily profits for class 2 products (middle class)
p_b = B['Average_daily_profit'].values.tolist()

# Extract the average daily profits for class 3 products (bottom class)
p_c = C['Average_daily_profit'].values.tolist()

# Calculate and print the mean (average) daily profits for each class
print(mean(p_a), mean(p_b), mean(p_c))

# Create a dictionary to store the mean profits for each class
dict1 = {'1': mean(p_a), '2': mean(p_b), '3': mean(p_c)}

# Prepare data for plotting
classes1 = list(dict1.keys())
averages = list(dict1.values())

# Create a bar plot to show the average profits per class
plt.bar(classes1, averages, color='maroon', width=0.4)
plt.xlabel("Product Classes")  # Label for the x-axis
plt.ylabel("Average Profits per Class")  # Label for the y-axis
plt.title("Average Profits per Class")  # Plot title
plt.savefig("average_profits_per_class.png")

# Create a dictionary to store the profits per product in each class
dict2 = {'1': p_a, '2': p_b, '3': p_c}
print(p_a)  # Print the profits for class 1 products

# --- Assigning colors to products based on their class ---

# Define conditions for assigning colors: class 3 -> blue, class 2 -> yellow, class 1 -> red
conditions = [new['product_class'] == 3, new['product_class'] == 2, new['product_class'] == 1]
choices = ['blue', 'yellow', 'red']

# Apply the color choices to a new 'color' column in the DataFrame
new['color'] = np.select(conditions, choices, default='')

# Create a bar plot showing the average daily profit for each product, colored by class
plt.bar(new.index, new['Average_daily_profit'], color=new['color'], width=0.4)
plt.xlabel("Products")  # Label for the x-axis
plt.ylabel("Profits per Product")  # Label for the y-axis
plt.title("Average Profits per Product")  # Plot title
plt.savefig("average_proftis_per_product.png")

# --- Adding annotations to the plot ---

# Create an empty list to hold the annotation text objects
annotations = []

# Add annotations for some specific products (one from each class) with product ID and profit
annotations.append(plt.annotate(('id:', list_a[-1], round(p_a[-1], 2)), (A.index[-1], p_a[-1])))  # Last product in class 1
annotations.append(plt.annotate(('id:', list_b[0], round(p_b[0], 2)), (B.index[0], p_b[0])))  # First product in class 2
annotations.append(plt.annotate(('id:', list_b[-1], round(p_b[-1], 2)), (B.index[-1], p_b[-1])))  # Last product in class 2
annotations.append(plt.annotate(('id:', list_c[0], round(p_c[0], 2)), (C.index[0], p_c[0])))  # First product in class 3

# Adjust the text annotations to avoid overlap
adjust_text(annotations, only_move={'points': 'xy', 'texts': 'y', 'objects': 'y'}, arrowprops=dict(arrowstyle="->", color='r'))

# --- Adding a legend for the product classes ---

# Define the class-color relationship in a dictionary
cl = {'Class 1': 'red', 'Class 2': 'yellow', 'Class 3': 'blue'}

# Create legend handles with colored rectangles for each class
labels = list(cl.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=cl[label]) for label in labels]

# Add the legend to the plot
plt.legend(handles, labels)

# Save the final plot with annotations and legend
plt.savefig("average_proftis_per_product_annotated.png")
