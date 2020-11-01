from Code.Customers import *
from Code.Customer_Probabilities import df

import random

# set up pool of 1000 returning customers (1/3 hipsters)
ReturningCustomersPool = [ReturningCustomer() for i in range(667)]
ReturningCustomersPool.extend([Hipster() for j in range(333)])

# get hour/minute pairs of the day
purchase_times = df[df['year'] == 2016]['time']

# simulate first 10000 transactions:

# record revenue
revenue = []
regulars_history = []

for time in purchase_times[1:10000]:  # restrict simulation period for now
    if random.random() <= 0.2:
        customer = random.choice(ReturningCustomersPool)
        while customer.budget < menu['milkshake'] + menu['pie']:
            print(customer.name + ' has been kicked out because he/she is poor!')  # this works (lower budget to test)
            ReturningCustomersPool.pop(ReturningCustomersPool.index(customer))  # customer gets removed
            customer = random.choice(ReturningCustomersPool)
        regulars_history.append(customer.history)  # for some reason this already returns unique histories?
    else:
        if random.random() <= 0.1:
            customer = TripAdvisorCustomer()
        else:
            customer = Customer()
    customer.make_choice(time)
    customer.make_payment()
    #customer.tell_purchase()
    revenue.append(customer.amount_spent)

print(sum(revenue))

for history in regulars_history:
    for key, value in history.items():
        print(key, value)




