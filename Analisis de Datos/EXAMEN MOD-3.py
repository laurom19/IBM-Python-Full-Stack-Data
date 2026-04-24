import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('automoviles_limpios_dummies.csv')
print(df.head())
print(df.columns)

df_test = df[['ESTILO_CARROCERIA','PRECIO']]
df_grp = df_test.groupby(['ESTILO_CARROCERIA'], as_index=False).mean()
print (df_grp['PRECIO'])