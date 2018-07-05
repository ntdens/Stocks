import pandas as pd

df = pd.read_csv('CME-FCK2019.csv')
df.set_index('Date', inplace=True)
print(df)