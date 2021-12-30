import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# things to plot:
# - bw for ucx
# - bw for vader
# - bw for intel
# - bw fot tcp

# open plot
f, ax = plt.subplots(2, 2, figsize=(10, 7))
ax = np.reshape(ax, (4, 1))
# colors
cycle_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# get data
fwks = ["ucx", "vader", "intel", "tcp"]

for fwk in fwks:
    idx = fwks.index(fwk)
    axi = ax[idx][0]

    df = pd.read_csv(f"clean/thin_core_{fwk}.csv")
    core_bw = df["Mbytes/sec"].tolist()
    core_bwc = df["Mbytes/sec_computed"].tolist()

    df = pd.read_csv(f"clean/thin_socket_{fwk}.csv")
    sock_bw = df["Mbytes/sec"].tolist()
    sock_bwc = df["Mbytes/sec_computed"].tolist()

    bytez = df["#bytes"].tolist()

    # plot bandwidths
    axi.set_title(f"{fwk}")
    axi.set_xlabel("#bytes")
    axi.set_ylim([1 / 10000, 22000])
    axi.set_xscale("log")
    # ax2.set_yscale('log')
    axi.plot(bytez, core_bw, ":o", color=cycle_colors[9], label="core")
    axi.plot(bytez, core_bwc, "-", color=cycle_colors[9])
    axi.plot(bytez, sock_bw, ":s", color=cycle_colors[8], label="socket")
    axi.plot(bytez, sock_bwc, "-", color=cycle_colors[8])

    if fwk != "vader":
        df = pd.read_csv(f"clean/thin_node_{fwk}.csv")
        node_bw = df["Mbytes/sec"].tolist()
        node_bwc = df["Mbytes/sec_computed"].tolist()
        axi.plot(bytez, node_bw, ":^", color=cycle_colors[7], label="node")
        axi.plot(bytez, node_bwc, "-", color=cycle_colors[7])

    axi.vlines(1048576, 1 / 1000, 21000, linestyles="-.", color="grey", label="L2 size")
    axi.vlines(
        19 * 1048576, 1 / 10, 21000, linestyles="--", color="grey", label="L3 size"
    )

ax[0][0].set_ylabel("bandwidth [GB/s]")
ax[0][0].set_yticks([4000,8000,12000,16000,20000])
ax[0][0].set_yticklabels([4,8,12,16,20])
ax[1][0].set_yticks([])
ax[2][0].set_ylabel("bandwidth [GB/s]")
ax[2][0].set_yticks([4000,8000,12000,16000,20000])
ax[2][0].set_yticklabels([4,8,12,16,20])
ax[3][0].set_yticks([])
ax[0][0].legend(loc="upper left")

plt.tight_layout()
plt.savefig('results/pp_plot.png')
