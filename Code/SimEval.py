################################################################################
# Part ? of Python Final Project: Simulation of Coffee Shop
# Group Partners: Andy Boomer and Jacob Pichelmann
################################################################################

# Goal: We want functions to evaluate every simulation. Approach is twofold:
# 1. Showcase functionality
# 2. Export simulated data
# 3. Produce sets of plot/analysis

import random
import pprint as pp
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys


def showcase_sim(sim, params, n_examples, to_text=False):
    # TODO: change to single string
    if to_text:
        sys.stdout = open(os.path.abspath('..') + '/Output/testtext.txt', 'w')
    print('This showcases the results and functionality of simulated customer in the  following simulation:')
    print('Simulated period: ' + min(sim['time']).strftime("%d/%m/%Y, %H:%M") + ' to ' + max(sim['time']).strftime(
        "%d/%m/%Y, %H:%M") + ', n = ' + str(len(sim)))
    print('Data Parameters:')
    pp.pprint(params['data_params'])
    print('\n')
    print('Class Parameters:')
    pp.pprint(params['class_params'])
    print('\n')
    # customers can tell their purchases
    print('A random selection of ' + str(n_examples) + ' exemplary purchases:')
    customers = list(sim['customer'])
    selected_customers = random.choices(customers, k=n_examples)
    for customer in selected_customers:
        customer.tell_purchase()
    print('\n')
    # returning customers know their history
    print('A random selection of ' + str(n_examples) + ' exemplary histories of returning customers:')
    returning_customers = list(sim[sim['customer_type'] == 'returning']['customer'])
    selected_customers = random.choices(returning_customers, k=n_examples)
    for customer in selected_customers:
        customer.tell_purchase_history()
        print('\n')
    print('\n')
    sys.stdout.close()


def store_sim(sim, ind):
    df = sim.drop(['customer'], axis=1)
    df.to_csv(os.path.abspath('..') + '/Output/simulated_data_' + ind + '.csv', sep=';', index=False)


def plot_sim(sim, ind):
    # TODO: more/different plots? what is meant by average income per day?
    # TODO: enhance plot for percentage of one-time vs returning vs empty
    sim['hour'] = sim['time'].dt.hour  # Get hour Integer
    sim['minute'] = sim['time'].dt.minute  # Get minute Integer
    sim['date'] = sim['time'].dt.date
    sim['month'] = sim['time'].dt.month
    sim['year'] = sim['time'].dt.year  # Get year Integer

    # replicate plots from exploratory analysis
    # Initial Count Plots
    fig, axes = plt.subplots(nrows=1, ncols=2)

    # Plot 1: Total Amount of Sold Foods
    sns.countplot(x='food', data=sim, ax=axes[0])
    axes[0].set_title("Count of Food Purchases in 5-Year Simulation")

    # Plot 2: Total Amount of Sold Drinks
    sns.countplot(x='drinks', data=sim, ax=axes[1])
    axes[1].set_title("Count of Drinks Purchases in 5-Year Simulation")
    fig.tight_layout()
    plt.savefig(os.path.abspath('..') + '/Output/countplot_' + ind + '.png')
    plt.close()

    # Get the total amount spent over the five years per unique customer
    rev_frame = sim.groupby('customer_type', as_index=False)['payments'].sum()

    # Get the cumulative revenue at each customer, sorted to get a cumulative curve
    cum_rev = rev_frame['payments'].sort_values(). \
        cumsum().reset_index(drop=True).reset_index()

    # Get the percentage of the max for the index and for the revenue
    cum_rev['index'] = cum_rev['index'] / cum_rev['index'].tail(1).values[0]
    cum_rev['payments'] = cum_rev['payments'] / cum_rev['payments'].tail(1).values[0]

    # Initialize the figure
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # Plot the curve (similar to gini inequality curve)
    plt.plot(cum_rev['index'], cum_rev['payments'],
             label="Cumulative Revenue Sum")
    # Plot a 45 degree line for reference, then show the plot
    plt.plot(cum_rev['index'], cum_rev['index'], label="45 Degree Line")
    plt.legend(loc="upper left")
    ax.set_title("Inequality Distribution of Total Spending by Customer")
    ax.set_xlabel("Percentile of Customer Index")  # Set x-axis title
    ax.set_ylabel("Percentile of Total Revenue")  # Set y-axis title
    plt.savefig(os.path.abspath('..') + '/Output/cum_rev_' + ind + '.png')
    plt.close()

    # show development of returning customers pool
    # Initialize the figure
    fig, ax = plt.subplots(nrows=1, ncols=1)
    sns.lineplot(x='time', y='returns_size', data=sim)
    ax.set_title("Size of returning customers pool")
    ax.set_xlabel("Time")  # Set x-axis title
    ax.set_ylabel("Amount of returning customers")  # Set y-axis title
    plt.savefig(os.path.abspath('..') + '/Output/returns_size_' + ind + '.png')
    plt.close()

    # revenue per day
    # Get the total amount spent over the five years per day
    fig, ax = plt.subplots(nrows=1, ncols=1)
    daily_rev = sim.groupby('date', as_index=False)['payments'].sum()
    sns.lineplot(x='date', y='payments', data=daily_rev)
    ax.set_title("Daily revenue")
    ax.set_xlabel("Time")  # Set x-axis title
    ax.set_ylabel("Total daily revenue in $")  # Set y-axis title
    plt.savefig(os.path.abspath('..') + '/Output/daily_rev_' + ind + '.png')
    plt.close()

    # customer composition per day
    fig, ax = plt.subplots(nrows=1, ncols=1)
    cust_struct = sim.groupby(['date', 'customer_type']).size().reset_index(name='counts')
    cust_struct['total'] = cust_struct['counts'].groupby(cust_struct['date']).transform('sum')
    cust_struct['perc'] = cust_struct['counts'] / cust_struct['total']
    sns.lineplot(x='date', y='perc', hue='customer_type', data=cust_struct)
    ax.set_title("Monthly Customer Composition")
    ax.set_xlabel("Time")  # Set x-axis title
    ax.set_ylabel("")  # Set y-axis title
    plt.savefig(os.path.abspath('..') + '/Output/cust_comp_' + ind + '.png')
    plt.close()
