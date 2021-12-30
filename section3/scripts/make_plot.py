import matplotlib.pyplot as plt
import pandas as pd

# read all data from csv
df = pd.read_csv('results/jacobi_table.csv')
procs = df['#procs'].tolist()

thin_exp = df['P_exp[MLUPs](t)'].tolist()
thin_prg = df['P_prg[MLUPs](t)'].tolist()

gpu_exp = df['P_exp[MLUPs](g)'].tolist()
gpu_prg = df['P_prg[MLUPs](g)'].tolist()

# initialize plot
f, [ax1, ax2] = plt.subplots(1, 2, figsize=(9, 4))

# first subplot
ax1.set_xlabel('#procs')
ax1.set_ylabel('P[MLUPs]')
ax1.set_title('thin node')
ax1.plot(procs, thin_exp, '--s', label='expected')
ax1.plot(procs, thin_prg, 'o', label='program')
ax1.legend(loc='lower right')

# second subplot
ax2.set_xlabel('#procs')
ax2.set_ylabel('P[MLUPs]')
ax2.set_title('gpu node')
ax2.plot(procs, gpu_exp, '--s', label='expected')
ax2.plot(procs, gpu_prg, 'o', label='program')
ax2.legend(loc='lower right')

# plot and save
plt.tight_layout()
plt.savefig('results/jacobi_plot.png')
