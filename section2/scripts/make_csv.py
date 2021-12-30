from sys import argv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


##### set up result files #############
name = argv[1].split(sep='/')[1]
res_file = 'upload/'+name+'.csv' 

##### set up number of files to analyze 
nreps = int(argv[2])


##### computing averages of times and bandwidths 
times = np.zeros((nreps,30))
bandwds = np.zeros((nreps,30))

for i in range(nreps):
    file = argv[1]+'/run_'+str(i)+'_tmp'
    df = pd.read_csv(file)
    
    if (i==0):
        bytez = np.array(df['#bytes'].tolist())
        reps = np.array(df['#repetitions'].tolist())

    times[i,:] = np.array(df['t[usec]'].tolist())
    bandwds[i,:] = np.array(df['Mbytes/sec'].tolist())

times = (times.T).sum(axis=1)/nreps
bandwds = (bandwds.T).sum(axis=1)/nreps


##### fitting data ####################
_ , latency = np.polyfit(bytez[0:8], times[0:8], 1)
invBW, _ = np.polyfit(bytez[8:], times[8:]-latency*np.ones_like(times[8:]), 1)


##### writing results #################
res = open(res_file, 'a')
print('# Computed latency: {0:.3g} usec | Computed bandwidth: {1:.2g} Gb/s |'.format(latency, 1/invBW/1000), \
        end='\n', file=res)

results = pd.DataFrame(columns = ['#bytes','#repetitions','t[usec]','t[usec]_computed', 'Mbytes/sec', 'Mbytes/sec_computed'])
results['#bytes'] = bytez
results['#repetitions'] = reps
results['t[usec]']= times
results['Mbytes/sec'] = bandwds
t_computed = latency+(invBW*bytez)
results['t[usec]_computed'] = t_computed

def inverse(x):
    return 1/x
inverse_times = inverse(t_computed)

bw_computed = bytez*inverse_times
results['Mbytes/sec_computed'] = bw_computed
print(results.to_string(index=False), file=res)
res.close

