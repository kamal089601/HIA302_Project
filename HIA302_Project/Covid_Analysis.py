import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('aefi.csv')

null_value = df.isna().sum()

shape = df.shape

columns = df.columns

new_df = df.drop(['date', 'daily_total', 'daily_serious_npra', 'daily_nonserious', 
         'daily_nonserious_npra', 'd1_site_pain', 'd2_site_pain'], axis=1, inplace=True)

value_counts = df['vaxtype'].value_counts()

result = df[df['vaxtype'].isin(['pfizer', 'sinovac', 'astrazeneca', 'sinopharm'])].groupby('vaxtype').sum()

result.to_csv('new_aefi.csv')

describe = result.describe()


print(test)