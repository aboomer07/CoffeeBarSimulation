################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 2 involves setting up customer classes
################################################################################


# import probabilities and lists of things offered at the coffee shop
from Customer_Probabilities import food_probs, drink_probs, food_list, drink_list

# Import libraries
import uuid
import names  # just for fun, can be installed with sudo pip
import numpy as np
import datetime  # For getting hour and minute from datetime objects


class Customer(object):
    def __init__(self, params):
        # less than a one in a trillion chance of repeating itself
        self.customer_id = uuid.uuid4()
        self.customer_type = 'one_time'
        self.budget = params[self.customer_type]['budget']
        self.name = names.get_first_name()  # just for fun
        # initialize variables for the customer
        self.food_choice = None
        self.drink_choice = None
        self.amount_spent = None
        self.time = None

    def make_choice(self, time, foods, drinks):
        # Overwrite the initialized variables

        self.time = time

        self.food_choice = np.random.choice(
            list(foods.keys()), 1, p=list(foods.values()))[0]

        self.drink_choice = np.random.choice(
            list(drinks.keys()), 1, p=list(drinks.values()))[0]

    def show_budget(self):
        # Display the customer's current budget
        print(self.name + '\'s budget is ' + str(self.budget))

    def make_payment(self, menu):
        # Make the payment based on the price in the menu and the choices
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        # Reduce the reminining budget accordingly
        self.budget = self.budget - self.amount_spent

    def tell_purchase(self):
        # Display what the customer purchased and at what time
        print(self.name + ' bought ' + self.drink_choice + ' and ' + self.food_choice + ' for a total price of ' +
              str(self.amount_spent) + ' at ' + str(self.time))


class ReturningCustomer(Customer):  # Define a returning customer
    def __init__(self, params):
        super(ReturningCustomer, self).__init__(params)
        self.customer_type = 'returning'
        # they have a higher budget
        self.budget = params[self.customer_type]['budget']
        self.history = {}  # They also can remember their purchase history
        self.visit = 0  # Keep track of their current visit number

    def make_payment(self, menu):
        # Their make payment function is slightly different with the history
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        self.budget = self.budget - self.amount_spent
        self.visit += 1  # Increase the visit variable by 1
        history = {'customer_name': self.name, self.time: [
            self.drink_choice, self.food_choice]}
        self.history.update(history)

    def tell_purchase_history(self):
        print(self.history)  # Show the current history dictionary


class Hipster(ReturningCustomer):
    # Hipsters are a type of returning customer, we chose to make it a subclass
    # In case we want the hipster to have some different behavior later
    def __init__(self, params):
        super(Hipster, self).__init__(params)
        self.customer_type = 'hipster'
        # Hipsters have an even larger budget
        self.budget = params[self.customer_type]['budget']
        self.inv_choice = params[self.customer_type]['inv_choice']

    def make_choice(self, time, foods, drinks):

        self.time = time

        probs = list(foods.values())

        if self.inv_choice:
            probs = [(1 - x) for x in probs]
            probs = [x/sum(probs) for x in probs]

        self.food_choice = np.random.choice(list(foods.keys()), 1, p=probs)[0]

        probs = list(drinks.values())

        if self.inv_choice:
            probs = [(1 - x) for x in probs]
            probs = [x/sum(probs) for x in probs]

        self.drink_choice = np.random.choice(list(drinks.keys()), 1, p=probs)[0]


class TripAdvisorCustomer(Customer):
    # Trip advisor customer is a subclass of customer that adds a random tip to purchase
    def __init__(self, params):
        super(TripAdvisorCustomer, self).__init__(params)
        self.customer_type = 'trip_advisor'

    def make_payment(self, menu):
        self.amount_spent = menu[self.food_choice] + \
            menu[self.drink_choice] + np.random.randint(1, 10)
        self.budget = self.budget - self.amount_spent


class EmptyInterval(object):
    def __init__(self, params):
        self.customer_type = 'empty_interval'
        self.customer_id = params[self.customer_type]
        self.budget = params[self.customer_type]
        self.name = params[self.customer_type]
        self.food_choice = params[self.customer_type]
        self.drink_choice = params[self.customer_type]
        self.amount_spent = params[self.customer_type]
        self.time = params[self.customer_type]

    def make_choice(self, time, foods, drinks):
        pass

    def show_budget(self):
        pass

    def make_payment(self, menu):
        pass

    def tell_purchase(self):
        print("Empty Interval")


# Now test these classes for a few different actions the customers can do
time1 = datetime.datetime(2020, 6, 25, 8, 0, 0)
time2 = datetime.datetime(2020, 10, 10, 14, 32, 0)

# food_probs_1 = food_probs[(food_probs['hour'] == time1.hour) & (
#     food_probs['minute'] == time1.minute)]['food_prob'].values[0]
# drink_probs_1 = drink_probs[(drink_probs['hour'] == time1.hour) & (
#     drink_probs['minute'] == time1.minute)]['drink_prob'].values[0]

# Cust3 = Hipster()  # Create hipster returning customer

# Have them make their first choice
# Cust3.make_choice(time1, food_probs_1, drink_probs_1)
# Cust3.make_payment()  # Make the payment based on the choice
# Cust3.tell_purchase_history()  # Return their history

# Cust3.make_choice(time2)  # They visit again at another time
# Cust3.make_payment()  # They make the payment for current visit
# Cust3.tell_purchase_history()  # They have a new updated history
