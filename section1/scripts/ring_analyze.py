import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read files
thin = pd.read_csv("ring_thin/times.csv")
ttimes = [el * 10 ** 6 for el in thin["time"].tolist()]

gpu = pd.read_csv("ring_gpu/times_gpu.csv")
gtimes = [el * 10 ** 6 for el in gpu["time"].tolist()]

# thin intra-socket
a1, a0 = np.polyfit(range(1, 13), ttimes[:12], 1)
thin_sock = [a0 + a1 * el for el in range(0, 14)]

# thin intra-node
b1, b0 = np.polyfit(range(13, 25), ttimes[12:24], 1)
thin_node = [b0 + b1 * el for el in range(12, 26)]

# thin out-of-node
c1, c0 = np.polyfit(range(25, 49), ttimes[24:], 1)
thin_out = [c0 + c1 * el for el in range(24, 50)]

# gpu intra-socket
d1, d0 = np.polyfit(range(1, 25), gtimes[:24], 1)
gpu_sock = [d0 + d1 * el for el in range(0, 26)]

# gpu intra-node
e1, e0 = np.polyfit(range(25, 49), gtimes[24:], 1)
gpu_node = [e0 + e1 * el for el in range(24, 50)]

# plotting
f, ax = plt.subplots(figsize=(7, 5))
ax.set_xlabel("#procs")
ax.set_xticks(range(0, 49, 4))
ax.set_ylabel("time [$\mu$sec]")

cycle_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

ax.plot(
    range(1, 13), ttimes[:12], "o", color=cycle_colors[0], label="thin (intra-socket)"
)
ax.plot(range(0, 14), thin_sock, "--", color=cycle_colors[0])

ax.plot(
    range(13, 25), ttimes[12:24], "s", color=cycle_colors[0], label="thin (intra-node)"
)
ax.plot(range(12, 26), thin_node, "--", color=cycle_colors[0])

ax.plot(
    range(25, 49), ttimes[24:], "^", color=cycle_colors[0], label="thin (out-of-node)"
)
ax.plot(range(24, 50), thin_out, "--", color=cycle_colors[0])

ax.plot(
    range(1, 25), gtimes[:24], "o", color=cycle_colors[1], label="gpu (intra-socket"
)
ax.plot(range(0, 26), gpu_sock, "--", color=cycle_colors[1])

ax.plot(
    range(25, 49), gtimes[24:], "s", color=cycle_colors[1], label="gpu (intra-socket"
)
ax.plot(range(24, 50), gpu_node, "--", color=cycle_colors[1])

ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("results/ring_plot.png")

# print latencies
data = [
    ["thin", "same socket", a1 / 2],
    ["gpu", "same socket", d1 / 2],
    ["thin", "same node", b1 / 2],
    ["gpu", "same node", e1 / 2],
    ["thin", "different nodes", c1 / 2],
]

df = pd.DataFrame(data, columns=["node", "binding", "latency[usec]"])
df.to_csv(
    path_or_buf="results/ring_table.csv",
    sep=",",
    index=False,
    float_format="%.2f",
    mode="w",
)
