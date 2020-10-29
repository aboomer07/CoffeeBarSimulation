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

# Print the unique foods that the bar sells with a join statement
print('The foods the bar sells are ' +
      ", ".join([x for x in FoodList if x != 'nothing']))

# Print the unique drinks the bar sells with a join
print('The drinks the bar sells are ' + ", ".join(DrinkList))

# How many unique customers did the bar have?
CustomerList = df['CUSTOMER'].unique()  # Unique set of customers ID's
print("There are " + str(len(CustomerList)) +
      " unique customers who have ever attended this bar")
################################################################################

################################################################################
# Calculating Probabilities For Food and Drinks per 5-Minute Interval
# Use Value Counts Function to Calculate the Probabilities for Each Food Item
#		And Each Drink. Unstack to Create Columns Per Item/Drink

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

################################################################################
# Initial Count Plots
fig, axes = plt.subplots(nrows=1, ncols=2)

# Plot 1: Total Amount of Sold Foods
FoodCount = sns.countplot(x='FOOD', data=df, ax=axes[0])

# Plot 2: Total Amount of Sold Drinks
DrinkCount = sns.countplot(x='DRINKS', data=df, ax=axes[1])
plt.show()
################################################################################

################################################################################
# Percentage for Each Food/Drink at a Given Time of Day
FoodProbs['Time'] = FoodProbs['HOUR'].apply(str) + ':' + \
                    np.where(FoodProbs['MINUTE'] < 10, "0" + FoodProbs['MINUTE'].apply(str),
                             FoodProbs['MINUTE'].apply(str))

fig, ax = plt.subplots(nrows=1, ncols=1)

plt.stackplot(FoodProbs['Time'],
              *[FoodProbs[col] for col in FoodList],
              labels=list(FoodList))
ax.legend(loc='upper left')
plt.xticks(rotation=45)
ax.xaxis.set_major_locator(plt.MaxNLocator(14))
plt.show()

DrinkProbs['Time'] = DrinkProbs['HOUR'].apply(str) + ':' + \
                     np.where(DrinkProbs['MINUTE'] < 10, "0" + DrinkProbs['MINUTE'].apply(str),
                              DrinkProbs['MINUTE'].apply(str))

fig, ax = plt.subplots(nrows=1, ncols=1)

plt.stackplot(DrinkProbs['Time'],
              *[DrinkProbs[col] for col in DrinkList],
              labels=list(DrinkList))
ax.legend(loc='upper left')
plt.xticks(rotation=45)
ax.xaxis.set_major_locator(plt.MaxNLocator(14))
plt.show()
################################################################################

################################################################################
# Distribution of Revenue by Customers
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}

df['FoodRevenue'] = df['FOOD'].map(menu)
df['DrinkRevenue'] = df['DRINKS'].map(menu)
df['Revenue'] = df['FoodRevenue'] + df['DrinkRevenue']

RevFrame = df.groupby('CUSTOMER', as_index=False)['Revenue'].sum()

CumRev = RevFrame['Revenue'].sort_values().cumsum(). \
    reset_index(drop=True).reset_index()

CumRev['index'] = CumRev['index'] / CumRev['index'].tail(1).values[0]
CumRev['Revenue'] = CumRev['Revenue'] / CumRev['Revenue'].tail(1).values[0]

plt.plot(CumRev['index'], CumRev['Revenue'])
plt.plot(CumRev['index'], CumRev['index'])
plt.show()
################################################################################

################################################################################
# Mean Time between visits from returning customers
TimeFrame = df[df['CUSTOMER'].duplicated()]. \
    sort_values(by=['CUSTOMER', 'TIME'])
TimeFrame['TimeDiff'] = TimeFrame['TIME']. \
    subtract(TimeFrame.groupby('CUSTOMER')['TIME'].shift()). \
    apply(lambda x: np.float(x.value) / (3600 * 24 * 1000000000))
TimeFrame['TimeDiff'] = np.where(TimeFrame['TimeDiff'] < 0,
                                 np.nan, TimeFrame['TimeDiff'])
plt.plot(sorted(TimeFrame.groupby('CUSTOMER')['TimeDiff'].mean().values))
plt.show()
################################################################################

################################################################################
# Percentage of One Time Customers by Year and Month
df['OneTime'] = np.where(df['CUSTOMER'].isin(TimeFrame['CUSTOMER'].unique()),
                         0, 1)
df['Month'] = df['TIME'].dt.month
df['YearMonth'] = df.apply(lambda x: datetime.date(x['YEAR'], x['Month'], 1), axis=1)
OneTime = df.groupby(['YEAR', 'Month'], as_index=False)['OneTime'].mean()
sns.lineplot(data=OneTime, x='Month', y='OneTime', style='YEAR')
################################################################################
