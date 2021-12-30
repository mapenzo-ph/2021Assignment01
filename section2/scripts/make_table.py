import pandas as pd

table = pd.read_csv('results/tmp_table.csv')

# get gpu val
dfgpu = table[table['type']=='gpu'].copy()  # take all gpu entries
dfgpu.drop(columns=['type',], inplace=True)
dfgpu.rename(columns={'latency':'lat[usec](gpu)', 
            'bandwidth':'bw[GB/s](gpu)'}, inplace=True)

#remove gpu vals from all
dfthin = table[table['type']=='thin'].copy() # take all thin entries
dfthin.drop(columns=['type',], inplace=True)
dfthin.rename(columns={'latency': 'lat[usec](thin)',
           'bandwidth': 'bw[GB/s](thin)'}, inplace=True)

#merge dataframes over all columns in common
all = dfthin.merge(dfgpu, on=['level', 'framework'])
all.rename(columns={'framework':'components', 'level':'map-by'}, inplace=True)

def order(x):
        if x == 'core': return 1
        elif x == 'socket': return 2
        elif x == 'node': return 3
        else: raise ValueError

all['level'] = list(map(order, all['map-by']))
all.sort_values(by=['level', 'lat[usec](thin)'], inplace=True)
all.drop(columns=['level',], inplace=True)
all.to_csv(path_or_buf='results/pp_table.csv', sep=',', mode='w', index=False)


# core = all[all['level']=='core'] # take only core
# core.drop(columns=['level',], inplace=True)

# socket = all[all['level'] == 'socket']  # take only socket
# socket.drop(columns=['level', ], inplace=True)

# node = all[all['level'] == 'node']  # take only node
# node.drop(columns=['level', ], inplace=True)


