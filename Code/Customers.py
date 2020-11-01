################################################################################
# Part 1 of Python Final Project: Simulation of Coffee Drinkers
# Group Partners: Andy Boomer and Jacob Pichelmann
# Part 2 involves setting up customer classes
################################################################################


# import probabilities and lists of things offered at the coffee shop
from Code.Customer_Probabilities import food_probs, drink_probs, food_list, drink_list

# Import libraries
import uuid
import names  # just for fun, can be installed with sudo pip
import numpy as np
import datetime  # For getting hour and minute from datetime objects

# set up menu of prices - maybe in other script?
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3, 'nothing': 0}


class Customer(object):
    def __init__(self):
        # less than a one in a trillion chance of repeating itself
        self.customer_id = uuid.uuid4()
        self.budget = 100
        self.name = names.get_first_name()  # just for fun
        # initialize variables for the customer
        self.food_choice = None
        self.drink_choice = None
        self.amount_spent = None
        self.time = None

    def make_choice(self, time):
        hour = time.hour  # Get the hour to be used in probability
        minute = time.minute  # Get the minute to be used in probability

        # Use the food list and probabilities to make a food choice
        food_prob = food_probs[(food_probs['hour'] == hour) & (
                food_probs['minute'] == minute)][food_list].values.tolist()[0]
        food_choice = np.random.choice(food_list, 1, p=food_prob)[0]

        # Use the drink list and probabilities to make a drink choice
        drink_prob = drink_probs[(drink_probs['hour'] == hour) & (
                drink_probs['minute'] == minute)][drink_list].values.tolist()[0]
        drink_choice = np.random.choice(drink_list, 1, p=drink_prob)[0]

        # Overwrite the initialized variables
        self.food_choice = food_choice
        self.drink_choice = drink_choice
        self.time = time

    def show_budget(self):
        # Display the customer's current budget
        print(self.name + '\'s budget is ' + str(self.budget))

    def make_payment(self):
        # Make the payment based on the price in the menu and the choices
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        # Reduce the reminining budget accordingly
        self.budget = self.budget - self.amount_spent

    def tell_purchase(self):
        # Display what the customer purchased and at what time
        print(self.name + ' bought ' + self.drink_choice + ' and ' + self.food_choice + ' for a total price of ' +
              str(self.amount_spent) + ' at ' + str(self.time))


class ReturningCustomer(Customer):  # Define a returning customer
    def __init__(self):
        super(ReturningCustomer, self).__init__()
        self.budget += 150  # they have a higher budget
        self.history = {}  # They also can remember their purchase history
        self.visit = 0  # Keep track of their current visit number

    def make_payment(self):
        # Their make payment function is slightly different with the history
        self.amount_spent = menu[self.food_choice] + menu[self.drink_choice]
        self.budget = self.budget - self.amount_spent
        self.visit += 1  # Increase the visit variable by 1
        history = {
            'customer_id': self.customer_id, 'customer_name': self.name,
            self.time: [self.drink_choice, self.food_choice]}
        self.history.update(history)

    def tell_purchase_history(self):
        print(self.history)  # Show the current history dictionary


class Hipster(ReturningCustomer):
    # Hipsters are a type of returning customer, we chose to make it a subclass
    # In case we want the hipster to have some different behavior later
    def __init__(self):
        super(Hipster, self).__init__()
        self.budget += 250  # Hipsters have an even larger budget


class TripAdvisorCustomer(Customer):
    # Trip advisor customer is a subclass of customer that adds a random tip to purchase
    def make_payment(self):
        self.amount_spent = menu[self.food_choice] + \
                            menu[self.drink_choice] + np.random.randint(1, 10)
        self.budget = self.budget - self.amount_spent


# Now test these classes for a few different actions the customers can do
time1 = datetime.datetime(2020, 6, 25, 8, 0, 0)
time2 = datetime.datetime(2020, 10, 10, 14, 32, 0)

Cust3 = Hipster()  # Create hipster returning customer

Cust3.make_choice(time1)  # Have them make their first choice
Cust3.make_payment()  # Make the payment based on the choice
Cust3.tell_purchase_history()  # Return their history

Cust3.make_choice(time2)  # They visit again at another time
Cust3.make_payment()  # They make the payment for current visit
Cust3.tell_purchase_history()  # They have a new updated history
