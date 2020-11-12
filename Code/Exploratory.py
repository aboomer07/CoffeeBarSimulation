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

# Force the correct directory
if os.getcwd().split("/")[-1] == "Code":
    os.chdir("..")

curr_dir = os.getcwd()
output_dir = curr_dir + "/Output"

data_path = curr_dir + "/Data/Coffeebar_2016-2020.csv"

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
#   And Each Drink. Unstack to Create Columns Per Item/Drink
food_probs = df.groupby(['hour', 'minute'])['food'].value_counts(
    normalize=True).unstack(fill_value=0).reset_index().rename_axis(None, axis=1)

drink_probs = df.groupby(['hour', 'minute'])['drinks'].value_counts(
    normalize=True).unstack(fill_value=0).reset_index().rename_axis(None, axis=1)
################################################################################

################################################################################
# Initial Count Plots
fig, axes = plt.subplots(nrows=1, ncols=2)

# Plot 1: Total Amount of Sold Foods
food_count = sns.countplot(x='food', data=df, ax=axes[0])
axes[0].set_title("Count of Food Purchases in 5-Year Period")

# Plot 2: Total Amount of Sold Drinks
drink_count = sns.countplot(x='drinks', data=df, ax=axes[1])
axes[1].set_title("Count of Drinks Purchases in 5-Year Period")
plt.savefig(output_dir + "/ExploratoryCountPlot.png")
plt.close()
################################################################################

################################################################################
# Percentage for Each Food/Drink at a Given time of Day
food_probs['time'] = food_probs['hour'].apply(str) + ':' + \
    np.where(food_probs['minute'] < 10, "0" + food_probs['minute'].apply(str),
             food_probs['minute'].apply(str))

# Create the matplotlib figure
fig, ax = plt.subplots(nrows=1, ncols=1)

# Create the stackplot, with the time variable on x, and food columns as y's
plt.stackplot(food_probs['time'],
              *[food_probs[col] for col in food_list],
              labels=list(food_list))
plt.legend(loc='upper left')  # Get a legend for the plot
plt.xticks(rotation=45)  # Rotate the x axis ticks for ease of viewing
ax.xaxis.set_major_locator(plt.MaxNLocator(14))
# Set the title and show the plot
ax.set_title("Proportion of Food Items Purchased Throughout a Day")
ax.set_xlabel("Time of Day")  # Set x-axis title
ax.set_ylabel("Percentage of Food Purchases")  # Set y-axis title
plt.savefig(output_dir + "/ExploratoryFoodProb.png")
plt.close()

# Get the time variable for to be used in the graph
drink_probs['time'] = drink_probs['hour'].apply(str) + ':' + \
    np.where(drink_probs['minute'] < 10, "0" + drink_probs['minute'].apply(str),
             drink_probs['minute'].apply(str))

# Create the matplotlib figure
fig, ax = plt.subplots(nrows=1, ncols=1)

# Create the stackplot, with the time variable on x, and drink columns as y's
plt.stackplot(drink_probs['time'],
              *[drink_probs[col] for col in drink_list],
              labels=list(drink_list))
ax.legend(loc='upper left')  # Get the legend
plt.xticks(rotation=45)  # Rotate the x axis ticks
ax.xaxis.set_major_locator(plt.MaxNLocator(14))
# Set the title and show the plot
ax.set_title("Proportion of Drinks Purchased Throughout a Day")
ax.set_xlabel("Time of Day")  # Set x-axis title
ax.set_ylabel("Percentage of Drink Purchases")  # Set y-axis title
plt.savefig(output_dir + "/ExploratoryDrinkProb.png")
plt.close()
################################################################################

################################################################################
# Distribution of revenue by customers
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}

# Use the map function to map the dictionary keys onto the food column
df['food_revenue'] = df['food'].map(menu)
# Use the map function to map the dictionary keys onto the drink column
df['drink_revenue'] = df['drinks'].map(menu)
# Get the total revenue based on the food revenue and drink revenue
df['revenue'] = df['food_revenue'] + df['drink_revenue']

# Get the total amount spent over the five years per unique customer
rev_frame = df.groupby('customer', as_index=False)['revenue'].sum()

# Get the cumulative revenue at each customer, sorted to get a cumulative curve
cum_rev = rev_frame['revenue'].sort_values().\
    cumsum().reset_index(drop=True).reset_index()

# Get the percentage of the max for the index and for the revenue
cum_rev['index'] = cum_rev['index'] / cum_rev['index'].tail(1).values[0]
cum_rev['revenue'] = cum_rev['revenue'] / cum_rev['revenue'].tail(1).values[0]

# Initialize the figure
fig, ax = plt.subplots(nrows=1, ncols=1)
# Plot the curve (similar to gini inequality curve)
plt.plot(cum_rev['index'], cum_rev['revenue'],
         label="Cumulative Revenue Sum")
# Plot a 45 degree line for reference, then show the plot
plt.plot(cum_rev['index'], cum_rev['index'], label="45 Degree Line")
plt.legend(loc="upper left")
ax.set_title("Inequality Distribution of Total Spending by Customer")
ax.set_xlabel("Percentile of Customer Index")  # Set x-axis title
ax.set_ylabel("Percentile of Total Revenue")  # Set y-axis title
plt.savefig(output_dir + "/ExploratoryRevenueGini.png")
plt.close()
################################################################################

