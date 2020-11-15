################################################################################
# Final Part of Python Final Project: Simulation of Coffee Shop
# Group Partners: Andy Boomer and Jacob Pichelmann
# This script executes and evaluates the simulation.
################################################################################

# Import all functions and objects from other project files
from Code.SimParams import *
from Code.SimEval import *
from Code.SimFunc import *

# import python libraries
import datetime

# set up simulation data frame
# The data frame can be subsetted to a smaller sample for a faster test sim
sim_df = df['time'] + pd.DateOffset(years=5)  # shift by five years to make more realistic
sim_df = sim_df.to_frame()
sim_df['year'] = sim_df['time'].dt.year
sim_df['hour'] = sim_df['time'].dt.hour
sim_df['minute'] = sim_df['time'].dt.minute

# For each simulation in 1-5, print out the time it takes and get the df
a = datetime.datetime.now()
sim1_df = run_simulation(sim_df, Sim1)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim2_df = run_simulation(sim_df, Sim2)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim3_df = run_simulation(sim_df, Sim3)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim4_df = run_simulation(sim_df, Sim4)
print((datetime.datetime.now() - a).seconds)

a = datetime.datetime.now()
sim5_df = run_simulation(sim_df, Sim5)
print((datetime.datetime.now() - a).seconds)

# For each sim in 1-5, call the two evaluation functions
# showcase_sim gets the printed summary
# plot_sim creates the set of analysis plots
# use store_sim if you want to export the simulation to csv

showcase_sim(sim1_df, Sim1, 2)
plot_sim(sim1_df, 'sim_1')

showcase_sim(sim2_df, Sim2, 2)
plot_sim(sim2_df, 'sim_2')

showcase_sim(sim3_df, Sim3, 2)
plot_sim(sim3_df, 'sim_3')

showcase_sim(sim4_df, Sim4, 2)
plot_sim(sim4_df, 'sim_4')

showcase_sim(sim5_df, Sim5, 2)
plot_sim(sim5_df, 'sim_5')
