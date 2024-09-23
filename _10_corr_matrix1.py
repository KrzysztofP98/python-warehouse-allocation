from datetime import datetime  # Importing datetime module
from elasticsearch import Elasticsearch  # Importing Elasticsearch for database interactions
import json  # Importing json for handling JSON data
import pandas as pd  # Importing pandas for data manipulation
import matplotlib.pyplot as plt  # Importing matplotlib for plotting
import numpy as np  # Importing numpy for numerical operations
import csv  # Importing csv for CSV file handling
from statistics import mean  # Importing mean function for statistics
import seaborn as sns  # Importing seaborn for enhanced plotting
from math import sqrt  # Importing sqrt function for mathematical operations
from adjustText import adjust_text  # Importing adjust_text for improving text placement in plots

# Load data from CSV files into pandas DataFrames
array = pd.read_csv('Array.csv')
id = pd.read_csv('Products.csv')

# Drop every second row from the array DataFrame
array = array.drop(index=array.index[1::2])
# Remove unnamed columns from the DataFrame
array = array.loc[:, ~array.columns.str.contains('^Unnamed')]
# Reset the index of the DataFrame
array = array.reset_index()
# Drop the old index column
array = array.drop(labels='index', axis=1)

# Print the first transformation of the DataFrame
print('first:', array)
# Transpose the DataFrame for analysis
array = array.transpose()

# Print the transposed DataFrame
print('second', array)
# Calculate the correlation matrix of the DataFrame
corr_matrix = array.corr()

# Print the number of columns in the correlation matrix
print(corr_matrix.shape[1])  # Number of columns in corr_matrix
# Print the length of the 'key' column in id DataFrame
print(len(id['key']))          # Length of id['key']

# Set the index of the correlation matrix to the 'key' from id DataFrame
corr_matrix.index = index=id['key']

# Print the correlation matrix
print(corr_matrix)

# Insert 'product_id' column at the start of the correlation matrix
column = id['key']
corr_matrix.insert(0, 'product_id', column)

# Create a boolean DataFrame indicating correlations >= 0.6 and < 1
a = (corr_matrix.ge(0.6) & corr_matrix.lt(1))

# Get the indices of True values in the boolean DataFrame
i, c = np.where(a==True)
print('i,c', i, c)

# Create a list of product pairs based on the indices
L = list(zip(a.index[i], a.columns[c]))
print('list L:', L)

# Load product classes from CSV into a DataFrame
pc = pd.read_csv('product_classes.csv')
# Create a heatmap of the correlation matrix
ax = sns.heatmap(corr_matrix, cmap=sns.cubehelix_palette(as_cmap=True), vmin=0, vmax=1)
ax.set(xlabel="product ids", ylabel="product ids")

# Initialize lists to hold product couples and annotations
couples = []
texts = []
# Iterate over the product pairs
for x, y in L:
    # m, n stand for product classes of the first and the second product respectively in a couple
    m = int(pc[pc['product_id'] == x]['product_class'])  # Class of first product
    n = int(pc[pc['product_id'] == y]['product_class'])  # Class of second product

    # Append the couple if the first product class is less than the second
    if m < n:
        couples.append(tuple((x, y)))  # Add the couple to the list
        plt.scatter(x, y, facecolors='black', alpha=.5, s=10)  # Plot the point
        plt.annotate((x, y), (x, y), size=5)  # Annotate the point

        # Store annotation text for adjustment
        texts.append(plt.annotate((x, y), (x, y), size=5))

# Save the plot
plt.savefig("correlation_matrix_annotations.png")
# Print the identified product couples
print('product couples:', couples)
