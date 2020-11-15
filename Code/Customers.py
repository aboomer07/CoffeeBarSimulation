################################################################################
# Part 2 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# This script introduces customer classes used in the subsequent simulation
################################################################################

# Import libraries
import uuid  # assign customers unique IDs
import names  # just for fun, can be installed with sudo pip
import numpy as np
import pandas as pd


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
        self.name + '\'s budget is ' + str(self.budget)

    def make_payment(self, menu):
        # Make the payment based on the price in the menu and the choices
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        # Reduce the remaining budget accordingly
        self.budget = self.budget - self.amount_spent

    def tell_purchase(self):
        # Display what the customer purchased and at what time
        print(self.name + ' bought ' + self.drink_choice + ' and ' + self.food_choice + ' for a total price of ' +
              str(self.amount_spent) + ' at ' + pd.to_datetime(str(self.time)).strftime("%d/%m/%Y, %H:%M"))


class ReturningCustomer(Customer):
    # Returning customers are a sub class of Customer
    def __init__(self, params):
        super(ReturningCustomer, self).__init__(params)
        self.customer_type = 'returning'
        # they have a higher budget
        self.budget = params[self.customer_type]['budget']
        self.history = {}  # They also can remember their purchase history

    def make_payment(self, menu):
        # Their make payment function is slightly different with the history
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        self.budget = self.budget - self.amount_spent
        history = {'customer_name': self.name, self.time: [
            self.drink_choice, self.food_choice]}
        self.history.update(history)

    def tell_purchase_history(self):
        print(self.history['customer_name'] + ' made the following purchases:')
        for key, value in self.history.items():
            if key == 'customer_name':
                pass
            else:
                key = pd.to_datetime(str(key))
                print(key.strftime("%d/%m/%Y, %H:%M") +
                      ': ' + ' and '.join(value))


class Hipster(ReturningCustomer):
    # Hipsters are a type of ReturningCustomer, we chose to make it a sub class
    # to allow them to have some different behavior
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
            probs = [x / sum(probs) for x in probs]

        self.food_choice = np.random.choice(list(foods.keys()), 1, p=probs)[0]

        probs = list(drinks.values())

        if self.inv_choice:
            probs = [(1 - x) for x in probs]
            probs = [x / sum(probs) for x in probs]

        self.drink_choice = np.random.choice(list(drinks.keys()), 1, p=probs)[0]


class TripAdvisorCustomer(Customer):
    # Trip advisor customer is a sub class of Customer that adds a random tip to purchase
    def __init__(self, params):
        super(TripAdvisorCustomer, self).__init__(params)
        self.customer_type = 'trip_advisor'

    def make_payment(self, menu):
        self.amount_spent = menu[self.food_choice] + \
            menu[self.drink_choice] + np.random.randint(1, 10)
        self.budget = self.budget - self.amount_spent


# Add an extra class to put null in each of the attributes
# Also needs to have the same methods so that the customer creation is seamless
class EmptyInterval(object):
    # The value of all the attributes is set in the sim_params dict
    def __init__(self, params):
        self.customer_type = 'empty_interval'
        self.customer_id = params[self.customer_type]
        self.budget = params[self.customer_type]
        self.name = params[self.customer_type]
        self.food_choice = params[self.customer_type]
        self.drink_choice = params[self.customer_type]
        self.amount_spent = params[self.customer_type]
        self.time = params[self.customer_type]

    # Empty Interval class has all the same methods, but nothing happens
    def make_choice(self, time, foods, drinks):
        pass

    def show_budget(self):
        pass

    def make_payment(self, menu):
        pass

    def tell_purchase(self):
        print("Empty Interval")
