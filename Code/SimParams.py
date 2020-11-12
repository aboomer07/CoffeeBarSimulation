import numpy as np
from Code.Customer_Probabilities import df

menu = {'sandwich': 2, 'cookie': 2, 'pie': 3, 'muffin': 3, 'milkshake': 5,
        'frappucino': 4, 'water': 2, 'coffee': 3, 'soda': 3, 'tea': 3, 'nothing': 0}
menu_20pct = {key: (1.2 * val) for key, val in menu.items()}

base_prices = np.array([menu for i in range(df.shape[0])])
prices_2018 = np.where(df['year'].values < 2018, base_prices, np.array(
    [menu_20pct for j in range(len(base_prices))]))

Sim1 = {
    'data_params': {
        'menus': base_prices},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

Sim2 = {
    'data_params': {
        'menus': base_prices},
    'class_params': {
        'num_returns': 50,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

Sim3 = {
    'data_params': {
        'menus': prices_2018},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

Sim4 = {
    'data_params': {
        'menus': base_prices},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 40, 'inv_choice': False},
        'empty_interval': np.nan
    }
}

Sim5 = {
    'data_params': {
        'menus': base_prices},
    'class_params': {
        'num_returns': 1000,
        'one_time': {'budget': 100},
        'returning': {'budget': 250},
        'hipster': {'budget': 500, 'inv_choice': True},
        'empty_interval': np.nan
    }
}
