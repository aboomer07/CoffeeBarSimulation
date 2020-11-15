################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 1 involves exploring sample coffee dataset, returns console prints and
# a set of plots with the prefix 'Exploratory'
################################################################################

################################################################################
###  Importing Libraries and Datafile ###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

# Force the correct directory
if os.getcwd().split("/")[-1] == "Code":
    os.chdir("..")
curr_dir = os.getcwd()

# If an output directory does not already exist, create one
if not os.path.isdir("Output"):
    os.mkdir("Output")
output_dir = curr_dir + "/Output"


data_path = curr_dir + "/Data/Coffeebar_2016-2020.csv"

df = pd.read_csv(data_path, sep=";")

# prices of the coffee shop are stored in the menu
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}
################################################################################

################################################################################
### Data preparation for plotting ###

# Cange column names to follow pep8
df.columns = ['time', 'customer', 'drinks', 'food']

# Perform initial data manipulation
df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%d %H:%M:%S")
df['year'] = df['time'].dt.year  # Get year Integer
df['month'] = df['time'].dt.month  # Get month Integer
df['hour'] = df['time'].dt.hour  # Get hour Integer
df['minute'] = df['time'].dt.minute  # Get minute Integer

df['food'] = df['food'].fillna("nothing")  # A null value means no food ordered

# Use the map function to map the dictionary keys onto the food column
df['food_revenue'] = df['food'].map(menu)
# Use the map function to map the dictionary keys onto the drink column
df['drink_revenue'] = df['drinks'].map(menu)
# Get the total revenue based on the food revenue and drink revenue
df['revenue'] = df['food_revenue'] + df['drink_revenue']

# construct indicators for customer types (one time and returning)
df['returning'] = df['customer'].isin(df[df['customer'].duplicated()]['customer']).astype(int)

df['onetime'] = np.where(df['returning'] == 0, 1, 0)
df['customer_type'] = np.where(df['onetime'] == 1, 'onetime', 'returning')
################################################################################

################################################################################
### Construct additional data frames for plotting ###

# Lists of unique drinks and foods
drink_list = df['drinks'].unique()  # Get the unique list of possible drinks
food_list = df['food'].unique()  # Get unique list of possible food items

# Probabilities of drinks and foods purchased at time tuples (hour/minute)
# Use Value Counts Function to Calculate the Probabilities for Each Food Item
# And Each Drink. Unstack to Create Columns Per Item/Drink
prob_df = df.groupby(['hour', 'minute'])['food'] \
    .value_counts(normalize=True).unstack(fill_value=0) \
    .reset_index().rename_axis(None, axis=1)

prob_df = prob_df.merge(df.groupby(['hour', 'minute'])['drinks']
                        .value_counts(normalize=True).unstack(fill_value=0)
                        .reset_index().rename_axis(None, axis=1),
                        on=['hour', 'minute'])

# Add time column
prob_df['time'] = prob_df['hour'].apply(str) + ':' + \
                  np.where(prob_df['minute'] < 10, "0" + prob_df['minute'].apply(str),
                           prob_df['minute'].apply(str))

# Total amount spent over five years per unique customer
rev_frame = df.groupby('customer', as_index=False)['revenue'].sum()

# Cumulative revenue at each customer, sorted to get a cumulative curve
cum_rev = rev_frame['revenue'].sort_values(). \
    cumsum().reset_index(drop=True).reset_index()

# Get the percentage of the max for the index and for the revenue
cum_rev['index'] = cum_rev['index'] / cum_rev['index'].tail(1).values[0]
cum_rev['revenue'] = cum_rev['revenue'] / cum_rev['revenue'].tail(1).values[0]

# Mean time between visits from returning customers
# Get only the customers who have visited more than once
time_frame = df[df['customer'].duplicated()] \
    .sort_values(by=['customer', 'time'])

# Find the number of days (as a float) between visits for returning customers
time_frame['time_diff'] = time_frame['time']. \
    subtract(time_frame.groupby('customer')['time'].shift()).apply(
    lambda x: np.float(x.value) / (3600 * 24 * 1000000000))

