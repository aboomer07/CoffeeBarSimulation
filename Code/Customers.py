################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 2 involves setting up customer classes
################################################################################

# Sidenote: I would propose to add hipsters as a subclass too, in order to allow for additional
# flexibility. We might think about altering hipsters' purchase probabilities for question 4 (e.g.
# they want to be different from the mainstream and choose product with lowest purchase probability)


# import from exploratory script
from Code.Customer_Probabilities import food_probs, drink_probs, food_list, drink_list
# Import libraries
import uuid
import names  # just for fun
import numpy as np

# Each customer has a customer_id and a certain budget. Based on the shape example in the slides the budget
# is not introduced at the super class level.

# set up menu of prices - maybe in other script?
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3,
        'milkshake': 5, 'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}

class Customer(object):
    def __init__(self):
        self.customer_id = uuid.uuid4()  # less than a one in a trillion chance of repeating itself
        self.budget = 100
        self.name = names.get_first_name()  # just for fun
        self.food_choice = None
        self.drink_choice = None
        self.amount_spent = None
        self.time = None

    def make_choice(self, hour, minute):
        food_prob = \
            food_probs[(food_probs['hour'] == hour) & (food_probs['minute'] == minute)][food_list].values.tolist()[0]
        food_choice = np.random.choice(food_list, 1, p=food_prob)[0]
        drink_prob = \
            drink_probs[(drink_probs['hour'] == hour) & (drink_probs['minute'] == minute)][drink_list].values.tolist()[
                0]
        drink_choice = np.random.choice(drink_list, 1, p=drink_prob)[0]
        self.food_choice = food_choice
        self.drink_choice = drink_choice
        self.time = [hour, minute]

    def show_budget(self):
        print(self.name + '\'s budget is ' + str(self.budget))

    def make_payment(self):
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        self.budget = self.budget - self.amount_spent

    def tell_purchase(self):
        print(self.name + ' bought ' + self.drink_choice + ' and ' + self.food_choice + ' for a total price of ' +
              str(self.amount_spent) + ' at ' + str(self.time[0]) + ':' + str(self.time[1]))


class ReturningCustomer(Customer):
    def __init__(self):
        super(ReturningCustomer, self).__init__()
        self.budget += 150
        self.history = {}
        self.visit = 0

    def make_payment(self):
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        self.budget = self.budget - self.amount_spent
        self.visit += 1
        history = {'Visit ' + str(self.visit): [self.drink_choice, self.food_choice, self.time]}
        self.history.update(history)

    def tell_purchase_history(self):
        print(self.history)


class Hipster(ReturningCustomer):
    def __init__(self):
        super(Hipster, self).__init__()
        self.budget += 250


class TripAdvisorCustomer(Customer):
    def make_payment(self):
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice] + np.random.randint(1, 10)
        self.budget = self.budget - self.amount_spent


Cust3 = Hipster()

Cust3.make_choice(12, 32)
Cust3.make_payment()
Cust3.tell_purchase_history()

Cust3.make_choice(14, 28)
Cust3.make_payment()
Cust3.tell_purchase_history()
