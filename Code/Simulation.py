from Code.Customers import *
from Code.Customer_Probabilities import df

import random
import pandas as pd

# set up pool of 1000 returning customers (1/3 hipsters)
ReturningCustomersPool = [ReturningCustomer() for i in range(667)]
ReturningCustomersPool.extend([Hipster() for j in range(333)])

# get hour/minute pairs of the day
purchase_times = df['time'][0:20000]
# purchase_times = pd.DatetimeIndex(df['time']) + pd.DateOffset(years=5)

def run_simulation(timespan):
    # record coffee shop performance
    time = []
    customer_id = []
    name = []
    customer_type = []
    drink = []
    food = []
    total_amount = []

    # record history of returning customers
    regulars_history = {}
    for t in timespan:  # restrict simulation period for now
        if random.random() <= 0.2:
            customer = random.choice(ReturningCustomersPool)
            while customer.budget < menu['milkshake'] + menu['pie']:
                print(
                    customer.name + ' has been kicked out because he/she is poor!')  # this works (lower budget to test)
                ReturningCustomersPool.pop(ReturningCustomersPool.index(customer))  # customer gets removed
                customer = random.choice(ReturningCustomersPool)
        else:
            if random.random() <= 0.1:
                customer = TripAdvisorCustomer()
            else:
                customer = Customer()
        customer.make_choice(t)
        customer.make_payment()

        # record characteristics of interest
        time.append(t)
        customer_id.append(customer.customer_id)
        name.append(customer.name)
        customer_type.append(customer.customer_type)
        drink.append(customer.drink_choice)
        food.append(customer.food_choice)
        total_amount.append(customer.amount_spent)
        try:
            regulars_history[customer.customer_id] = customer.history
        except AttributeError:
            continue
    coffee_shop_history = {'time': time, 'customer_id': customer_id, 'name': name,
                           'customer_type': customer_type, 'food': food, 'drink': drink,
                           'total_amount': total_amount}
    coffee_shop_history = pd.DataFrame(coffee_shop_history)
    return coffee_shop_history, regulars_history


c_hist, r_hist = run_simulation(purchase_times)

for key, value in r_hist.items():
    print(key, value)




