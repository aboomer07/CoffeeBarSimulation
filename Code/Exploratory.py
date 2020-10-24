################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 1 involves exploring sample coffee dataset, creating probabilities
################################################################################

################################################################################
# Importing Libraries and Datafile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import sys

data_path = os.path.abspath('..') + \
	"/Data/Coffeebar_2016-2020.csv"

df = pd.read_csv(data_path, sep = ";")
################################################################################

################################################################################
# Perform initial data manipulation
df['TIME'] = pd.to_datetime(df['TIME'], format = "%Y-%m-%d %H:%M:%S")
df['HOUR'] = df['TIME'].dt.hour
df['MINUTE'] = df['TIME'].dt.minute
df['YEAR'] = df['TIME'].dt.year

df['FOOD'] = df['FOOD'].fillna("nothing")
################################################################################

################################################################################
# What food and drink are sold?
drink_list = df['DRINKS'].unique()
food_list = df['FOOD'].unique()

# How many unique customers did the bar have?
customer_list = df['CUSTOMER'].unique()
################################################################################

################################################################################
# Plot 1: Total Amount of Sold Foods
food_count = sns.countplot(x = 'FOOD', data = df)
plt.show()

# Plot 2: Total Amount of Sold Drinks
drink_count = sns.countplot(x = 'DRINKS', data = df)
plt.show()
################################################################################

################################################################################
# Calculating Probabilities For Food and Drinks per 5-Minute Interval
food_probs = df.groupby(['HOUR', 'MINUTE', 'FOOD'], 
	as_index = False).count()
food_probs = food_probs[['HOUR', 'MINUTE', 'FOOD', 'TIME']]
food_probs = food_probs.rename({"TIME" : "COUNT"}, axis = 1)
food_probs = food_probs.set_index(['HOUR', 'MINUTE', 'FOOD']).unstack('FOOD')
# food_probs = food_probs.pivot(index=['HOUR', 'MINUTE'], columns='FOOD', values='COUNT') this threw an error
food_probs = food_probs.fillna(0)
food_probs['total'] = food_probs.sum(axis=1)
#food_probs.columns.name = None
food_probs.reset_index(inplace=True)
food_probs.columns = ['HOUR', 'MINUTE', 'cookie', 'muffin', 'nothing', 'pie', 'sandwich', 'total']
food_probs[food_list] = food_probs[food_list].div(food_probs['total'], axis=0)
food_probs['max_prob'] = food_probs[food_list].idxmax(axis=1)


# drink_probs = df.groupby(['HOUR', 'MINUTE', 'FOOD'],
# 	as_index = False).count()
# drink_probs = drink_probs[['HOUR', 'MINUTE', 'FOOD', 'TIME']]
# drink_probs = drink_probs.rename({"TIME" : "COUNT"}, axis = 1)
# drink_probs = drink_probs.pivot(index = ['HOUR', 'MINUTE'], columns = 'FOOD',
# 	values = 'COUNT')
# drink_probs = drink_probs.fillna(0)
# drink_probs['total'] = drink_probs.sum(axis = 1)
# drink_probs[drink_list] = drink_probs[drink_list].div(drink_probs['total'],
# 	axis = 0)
# drink_probs.columns.name = None
# drink_probs.reset_index(inplace = True)
################################################################################






