################################################################################
# Part ? of Python Final Project: Simulation of Coffee Shop
# Group Partners: Andy Boomer and Jacob Pichelmann
################################################################################

# Goal: We want functions to evaluate every simulation. Approach is threefold:
# 1. Showcase functionality
# 2. Export simulated data
# 3. Produce sets of plot/analysis

import random
import pprint as pp
import matplotlib.pyplot as plt
import seaborn as sns
import os
import inspect
import objgraph
from Code.SimParams import *
from Code.Customers import *

# Force the correct directory
if os.getcwd().split("/")[-1] == "Code":
    os.chdir("..")
curr_dir = os.getcwd()

# If an output directory does not already exist, create one
if not os.path.isdir("Output"):
    os.mkdir("Output")
output_dir = curr_dir + "/Output"


# Create a function to print some of the text related output from simulation
def showcase_sim(sim, params, n_examples):
    print('This showcases the results and functionality of simulated customer in the  following simulation:')
    print('Simulated period: ' + min(sim['time']).strftime("%d/%m/%Y, %H:%M") + ' to ' + max(sim['time']).strftime(
        "%d/%m/%Y, %H:%M") + ', n = ' + str(len(sim)))

    # Print the parameters passed to the simulation
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
        customer.tell_purchase()  # Get some purchases from random customers
    print('\n')

    # returning customers know their history
    print('A random selection of ' + str(n_examples) +
          ' exemplary histories of returning customers:')
    returning_customers = list(  # Choose the returning customers
        sim[sim['customer_type'] == 'returning']['customer'])
    selected_customers = random.choices(returning_customers, k=n_examples)

    # Get back the purchase histories of the selection returining customers
    for customer in selected_customers:
        customer.tell_purchase_history()
        print('\n')
    print('\n')


# Define function to store the simulation dataframe in a csv file
def store_sim(sim, ind):
    df = sim.drop(['customer'], axis=1)
    df.to_csv(output_dir + '/simulated_data_' +
              ind + '.csv', sep=';', index=False)


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
    fig, axes = plt.subplots(nrows=1, ncols=2, sharey='row')
    fig.set_size_inches(10, 5)

    # Plot 1: Total Amount of Sold Foods
    sns.countplot(x='food', data=sim, ax=axes[0])
    axes[0].set_title("Count of Food Purchases in 5-Year Simulation")

    # Plot 2: Total Amount of Sold Drinks
    sns.countplot(x='drinks', data=sim, ax=axes[1])
    axes[1].set_title("Count of Drinks Purchases in 5-Year Simulation")
    fig.tight_layout()
    plt.savefig(output_dir + '/countplot_' + ind + '.png')
    plt.close()

    # Get the total amount spent over the five years per unique customer
    rev_frame = sim.groupby('customer_type', as_index=False)['payments'].sum()

    # Get the cumulative revenue at each customer, sorted to get a cumulative curve
    cum_rev = rev_frame['payments'].sort_values(). \
        cumsum().reset_index(drop=True).reset_index()

    # Get the percentage of the max for the index and for the revenue
    cum_rev['index'] = cum_rev['index'] / cum_rev['index'].tail(1).values[0]
    cum_rev['payments'] = cum_rev['payments'] / \
        cum_rev['payments'].tail(1).values[0]

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
    plt.savefig(output_dir + '/cum_rev_' + ind + '.png')
    plt.close()

    # show development of returning customers pool
    # Initialize the figure
    fig, ax = plt.subplots(nrows=1, ncols=1)
    sns.lineplot(x='time', y='returns_size', data=sim)
    ax.set_title("Size of returning customers pool")
    ax.set_xlabel("Time")  # Set x-axis title
    ax.set_ylabel("Amount of returning customers")  # Set y-axis title
    plt.savefig(output_dir + '/returns_size_' + ind + '.png')
    plt.close()

    # revenue per day
    # Get the total amount spent over the five years per day
    fig, ax = plt.subplots(nrows=1, ncols=1)
    daily_rev = sim.groupby('date', as_index=False)['payments'].sum()
    sns.lineplot(x='date', y='payments', data=daily_rev)
    ax.set_title("Daily revenue")
    ax.set_xlabel("Time")  # Set x-axis title
    ax.set_ylabel("Total daily revenue in $")  # Set y-axis title
    plt.savefig(output_dir + '/daily_rev_' + ind + '.png')
    plt.close()

    # customer composition per day stacked
    fig, ax = plt.subplots(nrows=1, ncols=1)
    cust_list = ['one_time', 'returning',
                 'hipster', 'trip_advisor']
    cust_struct = sim.groupby('date')['customer_type']\
        .value_counts(normalize=True).unstack(fill_value=0)\
        .reset_index().rename_axis(None, axis=1)

    plt.stackplot(cust_struct['date'],
                  *[cust_struct[col] for col in cust_list],
                  labels=list(cust_list))

    ax.set_title("Monthly Customer Composition")
    ax.set_xlabel("Time")  # Set x-axis title
    ax.set_ylabel("")  # Set y-axis title
    plt.legend(loc='lower right')
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    plt.savefig(output_dir + '/cust_comp_stack_' + ind + '.png')
    plt.close()

    # Create the object graphs from objgraph library
    if ind == "sim_1":
        objgraph.show_refs(Customer, filter=lambda x: [(inspect.ismethod(i)) for i in inspect.getmembers(x)], max_depth=2,
                           filename=output_dir + "/" + ind + '_CustomerMethods.png')

        objgraph.show_refs(Customer(Sim1['class_params']),
                           filter=lambda x: [(inspect.ismethod(i)) for i in inspect.getmembers(x)], max_depth=2, filename=output_dir + "/" ind + '_CustomerAttributes.png')
