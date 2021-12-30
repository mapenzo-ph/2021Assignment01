import matplotlib.pyplot as plt
import pandas as pd

# get first dataset
ucx_df = pd.read_csv('clean/gpu_socket_ucx.csv')
ucx_times = ucx_df['t[usec]'].tolist()
ucx_fit = ucx_df['t[usec]_computed'].tolist()
ucx_bw = ucx_df['Mbytes/sec'].tolist()
ucx_bwc = ucx_df['Mbytes/sec_computed'].tolist()

# get second dataset
intel_df = pd.read_csv('clean/gpu_socket_intel.csv')
intel_times = intel_df['t[usec]'].tolist()
intel_fit = intel_df['t[usec]_computed'].tolist()
intel_bw = intel_df['Mbytes/sec'].tolist()
intel_bwc = intel_df['Mbytes/sec_computed'].tolist()

# get third dataset
tcp_df = pd.read_csv('clean/gpu_socket_tcp.csv')
tcp_times = tcp_df['t[usec]'].tolist()
tcp_fit = tcp_df['t[usec]_computed'].tolist()
tcp_bw = tcp_df['Mbytes/sec'].tolist()
tcp_bwc = tcp_df['Mbytes/sec_computed'].tolist()

# get fourth dataset
vader_df = pd.read_csv('clean/gpu_socket_vader.csv')
vader_times = vader_df['t[usec]'].tolist()
vader_fit = vader_df['t[usec]_computed'].tolist()
vader_bw = vader_df['Mbytes/sec'].tolist()
vader_bwc = vader_df['Mbytes/sec_computed'].tolist()

# colors and x axis
cycle_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
bytez = ucx_df['#bytes'].tolist()

# initialize plot for times
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
plt.savefig('results/plots_by_level/plot_gpu_socket.png')