# There is one value to remove from subtracting with the Nan in the first row
time_frame['time_diff'] = np.where(time_frame['time_diff'] < 0,
                                   np.nan, time_frame['time_diff'])

# Calculate the mean of the one time dummy variable to get the percentage
onetime = df.groupby(['year', 'month'], as_index=False)['onetime'].mean()

# Probability of customer being a returning customer at certain time
returning_prob = df.groupby(['hour', 'minute'],
                            as_index=False)['returning'].mean()

# Calculate food purchase probabilities per customer type
food_probs_type = df.groupby(['hour', 'minute', 'customer_type'])['food'] \
    .value_counts(normalize=True).unstack(fill_value=0) \
    .reset_index().rename_axis(None, axis=1)

# Change from wide to long for plotting
food_probs_type = food_probs_type.melt(
    id_vars=['hour', 'minute', 'customer_type'], value_vars=food_list)

# Calculate drink purchase probabilities per customer type
drink_probs_type = df.groupby(['hour', 'minute', 'customer_type'])['drinks'] \
    .value_counts(normalize=True).unstack(fill_value=0) \
    .reset_index().rename_axis(None, axis=1)

# Change from wide to long for plotting
drink_probs_type = drink_probs_type.melt(
    id_vars=['hour', 'minute', 'customer_type'], value_vars=drink_list)
################################################################################

################################################################################


################################################################################

################################################################################
# Answers to:
# What food and drinks are sold by the coffee bar? (Part 1)
# How many unique customers did the bar have? (Part 1)
# How many returning customers do we observe in the data? (Part 4)

# Print the unique foods that the coffee bar sells with a join statement
print('The foods the bar sells are ' +
      ", ".join([x for x in food_list if x != 'nothing']))

# Print the unique drinks the coffee bar sells with a join
print('The drinks the bar sells are ' + ", ".join(drink_list))

# How many unique and returning customers did the coffee bar have?
customerList = df['customer'].unique()  # Unique set of customers ID's
print("There are " + str(len(customerList)) +
      " unique (one-time) customers out of " + str(
    len(df['customer'])) + " customers who have ever attended this coffee shop. \n" +
      "Conversely, there have been " + str(df['returning'].sum()) + " returning customer in the last 5 years.")
################################################################################


################################################################################
# Bar Plots
# Answers to:
# 1. Bar plot of total amount of sold foods per year. (Part 1)
# 2. Bar plot of total amount of sold drinks per year.(Part 1)
# 3. Bar plot of food purchase probabilities per customer type. (Part 4)
# 4. Bar plot of drink purchase probabilities per customer type. (Part 4)

# Set up grid for plot 1 and plot 2
fig, axes = plt.subplots(nrows=1, ncols=2, sharey='row')
fig.set_size_inches(10, 5)

# Plot 1: Total Amount of Sold Foods
sns.countplot(x='food', data=df, ax=axes[0])
axes[0].set_title("Count of Food Purchases in 5-Year Period")

# Plot 2: Total Amount of Sold Drinks
sns.countplot(x='drinks', data=df, ax=axes[1])
axes[1].set_title("Count of Drinks Purchases in 5-Year Period")
fig.tight_layout()
plt.savefig(output_dir + "/ExploratoryCountPlot.png")
plt.close()

# Set up grid for plot 3 and plot 4
fig, axes = plt.subplots(nrows=1, ncols=2)
fig.set_size_inches(10, 5)

# Plot 3: Proportion of Sold Foods
sns.barplot(x='variable', y='value',
                        data=food_probs_type, hue='customer_type', ax=axes[0])
axes[0].xaxis.label.set_visible(False)
axes[0].yaxis.label.set_visible(False)
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))


# Plot 4: Proportion of Sold Drinks
sns.barplot(x='variable', y='value',
                         data=drink_probs_type, hue='customer_type', ax=axes[1])
axes[1].xaxis.label.set_visible(False)
axes[1].yaxis.label.set_visible(False)
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))


# Common title
fig.suptitle("Food/Drink Purchases in 5-Year Period by Customer Type")
#Export
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(output_dir + "/ExploratoryPurchPropByType.png")
plt.close()
################################################################################

