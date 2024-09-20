from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the count and stats data from CSV files (using relative paths for GitHub compatibility)
count = pd.read_csv("count.csv")
stats = pd.read_csv("demand_final.csv")

# Extract the 'averageDemand' and 'StandardDeviation' columns from stats
extracted_col = stats['averageDemand']
extracted_col1 = stats['StandardDeviation']

# Add the extracted columns to the 'count' DataFrame
count['averageDemand'] = extracted_col
count['StandardDeviation'] = extracted_col1

# Sort the DataFrame by 'averageDemand' in descending order
count_sorted = count.sort_values(by=['averageDemand'], ascending=False)

# Save the sorted DataFrame to a CSV file (using a relative path)
count_sorted.to_csv('stats.csv')

# Print the sorted DataFrame to check the results
print(count_sorted)

# Print the 'averageDemand' column to inspect the data
print(count_sorted['averageDemand'])

# Create a NumPy array of integers for the x-axis (1263 products)
print(np.arange(1263))

# Print the top 12 rows of the sorted DataFrame as a sample check
print(count_sorted[:12])

# Load the newly saved stats.csv file into a new DataFrame (relative path)
new = pd.read_csv("stats.csv")

# Set up data for the plot: y-values are 'averageDemand' and error bars are 'StandardDeviation'
y = new['averageDemand']
y_error = new['StandardDeviation']

# Plot the error bars with the 'averageDemand' data
plt.errorbar(np.arange(1263), y, yerr=y_error, lolims=False, uplims=False,
             xlolims=False, xuplims=False, errorevery=1, marker='o', ls='None')

# Label the x-axis and y-axis
plt.xlabel('Products')
plt.ylabel('Average daily demand')

# Save the plot as a PNG file (using relative path)
plt.savefig('errorbar.png')

# Display the plot
plt.show()
