import pandas as pd

df = pd.read_csv('../input/MTA-Bus-Time_.2014-08-01.txt', sep = '\t')
print(len(df))

df.dropna(inplace = True)
print(len(df))

df.to_csv('../input/data.txt', index = False, sep = '\t')
