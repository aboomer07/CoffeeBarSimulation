from SimParams import Sim1, Sim2, Sim3, Sim4, Sim5
from Customers import *
from Customer_Probabilities import df

import random
import pandas as pd
import numpy as np
import math

# get hour/minute pairs of the day
sim_df = df[['time', 'year', 'hour', 'minute']][:30000]


def run_simulation(data, params):

    data = data.copy(deep=True)

    sims = data.shape[0]

    data_params = params['data_params'].copy()
    class_params = params['class_params'].copy()

    data_params['menus'] = data_params['menus'][:sims]

    customers = np.empty(sims, dtype=object)
    customer_type = np.empty(sims, dtype=object)
    customer_id = np.empty(sims, dtype=object)
    names = np.empty(sims, dtype=object)
    pool_size = np.empty(sims, dtype=np.int64)
    food_choices = np.empty(sims, dtype=object)
    drink_choices = np.empty(sims, dtype=object)
    payments = np.empty(sims, dtype=np.float64)
    budget = np.empty(sims, dtype=np.float64)

    data = pd.merge(data, food_probs,
                    how='left', on=['hour', 'minute'])
    data = pd.merge(data, drink_probs,
                    how='left', on=['hour', 'minute'])

    data['foods'] = data[food_list].to_dict(orient='records')
    data['drinks'] = data[drink_list].to_dict(orient='records')

    num_returns = class_params['num_returns']
    num_hipsters = math.ceil(num_returns / 3)
    num_returns -= num_hipsters

    # set up pool of returning customers (1/3 hipsters)
    ReturningCustomersPool = [ReturningCustomer(
        class_params) for i in range(num_returns)]

    ReturningCustomersPool.extend([Hipster(class_params)
                                   for j in range(num_hipsters)])

    drink_array = np.array(data['drinks'])
    food_array = np.array(data['foods'])
    timespan = np.array(data['time'])

    for i in range(sims):  # restrict simulation period for now

        menu = data_params['menus'][i]
        t = timespan[i]
        pool_size[i] = len(ReturningCustomersPool)

        if random.random() <= 0.2:
            if pool_size[i] > 0:
                customer = random.choice(ReturningCustomersPool)
                while customer.budget < menu['milkshake'] + menu['pie']:
                    ReturningCustomersPool.pop(ReturningCustomersPool.index(
                        customer))  # customer gets removed
                    try:
                        customer = random.choice(ReturningCustomersPool)
                    except IndexError:
                        customer = EmptyInterval(class_params)
            else:
                customer = EmptyInterval(class_params)
        else:
            if random.random() <= 0.1:
                customer = TripAdvisorCustomer(class_params)
            else:
                customer = Customer(class_params)

        customer.make_choice(t, food_array[i], drink_array[i])
        customer.make_payment(menu)

        customers[i] = customer
        customer_id[i] = str(customer.customer_id)
        names[i] = customer.name
        customer_type[i] = customer.customer_type
        food_choices[i] = customer.food_choice
        drink_choices[i] = customer.drink_choice
        payments[i] = customer.amount_spent
        budget[i] = customer.budget

    coffee_shop_history = {
        'time': timespan, 'customer': customers, 'customer_id': customer_id,
        'ReturnsSize': pool_size, 'name': names, 'customer_type': customer_type,
        'food': food_choices, 'drinks': drink_choices, 'payments': payments,
        'budget': budget}

    coffee_shop_history = pd.DataFrame(coffee_shop_history)

    return coffee_shop_history


a = datetime.datetime.now()
sim1_df = run_simulation(sim_df, Sim1)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim2_df = run_simulation(sim_df, Sim2)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim3_df = run_simulation(sim_df, Sim3)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim4_df = run_simulation(sim_df, Sim4)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim5_df = run_simulation(sim_df, Sim5)
print((datetime.datetime.now() - a).seconds)
