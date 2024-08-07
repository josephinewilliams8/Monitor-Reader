import pandas as pd

df = pd.DataFrame({'date':[], 'time':[], 'sm3/h':[], 'sm3':[]})
df.to_csv('Monitor Reading.csv', sep=',', index=False, encoding='utf-8')