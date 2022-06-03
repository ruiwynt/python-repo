import pandas as pd

df = pd.read_csv("pima.csv")
df.iloc[:,[1,4,5,6,7,8]].to_csv("cfs.csv", header=False, index=False)