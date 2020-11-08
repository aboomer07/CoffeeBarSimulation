################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 1 involves exploring sample coffee dataset, creating probabilities
################################################################################

################################################################################
# Importing Libraries and Datafile
import numpy as np
import pandas as pd
import re
import os
import sys

data_path = os.path.abspath('..') + \
    "/Data/Coffeebar_2016-2020.csv"

df = pd.read_csv(data_path, sep=";")
################################################################################

################################################################################
# change column names to follow pep8
df.columns = ['time', 'customer', 'drinks', 'food']

# Perform initial data manipulation
df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%d %H:%M:%S")
df['hour'] = df['time'].dt.hour  # Get hour Integer
df['minute'] = df['time'].dt.minute  # Get minute Integer
df['year'] = df['time'].dt.year  # Get year Integer

df['food'] = df['food'].fillna("nothing")  # A null value means no food ordered
################################################################################

################################################################################

# Get the unique list of drinks
drink_list = np.sort(np.array(df['drinks'].unique()))
# Get unique list of food items
food_list = np.sort((np.array(df['food'].unique())))

################################################################################

################################################################################
# Calculating Probabilities For food and drinks per 5-minute Interval
# Use Value Counts to Calculate
food_probs = df.groupby(['hour', 'minute'])['food']. \
    value_counts(normalize=True). \
    unstack(fill_value=0). \
    reset_index(). \
    rename_axis(None, axis=1)

drink_probs = df.groupby(['hour', 'minute'])['drinks']. \
    value_counts(normalize=True). \
    unstack(fill_value=0). \
    reset_index(). \
    rename_axis(None, axis=1)
################################################################################
