import matplotlib.pyplot as plt 
import pandas as pd

# get data
df = pd.read_csv('clean/gpu_core_intel.csv')
core_times = df['t[usec]'].tolist()
core_fit = df['t[usec]_computed'].tolist()
core_bw = df['Mbytes/sec'].tolist()
core_bwc = df['Mbytes/sec_computed'].tolist()

df = pd.read_csv('clean/gpu_socket_intel.csv')
sock_times = df['t[usec]'].tolist()
sock_fit = df['t[usec]_computed'].tolist()
sock_bw = df['Mbytes/sec'].tolist()
sock_bwc = df['Mbytes/sec_computed'].tolist()

df = pd.read_csv('clean/gpu_node_intel.csv')
node_times = df['t[usec]'].tolist()
node_fit = df['t[usec]_computed'].tolist()
node_bw = df['Mbytes/sec'].tolist()
node_bwc = df['Mbytes/sec_computed'].tolist()

# colors and x axis
cycle_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
bytez = df['#bytes'].tolist()

# initialize plot for times
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(7,10))

# plot times
ax1.set_xlabel('#bytes')
ax1.set_ylabel('time [$\mu$sec]')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.plot(bytez, core_times, ':o', color=cycle_colors[9], label='core')
ax1.plot(bytez, core_fit, '-', color=cycle_colors[9])
ax1.plot(bytez, sock_times, ':s', color=cycle_colors[8], label='socket')
ax1.plot(bytez, sock_fit, '-', color=cycle_colors[8])
ax1.plot(bytez, node_times, ':^', color=cycle_colors[7], label='node')
ax1.plot(bytez, node_fit, '-', color=cycle_colors[7])
ax1.legend(loc='upper left')

# plot bandwidths
ax2.set_xlabel('#bytes')
ax2.set_ylabel('bandwidth [Mb/s]')
ax2.set_xscale('log')
# ax2.set_yscale('log')
ax2.plot(bytez, core_bw, ':o', color=cycle_colors[9], label='core')
ax2.plot(bytez, core_bwc, '-', color=cycle_colors[9])
ax2.plot(bytez, sock_bw, ':s', color=cycle_colors[8], label='socket')
ax2.plot(bytez, sock_bwc, '-', color=cycle_colors[8])
ax2.plot(bytez, node_bw, ':^', color=cycle_colors[7], label='node')
ax2.plot(bytez, node_bwc, '-', color=cycle_colors[7])

ax2.legend(loc='upper left')

f.tight_layout()
# plt.show()
plt.savefig('results/plots_by_framework/plot_gpu_intel.png')
