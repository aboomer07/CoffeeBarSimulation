from Code.SimFunc import *
from Code.SimEval import *

# set up simulation data frame
sim_df = df[['time', 'year', 'hour', 'minute']][:30000]

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

