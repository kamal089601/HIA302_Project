#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

filepath = '/Users/azfar/Documents/GitHub/group-project/Data Files'

# Import original datasets into specified DataFrames
df = pd.read_csv(filepath+'/for_analysis.csv')

# Distribution of total doses between brands
total_allvax = df['total_doses'].sum()

print('pfizer:'+str(df['total_doses'].loc[0])+'\n'+
      'astra: '+str(df['total_doses'].loc[1])+'\n'+
      'svac: '+str(df['total_doses'].loc[2])+'\n'+
      'spharm: '+str(df['total_doses'].loc[3]))
pct_pfizer = 45070100 / total_allvax * 100
pct_astra = 5708790 / total_allvax * 100
pct_sinov = 21584481 / total_allvax * 100
pct_sinop = 44309 / total_allvax * 100

# Incidence of AEFI in all brands
aefi_pfizer = float(df['daily_total'].loc[0]) / 45070100
aefi_astra = float(df['daily_total'].loc[1]) / 5708790
aefi_sinov = float(df['daily_total'].loc[2]) / 21584481
aefi_sinop = float(df['daily_total'].loc[3]) / 44309

pct_aefi_pfizer = aefi_pfizer * 100
pct_aefi_astra = aefi_astra * 100
pct_aefi_sinov = aefi_sinov * 100
pct_aefi_sinop = aefi_sinop * 100

print(pct_aefi_astra)
print(pct_aefi_pfizer)
print(pct_aefi_sinov)
print(pct_aefi_sinop)

# Pie chart for total doses given
labels = 'Pfizer', 'Astrazeneca', 'Sinovac', 'Sinopharm'
sizes = [45070100, 5708790, 21584481, 44309]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels)