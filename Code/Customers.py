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
from Code.Customer_Probabilities import FoodProbs, DrinkProbs, FoodList, DrinkList
# Import libraries
import uuid
import names  # just for fun
import numpy as np

# Each customer has a customerID and a certain budget. Based on the shape example in the slides the budget
# is not introduced at the super class level.

# set up menu of prices - maybe in other script?
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3,
        'milkshake': 5, 'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}


class Customer(object):
    def __init__(self):
        self.CustomerID = uuid.uuid4()  # less than a one in a trillion chance of repeating itself
        self.budget = 100
        self.name = names.get_first_name()  # just for fun

    def chooseFood(self, HOUR, MINUTE):
        prob = FoodProbs[(FoodProbs['HOUR'] == HOUR) & (FoodProbs['MINUTE'] == MINUTE)][FoodList].values.tolist()[0]
        FoodChoice = np.random.choice(FoodList, 1, p=prob)[0]
        self.FoodChoice = FoodChoice
        self.Time = str(HOUR) + ':' + str(MINUTE)  # this is ugly and needs to be changed
        return self.FoodChoice

    def chooseDrink(self, HOUR, MINUTE):
        prob = DrinkProbs[(DrinkProbs['HOUR'] == HOUR) & (DrinkProbs['MINUTE'] == MINUTE)][DrinkList].values.tolist()[0]
        DrinkChoice = np.random.choice(DrinkList, 1, p=prob)[0]
        self.DrinkChoice = DrinkChoice
        return self.DrinkChoice

    def showBudget(self):
        print(self.name + '\'s budget is ' + str(self.budget))

    def makePayment(self):
        self.amount_spent = menu[self.FoodChoice] + menu[self.DrinkChoice]
        self.budget = self.budget - self.amount_spent

    def tellPurchase(self):
        print(self.name + ' bought ' + self.DrinkChoice + ' and ' + self.FoodChoice + ' for a total price of ' +
              str(self.amount_spent) + ' at ' + self.Time)


class ReturningCustomer(Customer):
    def __init__(self):
        super(ReturningCustomer, self).__init__()
        self.budget += 150
        self.FoodChoiceHistory = []
        self.DrinkChoiceHistory = []

    def tellPurchaseHistory(self):
        print(self.FoodChoiceHistory)
        print(self.DrinkChoiceHistory)

    def chooseFood(self, HOUR, MINUTE):
        FoodChoice = FoodProbs[(FoodProbs['HOUR'] == HOUR) & (FoodProbs['MINUTE'] == MINUTE)]['max_prob']
        self.FoodChoice = FoodChoice.to_string(index=False).strip()
        self.FoodChoiceHistory.append(FoodChoice.to_string(index=False).strip())
        self.Time = str(HOUR) + ':' + str(MINUTE)  # this is ugly and needs to be changed
        return self.FoodChoice

    def chooseDrink(self, HOUR, MINUTE):
        DrinkChoice = DrinkProbs[(DrinkProbs['HOUR'] == HOUR) & (DrinkProbs['MINUTE'] == MINUTE)]['max_prob']
        self.DrinkChoice = DrinkChoice.to_string(index=False).strip()
        self.DrinkChoiceHistory.append(DrinkChoice.to_string(index=False).strip())
        return self.DrinkChoice


class Hipster(ReturningCustomer):
    def __init__(self):
        super(Hipster, self).__init__()
        self.budget += 250


class TripAdvisorCustomer(Customer):
    def makePayment(self):  # is overwirting a method bad style?
        self.amount_spent = menu[self.FoodChoice] + menu[self.DrinkChoice] + np.random.randint(1, 10)
        self.budget = self.budget - self.amount_spent


# in this current set up we would not necessarily have to set up a class for one time customers - is this a mistake?


Cust1 = Customer()
Cust1.showBudget()

print(Cust1.chooseDrink(8, 5))
print(Cust1.chooseFood(8, 5))  # in the morning he wants coffee and nothing to eat
print(Cust1.FoodChoice)

# print(Cust1.chooseFood(14, 30))
# 14:30 has no records so this returns nothing weird Series string, need to add
# error!

print(Cust1.chooseDrink(12, 32))
print(Cust1.chooseFood(12, 32))  # for lunch he wants soda and a sandwich

Cust1.makePayment()
Cust1.showBudget()  # soda and sandwich cost 5 in total, so this works. Note that the past choices have been
# overwritten

Cust1.tellPurchase()

Cust2 = ReturningCustomer()
Cust2.showBudget()
Cust2.chooseFood(8, 5)
Cust2.chooseFood(13, 28)
Cust2.chooseFood(13, 36)

Cust2.tellPurchaseHistory()

Cust3 = Hipster()
Cust3.chooseDrink(12, 32)
Cust3.chooseFood(12, 32)
Cust3.chooseDrink(14, 28)
Cust3.chooseFood(14, 28)
Cust3.showBudget()
Cust3.tellPurchaseHistory()

Cust4 = TripAdvisorCustomer()
Cust4.chooseDrink(8, 5)
Cust4.chooseFood(8, 5)
Cust4.makePayment()
Cust4.tellPurchase()  # amount customer spends is >3 so this works!
print(Cust4.amount_spent)
print(Cust4.CustomerID)
