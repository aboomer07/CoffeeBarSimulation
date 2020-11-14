# Import the necessary python libraries dataframe
import numpy as np
from Code.CustomerProbabilities import df

# Initialize the basic menu defined in the project scope
menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3,
        'nothing': 0}

# One of the simulations involves a 20% increase in prices
menu_20pct = {key: (1.2 * val) for key, val in menu.items()}

# Full array of base prices, and one with prices changing in 2018
base_prices = np.array([menu for i in range(df.shape[0])])
prices_2018 = np.where(df['year'].values < 2018, base_prices, np.array(
    [menu_20pct for j in range(len(base_prices))]))

# The first simulation is all the base parameters defined in the project
Sim1 = {
    'data_params': {  # Use to access the menu prices at each iteration in sim
        'menus': base_prices},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

# The second simulation lowers the pool of returning customers to 50
Sim2 = {
    'data_params': {  # Use to access the menu prices at each iteration in sim
        'menus': base_prices},
    'class_params': {
        'num_returns': 50,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

# The third simulation includes the prices that increase by 20% in 2018
Sim3 = {
    'data_params': {  # Use to access the menu prices at each iteration in sim
        'menus': prices_2018},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

# The fourth simulation lowers the budget of the hipster to 40
Sim4 = {
    'data_params': {  # Use to access the menu prices at each iteration in sim
        'menus': base_prices},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 40, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

# The fifth simulation changes the hipster choice to the least probable option
Sim5 = {
    'data_params': {  # Use to access the menu prices at each iteration in sim
        'menus': base_prices},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': True},
        'empty_interval': np.nan
    }
}
