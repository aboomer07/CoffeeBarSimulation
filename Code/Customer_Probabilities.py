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

DataPath = os.path.abspath('..') + \
           "/Data/Coffeebar_2016-2020.csv"

df = pd.read_csv(DataPath, sep=";")
################################################################################

################################################################################
# Perform initial data manipulation
df['TIME'] = pd.to_datetime(df['TIME'], format="%Y-%m-%d %H:%M:%S")
df['HOUR'] = df['TIME'].dt.hour  # Get Hour Integer
df['MINUTE'] = df['TIME'].dt.minute  # Get Minute Integer
df['YEAR'] = df['TIME'].dt.year  # Get Year Integer

df['FOOD'] = df['FOOD'].fillna("nothing")  # A null value means no food ordered
################################################################################

################################################################################
# What food and drink are sold?
DrinkList = df['DRINKS'].unique()  # Get the unique list of possible drinks
FoodList = df['FOOD'].unique()  # Get unique list of possible food items

# How many unique customers did the bar have?
CustomerList = df['CUSTOMER'].unique()  # Unique set of customers ID's
################################################################################

################################################################################
# Calculating Probabilities For Food and Drinks per 5-Minute Interval
# Use Value Counts to Calculate
FoodProbs = df.groupby(['HOUR', 'MINUTE'])['FOOD']. \
    value_counts(normalize=True). \
    unstack(fill_value=0). \
    reset_index(). \
    rename_axis(None, axis=1)

DrinkProbs = df.groupby(['HOUR', 'MINUTE'])['DRINKS']. \
    value_counts(normalize=True). \
    unstack(fill_value=0). \
    reset_index(). \
    rename_axis(None, axis=1)
################################################################################
