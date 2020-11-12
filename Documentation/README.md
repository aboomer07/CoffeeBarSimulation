# Simulating a Coffee Shop

This project simulates customers visiting a coffee shop over a time span of 5 years, based on empirical input data.

## Getting Started

You already found the READ ME, so well done, the hardest part is behind you! In case you have not yet cloned the repository, please navigate to
https://bitbucket.org/aboomer07/examtse2020-21/src/master/ and clone the repository to your local machine.

### Prerequisites

* Python 3.8 up and running, preferably via anaconda. 
Non-standard libraries might have to be installed prior to executing the program: 
* uuid (pip install uuid)
* names (sudo pip install names)

## Code Structure
![CodeStructure](FileDiagram.png)

## Evaluating the simulation

The simulated process can be evaluated via two functions: 
``` 
showcase_sim(sim, params, n_example) 
```
Takes in the simulated data frame, it's underlying parameters and the number of examples that should be shown.
Returns _n_example_ randomly selected simulated customers and showcases their functionality and purchasing history.

``` 
plot_sim(sim, ind) 
```

Takes as arguments the simulated data frame and and a string indicator to name the resulting plots (e.g. 'sim_1').
Returns a set of plots to evaluate the simulation and compare simulation runs.

## Storing the simulation

* store_sim(sim, ind) 
Exports the simulated data as a csv file to your output folder.

## Versioning


## Authors

* **Andy Boomer**

* **Jacob Pichelmann**

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
