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
import datetime
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
# What food and drink are sold?
drink_list = df['drinks'].unique()  # Get the unique list of possible drinks
food_list = df['food'].unique()  # Get unique list of possible food items

# Print the unique foods that the bar sells with a join statement
print('The foods the bar sells are ' +
      ", ".join([x for x in food_list if x != 'nothing']))

# Print the unique drinks the bar sells with a join
print('The drinks the bar sells are ' + ", ".join(drink_list))

# How many unique customers did the bar have?
customerList = df['customer'].unique()  # Unique set of customers ID's
print("There are " + str(len(customerList)) +
      " unique customers who have ever attended this bar")
################################################################################

################################################################################
# Calculating Probabilities For Food and Drinks per 5-minute Interval
# Use Value Counts Function to Calculate the Probabilities for Each Food Item
#		And Each Drink. Unstack to Create Columns Per Item/Drink

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

################################################################################
# Initial Count Plots
fig, axes = plt.subplots(nrows=1, ncols=2)

# Plot 1: Total Amount of Sold Foods
food_count = sns.countplot(x='food', data=df, ax=axes[0])

# Plot 2: Total Amount of Sold Drinks
drink_count = sns.countplot(x='drinks', data=df, ax=axes[1])
plt.show()
################################################################################

################################################################################
# Percentage for Each Food/Drink at a Given time of Day
food_probs['time'] = food_probs['hour'].apply(str) + ':' + \
                    np.where(food_probs['minute'] < 10, "0" + food_probs['minute'].apply(str),
                             food_probs['minute'].apply(str))

fig, ax = plt.subplots(nrows=1, ncols=1)

plt.stackplot(food_probs['time'],
              *[food_probs[col] for col in food_list],
              labels=list(food_list))
ax.legend(loc='upper left')
plt.xticks(rotation=45)
ax.xaxis.set_major_locator(plt.MaxNLocator(14))
plt.show()

drink_probs['time'] = drink_probs['hour'].apply(str) + ':' + \
                     np.where(drink_probs['minute'] < 10, "0" + drink_probs['minute'].apply(str),
                              drink_probs['minute'].apply(str))

fig, ax = plt.subplots(nrows=1, ncols=1)

plt.stackplot(drink_probs['time'],
              *[drink_probs[col] for col in drink_list],
              labels=list(drink_list))
ax.legend(loc='upper left')
plt.xticks(rotation=45)
ax.xaxis.set_major_locator(plt.MaxNLocator(14))
plt.show()
################################################################################

################################################################################
# Distribution of revenue by customers
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}

df['food_revenue'] = df['food'].map(menu)
df['drink_revenue'] = df['drinks'].map(menu)
df['revenue'] = df['food_revenue'] + df['drink_revenue']

rev_frame = df.groupby('customer', as_index=False)['revenue'].sum()

cum_rev = rev_frame['revenue'].sort_values().cumsum(). \
    reset_index(drop=True).reset_index()

cum_rev['index'] = cum_rev['index'] / cum_rev['index'].tail(1).values[0]
cum_rev['revenue'] = cum_rev['revenue'] / cum_rev['revenue'].tail(1).values[0]

plt.plot(cum_rev['index'], cum_rev['revenue'])
plt.plot(cum_rev['index'], cum_rev['index'])
plt.show()
################################################################################

################################################################################
# Mean time between visits from returning customers
time_frame = df[df['customer'].duplicated()]. \
    sort_values(by=['customer', 'time'])
time_frame['time_diff'] = time_frame['time']. \
    subtract(time_frame.groupby('customer')['time'].shift()). \
    apply(lambda x: np.float(x.value) / (3600 * 24 * 1000000000))
time_frame['time_diff'] = np.where(time_frame['time_diff'] < 0,
                                 np.nan, time_frame['time_diff'])
plt.plot(sorted(time_frame.groupby('customer')['time_diff'].mean().values))
plt.show()
################################################################################

################################################################################
# Percentage of One time customers by year and month
df['onetime'] = np.where(df['customer'].isin(time_frame['customer'].unique()),
                         0, 1)
df['month'] = df['time'].dt.month
df['yearmonth'] = df.apply(lambda x: datetime.date(x['year'], x['month'], 1), axis=1)
onetime = df.groupby(['year', 'month'], as_index=False)['onetime'].mean()
sns.lineplot(data=onetime, x='month', y='onetime', style='year')
################################################################################
