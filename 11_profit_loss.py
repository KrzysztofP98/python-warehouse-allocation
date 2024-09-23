from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import mean
import seaborn as sns
from math import sqrt

pc = pd.read_csv('C:/Users/krzys/Desktop/final/product_classes.csv')

pc = pc.loc[:, ~pc.columns.str.contains('^Unnamed')]

pc.loc[pc['product_class'] == 1, 'Average_daily_profit_loss'] = 0.2 * pc['Average_daily_profit']
pc.loc[pc['product_class'] == 2, 'Average_daily_profit_loss'] = 0.3 * pc['Average_daily_profit']
pc.loc[pc['product_class'] == 3, 'Average_daily_profit_loss'] = 0.5 * pc['Average_daily_profit']


pc.to_csv('Average_daily_profit_loss.csv')
