from Customers import *
from Customer_Probabilities import df

import random
import pandas as pd
import numpy as np

# get hour/minute pairs of the day
purchase_times = df[['time', 'year', 'hour', 'minute']][0:1000]


def run_simulation(df):

    # times = {}
    # times['Prep'] = 0
    # times['Conditional'] = 0
    # times['Classes'] = 0
    # times['Append'] = 0
    # times['Final'] = 0

    # prep = datetime.datetime.now()

    # record coffee shop performance
    # time = []
    # customer_id = []
    # name = []
    # customer_type = []
    # drink = []
    # food = []

    # set up pool of 1000 returning customers (1/3 hipsters)
    ReturningCustomersPool = [ReturningCustomer() for i in range(667)]
    ReturningCustomersPool.extend([Hipster() for j in range(333)])

    popped = []

    sims = df.shape[0]
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

    cust_array = np.where(np.random.rand(sims) <= 0.2,
                          np.random.choice(ReturningCustomersPool, size=sims),
                          np.where(np.random.rand(sims) <= 0.1,
                                   [TripAdvisorCustomer() for i in range(sims)],
                                   [Customer() for i in range(sims)]))

    # record history of returning customers
    regulars_history = {}

    # any(customer.make_choice(
    #     timespan[i], food_choice[i], drink_choice[i]) for i in range(sims))

    # any(customer.make_payment() for i in range(sims))

    # total_amount = np.array([customer.amount_spent for i in range(sims)])

    # budget = np.array([customer.budget for i in range(sims)])

    # under_budget = budget < (menu['milkshake'] + menu['pie'])

    # while len(under_budget) > 0:

    #     first_under = under_budget[0]

    #     all_under = cust_array == cust_array[first_under]

    #     ReturningCustomersPool.pop(ReturningCustomersPool.index(
    #         first_under))

    #     cust_array[all_under] = np.random.choice(
    #         ReturningCustomersPool, size=len(all_under))

    # times['Prep'] += (datetime.datetime.now() - prep).microseconds

    for i in range(sims):  # restrict simulation period for now
        t = timespan[i]
        # cond = datetime.datetime.now()
        # if random.random() <= 0.2:
        #     customer = random.choice(ReturningCustomersPool)
        #     while customer.budget < menu['milkshake'] + menu['pie']:
        #         # this works (lower budget to test)
        #         print(customer.name + ' has been kicked out because he/she is poor!')
        #         ReturningCustomersPool.pop(ReturningCustomersPool.index(
        #             customer))  # customer gets removed
        #         customer = random.choice(ReturningCustomersPool)
        # else:
        #     if random.random() <= 0.1:
        #         customer = TripAdvisorCustomer()
        #     else:
        #         customer = Customer()

        customer = cust_array[i]
        while customer.budget < menu['milkshake'] + menu['pie']:
            # print(customer.name + ' has been kicked out because he/she is poor!')

            ReturningCustomersPool.pop(ReturningCustomersPool.index(
                customer))

            popped.append(str(customer.customer_id))

            cust_array[i:] = np.where(
                cust_array[i:] == customer,
                np.random.choice(ReturningCustomersPool, size=len(cust_array[i:] == customer)), cust_array[i:])

            customer = cust_array[i]

        # times['Conditional'] += (datetime.datetime.now() - cond).microseconds

        # classes = datetime.datetime.now()

        customer.make_choice(t, food_array[i], drink_array[i])

        # times['Classes'] += (datetime.datetime.now() - classes).microseconds

        # append = datetime.datetime.now()
        customer.make_payment()

        # record characteristics of interest
        # time.append(t)
        # customer_id.append(customer.customer_id)
        # name.append(customer.name)
        # customer_type.append(customer.customer_type)
        # drink.append(customer.drink_choice)
        # food.append(customer.food_choice)
        # total_amount.append(customer.amount_spent)
        total_amount[i] = customer.amount_spent

        try:
            regulars_history[customer.customer_id] = customer.history
        except AttributeError:
            continue

        # times['Append'] += (datetime.datetime.now() - append).microseconds

    # final = datetime.datetime.now()

    customer_id = [str(i.customer_id) for i in cust_array]
    name = [i.name for i in cust_array]
    customer_type = [i.customer_type for i in cust_array]

    coffee_shop_history = {'time': timespan,
                           'customer_id': customer_id, 'name': name,
                           'customer_type': customer_type, 'food': food_array,
                           'drink': drink_array, 'total_amount': total_amount}

    coffee_shop_history = pd.DataFrame(coffee_shop_history)
    # times['Final'] += (datetime.datetime.now() - final).microseconds

    return coffee_shop_history, regulars_history, popped


a = datetime.datetime.now()
c_hist, r_hist, popped = run_simulation(purchase_times)
print((datetime.datetime.now() - a).seconds)

for key, value in r_hist.items():
    print(key, value)
