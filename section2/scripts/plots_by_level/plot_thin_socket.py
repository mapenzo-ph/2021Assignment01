import matplotlib.pyplot as plt
import pandas as pd

# get first dataset
df = pd.read_csv('clean/thin_socket_ucx.csv')
ucx_times = df['t[usec]'].tolist()
ucx_fit = df['t[usec]_computed'].tolist()
ucx_bw = df['Mbytes/sec'].tolist()
ucx_bwc = df['Mbytes/sec_computed'].tolist()

# get second dataset
df = pd.read_csv('clean/thin_socket_intel.csv')
intel_times = df['t[usec]'].tolist()
intel_fit = df['t[usec]_computed'].tolist()
intel_bw = df['Mbytes/sec'].tolist()
intel_bwc = df['Mbytes/sec_computed'].tolist()

# get third dataset
df = pd.read_csv('clean/thin_socket_tcp.csv')
tcp_times = df['t[usec]'].tolist()
tcp_fit = df['t[usec]_computed'].tolist()
tcp_bw = df['Mbytes/sec'].tolist()
tcp_bwc = df['Mbytes/sec_computed'].tolist()

# get fourth dataset
vader_df = pd.read_csv('clean/thin_socket_vader.csv')
vader_times = vader_df['t[usec]'].tolist()
vader_fit = vader_df['t[usec]_computed'].tolist()
vader_bw = vader_df['Mbytes/sec'].tolist()
vader_bwc = vader_df['Mbytes/sec_computed'].tolist()

# colors and x axis
cycle_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
bytez = df['#bytes'].tolist()

# initialize plot
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 10))

# plot times
ax1.set_xlabel('#bytes')
ax1.set_ylabel('time [$\mu$sec]')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.plot(bytez, ucx_times, ':s', color=cycle_colors[0], label='ucx')
ax1.plot(bytez, ucx_fit, '-', color=cycle_colors[0])
ax1.plot(bytez, intel_times, ':s', color=cycle_colors[1], label='intel')
ax1.plot(bytez, intel_fit, '-', color=cycle_colors[1])
ax1.plot(bytez, tcp_times, ':s', color=cycle_colors[2], label='self,tcp')
ax1.plot(bytez, tcp_fit, '-', color=cycle_colors[2])
ax1.plot(bytez, vader_times, ':s', color=cycle_colors[3], label='self,vader')
ax1.plot(bytez, vader_fit, '-', color=cycle_colors[3])
ax1.legend(loc='upper left')

# plot bandwidths
ax2.set_xlabel('#bytes')
ax2.set_ylabel('bandwidth [Mb/s]')
ax2.set_xscale('log')
# ax2.set_yscale('log')
ax2.plot(bytez, ucx_bw, ':s', color=cycle_colors[0], label='ucx')
ax2.plot(bytez, ucx_bwc, '-', color=cycle_colors[0])
ax2.plot(bytez, intel_bw, ':s', color=cycle_colors[1], label='intel')
ax2.plot(bytez, intel_bwc, '-', color=cycle_colors[1])
ax2.plot(bytez, tcp_bw, ':s', color=cycle_colors[2], label='self,tcp')
ax2.plot(bytez, tcp_bwc, '-', color=cycle_colors[2])
ax2.plot(bytez, vader_bw, ':s', color=cycle_colors[3], label='self,vader')
ax2.plot(bytez, vader_bwc, '-', color=cycle_colors[3])
ax2.legend(loc='upper left')

f.tight_layout()
# plt.show()
plt.savefig('results/plots_by_level/plot_thin_socket.png')
