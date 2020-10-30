from Code.Customers import *
from Code.Customer_Probabilities import food_probs

import random

# set up pool of 1000 returning customers (1/3 hipsters)
ReturningCustomersPool = [ReturningCustomer() for i in range(777)]
ReturningCustomersPool.extend([Hipster() for j in range(333)])

# get hour/minute pairs of the day
purchase_times = food_probs[['hour', 'minute']]

# simulate one day:

# record revenue
revenue = []

for hour, minute in purchase_times.itertuples(index=False):
    if random.random() <= 0.2:
        customer = random.choice(ReturningCustomersPool)
    else:
        if random.random() <= 0.1:
            customer = TripAdvisorCustomer()
        else:
            customer = Customer()
    customer.make_choice(hour, minute)
    customer.make_payment()
    customer.tell_purchase()
    revenue.append(customer.amount_spent)

print(revenue)
print(sum(revenue))



