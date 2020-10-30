################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 2 involves setting up customer classes
################################################################################

# Sidenote: I would propose to add hipsters as a subclass too, in order to allow for additional
# flexibility. We might think about altering hipsters' purchase probabilities for question 4 (e.g.
# they want to be different from the mainstream and choose product with lowest purchase probability)

# import sys
# import os
# sys.path.insert(0, os.path.abspath('.') + '/Code')
# print(sys.path)

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

    def choose_food(self, hour, minute):
        prob = food_probs[(food_probs['hour'] == hour) & (food_probs['minute'] == minute)][food_list].values.tolist()[0]
        food_choice = np.random.choice(food_list, 1, p=prob)[0]
        self.food_choice = food_choice
        self.time = str(hour) + ':' + str(minute)  # this is ugly and needs to be changed
        return self.food_choice

    def choose_drink(self, hour, minute):
        prob = drink_probs[(drink_probs['hour'] == hour) & (drink_probs['minute'] == minute)][drink_list].values.tolist()[0]
        drink_choice = np.random.choice(drink_list, 1, p=prob)[0]
        self.drink_choice = drink_choice
        return self.drink_choice

    def show_budget(self):
        print(self.name + '\'s budget is ' + str(self.budget))

    def make_payment(self):
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        self.budget = self.budget - self.amount_spent

    def tell_purchase(self):
        print(self.name + ' bought ' + self.drink_choice + ' and ' + self.food_choice + ' for a total price of ' +
              str(self.amount_spent) + ' at ' + self.time)


class ReturningCustomer(Customer):
    def __init__(self):
        super(ReturningCustomer, self).__init__()
        self.budget += 150
        self.food_choice_history = []
        self.drink_choice_history = []

    def tell_purchase_history(self):
        print(self.food_choice_history)
        print(self.drink_choice_history)

    def choose_food(self, hour, minute):
        prob = food_probs[(food_probs['hour'] == hour) & (food_probs['minute'] == minute)][food_list].values.tolist()[0]
        food_choice = np.random.choice(food_list, 1, p=prob)[0]
        self.food_choice = food_choice
        self.food_choice_history.append(food_choice)
        self.time = str(hour) + ':' + str(minute)  # this is ugly and needs to be changed
        return self.food_choice

    def choose_drink(self, hour, minute):
        prob = drink_probs[(drink_probs['hour'] == hour) & (drink_probs['minute'] == minute)][drink_list].values.tolist()[0]
        drink_choice = np.random.choice(drink_list, 1, p=prob)[0]
        self.drink_choice = drink_choice
        self.drink_choice_history.append(drink_choice)
        return self.drink_choice


class Hipster(ReturningCustomer):
    def __init__(self):
        super(Hipster, self).__init__()
        self.budget += 250


class TripAdvisorCustomer(Customer):
    def make_payment(self):
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice] + np.random.randint(1, 10)
        self.budget = self.budget - self.amount_spent


# in this current set up we would not necessarily have to set up a class for one time customers - is this a mistake?


Cust1 = Customer()
Cust1.show_budget()

print(Cust1.choose_drink(8, 5))
print(Cust1.choose_food(8, 5))  # in the morning he wants coffee and nothing to eat
print(Cust1.food_choice)

# print(Cust1.choose_food(14, 30))
# 14:30 has no records so this returns nothing weird Series string, need to add
# error!

print(Cust1.choose_drink(12, 32))
print(Cust1.choose_food(12, 32))  # for lunch he wants soda and a sandwich

Cust1.make_payment()
Cust1.show_budget()  # soda and sandwich cost 5 in total, so this works. Note that the past choices have been
# overwritten

Cust1.tell_purchase()

Cust2 = ReturningCustomer()
Cust2.show_budget()
Cust2.choose_food(8, 5)
Cust2.choose_food(13, 28)
Cust2.choose_food(13, 36)

Cust2.tell_purchase_history()

Cust3 = Hipster()
Cust3.choose_drink(12, 32)
Cust3.choose_food(12, 32)
Cust3.choose_drink(14, 28)
Cust3.choose_food(14, 28)
Cust3.show_budget()
Cust3.tell_purchase_history()

Cust4 = TripAdvisorCustomer()
Cust4.choose_drink(8, 5)
Cust4.choose_food(8, 5)
Cust4.make_payment()
Cust4.tell_purchase()  # amount customer spends is >3 so this works!
print(Cust4.amount_spent)
print(Cust4.customer_id)

Cust4.choose_drink(14, 32)
Cust4.choose_food(14, 32)
Cust4.make_payment()
Cust4.tell_purchase()
