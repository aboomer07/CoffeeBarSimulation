from Customers import *
from Customer_Probabilities import df

import random
import pandas as pd
import numpy as np

# get hour/minute pairs of the day
purchase_times = df[['time', 'year', 'hour', 'minute']]


def run_simulation(df):

    # set up pool of 1000 returning customers (1/3 hipsters)
    ReturningCustomersPool = [ReturningCustomer() for i in range(667)]
    ReturningCustomersPool.extend([Hipster() for j in range(333)])

    sims = df.shape[0]

    customer_id = np.empty(sims, dtype=object)
    name = np.empty(sims, dtype=object)
    customer_type = np.empty(sims, dtype=object)
    total_amount = np.empty(sims)

    df = pd.merge(df, food_probs,
                  how='left', on=['hour', 'minute'])
    df = pd.merge(df, drink_probs,
                  how='left', on=['hour', 'minute'])

    df['food_choice'] = food_list[(np.random.rand(
        sims, 1) < df[food_list].cumsum(axis=1).values).argmax(axis=1)]

    df['drink_choice'] = drink_list[(np.random.rand(
        sims, 1) < df[drink_list].cumsum(axis=1).values).argmax(axis=1)]

    drink_array = np.array(df['drink_choice'])
    food_array = np.array(df['food_choice'])
    timespan = np.array(df['time'])

    # record history of returning customers
    regulars_history = {}

    for i in range(sims):  # restrict simulation period for now
        t = timespan[i]
        if random.random() <= 0.2:
            customer = random.choice(ReturningCustomersPool)
            while customer.budget < menu['milkshake'] + menu['pie']:
                # this works (lower budget to test)
                # print(customer.name + ' has been kicked out because he/she is poor!')
                ReturningCustomersPool.pop(ReturningCustomersPool.index(
                    customer))  # customer gets removed

                customer = random.choice(ReturningCustomersPool)
        else:
            if random.random() <= 0.1:
                customer = TripAdvisorCustomer()
            else:
                customer = Customer()

        customer.make_choice(t, food_array[i], drink_array[i])

        customer.make_payment()

        customer_id[i] = customer.customer_id
        name[i] = customer.name
        customer_type[i] = customer.customer_type
        total_amount[i] = customer.amount_spent

        try:
            regulars_history[customer.customer_id] = customer.history
        except AttributeError:
            continue

    coffee_shop_history = {'time': timespan,
                           'customer_id': customer_id, 'name': name,
                           'customer_type': customer_type, 'food': food_array,
                           'drink': drink_array, 'total_amount': total_amount}

    coffee_shop_history = pd.DataFrame(coffee_shop_history)

    return coffee_shop_history, regulars_history


a = datetime.datetime.now()
c_hist, r_hist = run_simulation(purchase_times)
print((datetime.datetime.now() - a).seconds)

for key, value in r_hist.items():
    print(key, value)
