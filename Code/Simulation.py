from Code.Customers import *
from Code.Customer_Probabilities import food_probs

import random

# set up pool of 1000 returning customers (1/3 hipsters)
ReturningCustomersPool = [ReturningCustomer() for i in range(777)]
ReturningCustomersPool.extend([Hipster() for j in range(333)])

# get hour/minute pairs of the day
PurchaseTimes = food_probs[['HOUR', 'MINUTE']]

# simulate one day:

# record revenue
revenue = []

for HOUR, MINUTE in PurchaseTimes.itertuples(index=False):
    if random.random() <= 0.2:
        customer = random.choice(ReturningCustomersPool)
    else:
        if random.random() <= 0.1:
            customer = TripAdvisorCustomer()
        else:
            customer = Customer()
    customer.chooseDrink(HOUR, MINUTE)
    customer.chooseFood(HOUR, MINUTE)
    customer.makePayment()
    customer.tellPurchase()
    revenue.append(customer.amount_spent)

print(revenue)
print(sum(revenue))



