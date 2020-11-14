# Import the needed objects and functions from other files
from Code.Customers import *
from Code.CustomerProbabilities import *

# Import the python libraries needed in the simulation
import random
import pandas as pd
import numpy as np
import math


# Define a function to take in data and simulation parameters
def run_simulation(data, params):
    data = data.copy(deep=True)  # Make sure data doesn't get overwritten

    sims = data.shape[0]  # Get the size of the current simulation

    # Get the parameters for the objects and for the menu price array
    data_params = params['data_params'].copy()
    class_params = params['class_params'].copy()

    # The menu array size is the full sample, limit to current sample
    data_params['menus'] = data_params['menus'][:sims]

    # Predefine a set of numpy arrays for each output to speed up code
    customers = np.empty(sims, dtype=object)
    customer_type = np.empty(sims, dtype=object)
    customer_id = np.empty(sims, dtype=object)
    names = np.empty(sims, dtype=object)
    pool_size = np.empty(sims, dtype=np.int64)
    food_choices = np.empty(sims, dtype=object)
    drink_choices = np.empty(sims, dtype=object)
    payments = np.empty(sims, dtype=np.float64)
    budget = np.empty(sims, dtype=np.float64)

    # Get the food and drink probabilities and put them into dictionaries
    data = pd.merge(data, prob_df, how='left', on=['hour', 'minute'])
    data['foods'] = data[food_list].to_dict(orient='records')
    data['drinks'] = data[drink_list].to_dict(orient='records')

    # Get the size of the returning pool for this simulation
    num_returns = class_params['num_returns']
    num_hipsters = math.ceil(num_returns / 3)
    num_returns -= num_hipsters

    # set up pool of returning customers (1/3 hipsters)
    ReturningCustomersPool = [ReturningCustomer(
        class_params) for i in range(num_returns)]
    ReturningCustomersPool.extend([Hipster(class_params)
                                   for j in range(num_hipsters)])

    # Get the food, drink probability and time dicts into arrays for speed
    drink_array = np.array(data['drinks'])
    food_array = np.array(data['foods'])
    timespan = np.array(data['time'])

    # Loop through the total number of iterations in current simulation
    for i in range(sims):

        menu = data_params['menus'][i]  # Get the current set of prices
        t = timespan[i]  # Get current datetime
        pool_size[i] = len(ReturningCustomersPool)  # Get current size of pool

        # Nested if to determine which type of customer to pull this iteration
        if random.random() <= 0.2:

            # Conditional whether a returning can be pulled
            if pool_size[i] > 0:
                customer = random.choice(ReturningCustomersPool)
                # Check whether the chosen returning has enough budget
                while customer.budget < max(
                        {key: val for key, val in menu.items() if (key in drink_list)}.values()) + max(
                        {key: val for key, val in menu.items() if (key in food_list)}.values()):
                    ReturningCustomersPool.pop(ReturningCustomersPool.index(
                        customer))  # customer gets removed

                    # Error checking to see if returning can be accessed
                    try:
                        customer = random.choice(ReturningCustomersPool)
                    except IndexError:
                        customer = EmptyInterval(class_params)
            # If returning is empty, create null interval
            else:
                customer = EmptyInterval(class_params)
        # If returning customer isn't chosen, choose one of the one-times
        else:
            if random.random() <= 0.1:  # Trip advisor choice
                customer = TripAdvisorCustomer(class_params)
            else:  # Regular one-time choice
                customer = Customer(class_params)

        # Every customer object can make a choice given these inputs
        customer.make_choice(t, food_array[i], drink_array[i])
        customer.make_payment(menu)  # Make payment given prices

        # Store all the outputs in the predefined arrays
        customers[i] = customer
        customer_id[i] = str(customer.customer_id)
        names[i] = customer.name
        customer_type[i] = customer.customer_type
        food_choices[i] = customer.food_choice
        drink_choices[i] = customer.drink_choice
        payments[i] = customer.amount_spent
        budget[i] = customer.budget

    # Put all the predefined arrays into a dictionary
    coffee_shop_history = {
        'time': timespan, 'customer': customers, 'customer_id': customer_id,
        'returns_size': pool_size, 'name': names,
        'customer_type': customer_type, 'food': food_choices,
        'drinks': drink_choices, 'payments': payments, 'budget': budget}

    # Put this dictionary into a dataframe, columns are the keys
    coffee_shop_history = pd.DataFrame(coffee_shop_history)

    return coffee_shop_history