################################################################################
# Mean time between visits from returning customers
# Get only the customers who have visited more than once
time_frame = df[df['customer'].duplicated()].\
    sort_values(by=['customer', 'time'])

# Find the number of days (as a float) between visits for returning customers
time_frame['time_diff'] = time_frame['time'].\
    subtract(time_frame.groupby('customer')['time'].shift()).apply(
        lambda x: np.float(x.value) / (3600 * 24 * 1000000000))

# There is one value to remove from subtracting with the Nan in the first row
time_frame['time_diff'] = np.where(time_frame['time_diff'] < 0,
                                   np.nan, time_frame['time_diff'])

# Initialize the figure
fig, ax = plt.subplots(ncols=1, nrows=1)

# Calculate the mean time difference and plot it
plt.plot(sorted(time_frame.groupby('customer')['time_diff'].mean().values))
# Set title and show the plot
ax.set_title("Mean Time Between Visits for Returning Customers")
ax.set_xlabel("Ordered Index of Returning Customers")  # Set x-axis title
ax.set_ylabel("Mean Time Between Visits (Days)")  # Set y-axis title
plt.savefig(output_dir + "/ExploratoryMeanTime.png")
plt.close()
################################################################################

################################################################################
# Percentage of One time customers by year and month
# Use the time frame specified above to categorize returning customers
df['onetime'] = np.where(df['customer'].isin(time_frame['customer'].unique()),
                         0, 1)
df['returning'] = np.where(df['onetime'] == 0, 1, 0)
df['customer_type'] = np.where(df['onetime'] == 1, 'onetime', 'returning')

# Get the month to be used in the plot
df['month'] = df['time'].dt.month

# Calculate the mean of the one time dummy variable to get the percentage
onetime = df.groupby(['year', 'month'], as_index=False)['onetime'].mean()

# Initialize the plot
fig, ax = plt.subplots(ncols=1, nrows=1)

# Plot the percentage, with different lines as the years
sns.barplot(data=onetime, x='month', y='onetime',
            hue='year', ax=ax)
# Set title and show the plot
ax.set_title("Proportion of One Time Customers Per Month and Year")
plt.savefig(output_dir + "/ExploratoryOneTimePct.png")
plt.close()
################################################################################

################################################################################
# Additional exploratory questions from part 4
# In the provided data set there are actual returning customers. How
# many? Do they have specific times when they show up more?
returning_prob = df.groupby(['hour', 'minute'], as_index=False)[
    'returning'].mean()

# Initialize the plot
fig, ax = plt.subplots(ncols=1, nrows=1)

# Plot probabilities of returning customers over a day
sns.lineplot(data=returning_prob, x='hour', y='returning', ax=ax)
ax.set_title("Proportion of Regular Customers during a Day")
plt.savefig(output_dir + "/ExploratoryReturningDailyPct.png")
plt.close()

# How does this impact their buying history?
food_probs_type = df.groupby(['hour', 'minute', 'customer_type'])['food'].value_counts(
    normalize=True).unstack(fill_value=0).reset_index().rename_axis(None, axis=1)
# wide to long
food_probs_type = food_probs_type.melt(id_vars=['hour', 'minute', 'customer_type'],
                                       value_vars=food_list)

drink_probs_type = df.groupby(['hour', 'minute', 'customer_type'])['drinks'].value_counts(
    normalize=True).unstack(fill_value=0).reset_index().rename_axis(None, axis=1)
# wide to long
drink_probs_type = drink_probs_type.melt(id_vars=['hour', 'minute', 'customer_type'],
                                         value_vars=drink_list)

# Count Plots by customer type
fig, axes = plt.subplots(nrows=1, ncols=2)

# Plot 1: Proportion of Sold Foods
food_prop = sns.barplot(x='variable', y='value',
                        data=food_probs_type, hue='customer_type', ax=axes[0])
axes[0].set_title("Food Purchases in 5-Year Period by Customer Type")

# Plot 2: Proportion of Sold Drinks
drink_prop = sns.barplot(x='variable', y='value',
                         data=drink_probs_type, hue='customer_type', ax=axes[1])
axes[1].set_title("Drink Purchases in 5-Year Period by Customer Type")
plt.savefig(output_dir + "/ExploratoryPurchPropByType.png")
plt.close()

# Do you see correlations between what returning customers buy and one-timers?
fig, axes = plt.subplots(nrows=2, ncols=1)

sns.lineplot(data=food_probs_type, x='hour', y='value',
             hue='variable', style='customer_type', ax=axes[0])
axes[0].set_title("Correlation of Food Purchases")

sns.lineplot(data=drink_probs_type, x='hour', y='value',
             hue='variable', style='customer_type', ax=axes[1])
axes[1].set_title("Correlation of Drink Purchases")
axes[0].legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
axes[1].legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
plt.tight_layout()
plt.savefig(output_dir + "/ExploratoryPurchaseCorr.png")
plt.close()

################################################################################
