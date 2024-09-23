from gurobipy import Model, GRB, quicksum
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import matplotlib.pyplot as plt

# Read the ratio CSV
ratio = pd.read_csv('ratio.csv')

# Extract the relevant columns
P = ratio['Average_daily_profit'].values.tolist()
W = (ratio['ratio'] / 100).values.tolist()
B = ratio['boxes'].values.tolist()

# Initialize the model
m = Model("product mix")

# Number of items
num_items = len(B)

# Variables: x[j] is binary, representing whether each item is selected
x = m.addVars(num_items, vtype=GRB.BINARY, name='stay')

# Constraint: Total boxes should not exceed 960 for each item
m.addConstr(quicksum(B[i] * x[i] for i in range(num_items)) <= 960)

# Objective: Maximize the weighted profit
m.setObjective(quicksum(W[i] * P[i] * x[i] for i in range(num_items)), GRB.MAXIMIZE)

# Optimize the model
m.optimize()

# Print the results
for v in m.getVars():
    print("%s is: %g" % (v.varName, v.x))

print("Objective total minimum capacity is: %g" % m.objVal)
