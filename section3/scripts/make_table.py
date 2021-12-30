import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = "{:,.2f}".format

# read values and sort using #procs and node type
data = pd.read_csv("results/jacobi_data.csv")
data.sort_values(["#procs", "type"], ascending=[True, True], inplace=True)
data.reset_index(drop=True, inplace=True)

# find k from grid
kx = [2 if el > 1 else 0 for el in data["nx"]]
ky = [2 if el > 1 else 0 for el in data["ny"]]
kz = [2 if el > 1 else 0 for el in data["nz"]]
k_vals = [sum(ks) for ks in zip(kx, ky, kz)]
data["k"] = k_vals

# compute c using k
data["c(k)[MB]"] = [1200 * 1200 * k * 2 * 8 / 10 ** 6 for k in k_vals]

# import network data and join dfs
network_data = pd.read_csv("results/network_data.csv")
data = data.merge(network_data, on=["type", "comm_level"], how="outer")

# find baseline serial times
serial_thin = data[data["type"] == "thin"]["T_tot[sec]"].tolist()[0]
print(serial_thin)
serial_gpu = data[data["type"] == "gpu"]["T_tot[sec]"].tolist()[0]
print(serial_gpu)
data["Ts[sec]"] = [
    serial_thin if data["type"][i] == "thin" else serial_gpu for i in range(len(k_vals))
]

# compute communication times from model
data["Tc[sec]"] = data["c(k)[MB]"] / (data["bw[GB/s]"] * 10 ** 3) + data["k"] * (
    data["lat[usec]"] / 10 ** 6
)

# compute communication times from data
data["test"] = (data["T_tot[sec]"] - data["T_sweep[sec]"])*data['#procs']
base = data["test"].tolist()[0]
data["test"] = (data["test"] - base)/data['#procs']
# compute performance
data["P_exp[MLUPs]"] = (
    1200
    * 1200
    * 1200
    * data["#procs"]
    / (data["Ts[sec]"] + data["Tc[sec]"])
    / 10 ** 6
)

# drop useless columns and reorder
data.drop(columns=["Ts[sec]", "lat[usec]", "bw[GB/s]", 'T_sweep[sec]', 'T_tot[sec]', 'test'], inplace=True)
data = data[['type', 'comm_level', '#procs', 'nx', 'ny', 'nz', 'k', 'c(k)[MB]', 'Tc[sec]', 'P_exp[MLUPs]', 'P_prg[MLUPs]']]

# split thin and gpu and merge back
dfthin = data[data["type"] == "thin"].copy()
dfthin.drop(
    columns=[
        "type",
    ],
    inplace=True
)
dfthin.rename(
    columns={
        "Tc[sec]": "Tc[sec](t)",
        "P_exp[MLUPs]": "P_exp[MLUPs](t)",
        "P_prg[MLUPs]": "P_prg[MLUPs](t)",
    },
    inplace=True
)

dfgpu = data[data["type"] == "gpu"].copy()
dfgpu.drop(
    columns=[
        "type",
    ],
    inplace=True
)
dfgpu.rename(
    columns={
        "Tc[sec]": "Tc[sec](g)",
        "P_exp[MLUPs]": "P_exp[MLUPs](g)",
        "P_prg[MLUPs]": "P_prg[MLUPs](g)",
    },
    inplace=True
)

data = dfthin.merge(dfgpu, on=['#procs','nx','ny','nz','k','comm_level', 'c(k)[MB]'], how='outer')

# save on file
data.to_csv(
    path_or_buf="results/jacobi_table.csv",
    sep=",",
    mode="w",
    index=False,
    float_format="%.4lf",
)

print(data.head(10))