################################################################################
# Stack plots
# Answers to:
# Further analysis of calculated purchase probabilities during the day (data understanding). (Part 1)

# Set up grid for both plots
fig, axes = plt.subplots(nrows=1, ncols=2)

# Create the stack plot for food
axes[0].stackplot(prob_df['time'], *[prob_df[col] for col in food_list],
              labels=list(food_list))

axes[0].legend(loc='lower right', fancybox=True, ncol=2)  # Get a legend for the plot

# Create the stack plot for drinks
axes[1].stackplot(prob_df['time'], *[prob_df[col] for col in drink_list],
              labels=list(drink_list))

axes[1].legend(loc='lower right', fancybox=True)  # Get the legend


# Axis styling
axes[0].xaxis.set_major_locator(plt.MaxNLocator(12))
axes[1].xaxis.set_major_locator(plt.MaxNLocator(12))
axes[0].set_ylabel("Percentage of Food Purchases")
axes[1].set_ylabel("Percentage of Drink Purchases")
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.setp(axes[0].get_xticklabels() + axes[1].get_xticklabels(), rotation=30, ha='right')
# Common title
fig.suptitle("Proportion of Food/Drinks Purchased Throughout a Day")
#Export
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(output_dir + "/ExploratoryPurchaseProb.png")
plt.close()
################################################################################

################################################################################
# Revenue plots
# Answers to:
# Further analysis of revenue structure (data understanding). (Part 1)

# Set up single figure grid
fig, ax = plt.subplots(nrows=1, ncols=1)

# Plot the cumulative revenue (similar to gini inequality curve)
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
# Customer composition plots
# Answers to:
# Further analysis of customer structure (data understanding). (Part 1)
# Do returning customers have specific times when they show up more? (Part 4)

# Initialize first figure
fig, ax = plt.subplots(ncols=1, nrows=1)

# Calculate the mean time difference and plot it
plt.plot(sorted(time_frame.groupby('customer')['time_diff'].mean().values))

# Set title and show the plot
ax.set_title("Mean Time Between Visits for Returning Customers")
ax.set_xlabel("Ordered Index of Returning Customers")  # Set x-axis title
ax.set_ylabel("Mean Time Between Visits (Days)")  # Set y-axis title
plt.savefig(output_dir + "/ExploratoryMeanTime.png")
plt.close()

# Initialize second figure
fig, ax = plt.subplots(ncols=1, nrows=1)

# Plot the percentage, with different lines as the years
sns.barplot(data=onetime, x='month', y='onetime',
            hue='year', ax=ax)

# Set title and show the plot
ax.set_title("Proportion of One Time Customers Per Month and Year")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.savefig(output_dir + "/ExploratoryOneTimePct.png")
plt.close()

# Initialize third figure
fig, ax = plt.subplots(ncols=1, nrows=1)

# Plot probabilities of returning customers over a day
sns.lineplot(data=returning_prob, x='hour', y='returning', ax=ax)
ax.set_title("Proportion of Returning Customers during a Day")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.savefig(output_dir + "/ExploratoryReturningDailyPct.png")
plt.close()
################################################################################

################################################################################
# Customer composition purchase analysis
# Answers to:
# # Do you see correlations between what returning customers buy and one-timers? (Part 4)

# Initialize figure
fig, axes = plt.subplots(nrows=2, ncols=1)

sns.lineplot(data=food_probs_type, x='hour', y='value',
             hue='variable', style='customer_type', ax=axes[0])
axes[0].set_title("Correlation of Food Purchases")
axes[0].set_ylabel("Proportion of Total Purchases")  # Set y-axis title
axes[0].legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., title='Purchase')
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))



sns.lineplot(data=drink_probs_type, x='hour', y='value',
             hue='variable', style='customer_type', ax=axes[1])
axes[1].set_title("Correlation of Drink Purchases")
axes[1].set_ylabel("Proportion of Total Purchases")  # Set y-axis title
axes[1].legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., title='Purchase')
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.tight_layout()
plt.savefig(output_dir + "/ExploratoryPurchaseCorr.png")
plt.close()
################################################################################
