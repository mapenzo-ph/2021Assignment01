import pandas as pd

# reading dataframes and sorting
df800 = pd.read_csv("results/matrix_800.csv")
df800.rename(columns={"time[sec]": "800x300x100"}, inplace=True)
df800.sort_values(
    by=[
        "nx",
    ],
    ascending=False,
    inplace=True,
)
print(df800.head(7))
print("\n")

df1200 = pd.read_csv("results/matrix_1200.csv")
df1200.rename(columns={"time[sec]": "1200x200x100"}, inplace=True)
df1200.sort_values(
    by=[
        "nx",
    ],
    ascending=False,
    inplace=True,
)
print(df1200.head(7))
print("\n")

df2400 = pd.read_csv("results/matrix_2400.csv")
df2400.rename(columns={"time[sec]": "2400x100x100"}, inplace=True)
df2400.sort_values(
    by=[
        "nx",
    ],
    ascending=False,
    inplace=True,
)
print(df2400.head(7))
print("\n")

data = df800.merge(df1200, how="outer", on=["nx", "ny", "nz"]).merge(
    df2400, how="outer", on=["nx", "ny", "nz"]
)
data.to_csv(
    path_or_buf="results/matrix_table.csv", mode='w', sep=",", float_format="%.4f", index=False
)
