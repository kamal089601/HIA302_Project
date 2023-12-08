#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 19:17:04 2023

@author: hanienyee
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate


def percent(a, b):
    percentage = (a/b)*100
    return percentage

# blues=['mediumturquoise', 'teal', 'powderblue', 'cadetblue', 'paleturquoise', 'aquamarine']
# reds = ['indianred', 'steelblue']


df1 = pd.read_csv('Latest_covid_datasets.csv')

df1.columns

#sum up and group by vaxtype
df1_sum = df1.groupby('vaxtype')[['daily_total', 'daily_nonserious_mysj_dose1',
       'daily_nonserious_mysj_dose2', 'd1_site_swelling', 'd1_site_redness',
       'd1_tiredness', 'd1_headache', 'd1_muscle_pain', 'd1_joint_pain',
       'd1_weakness', 'd1_fever', 'd1_vomiting', 'd1_chills', 'd1_rash',
       'd2_site_swelling', 'd2_site_redness', 'd2_tiredness', 'd2_headache',
       'd2_muscle_pain', 'd2_joint_pain', 'd2_weakness', 'd2_fever',
       'd2_vomiting', 'd2_chills', 'd2_rash','pfizer1', 'pfizer2', 'sinovac1',
       'sinovac2', 'astra1', 'astra2']].sum()


#organising data merged from vax_malaysia.csv
## column for total administered dose 1
Total_D1_admin = [df1_sum.loc['astrazeneca', 'astra1'], df1_sum.loc['pfizer', 'pfizer1'], df1_sum.loc['sinovac', 'sinovac1']]
df1_sum['Total_D1_admin'] = Total_D1_admin

## column for total administered dose 2
Total_D2_admin = [df1_sum.loc['astrazeneca', 'astra2'], df1_sum.loc['pfizer', 'pfizer2'], df1_sum.loc['sinovac', 'sinovac2']]
df1_sum['Total_D2_admin'] = Total_D2_admin

## column of total dose 1 and 2 administered
Total_dose_admin = df1_sum[['Total_D1_admin', 'Total_D2_admin']].sum(axis=1)
df1_sum['Total_dose_admin'] = Total_dose_admin

## dropping columns that are no more needed
df1_sum = df1_sum.drop(['pfizer1', 'pfizer2', 'sinovac1','sinovac2', 'astra1', 'astra2'], axis=1)

df1_sum.insert(0, column = "vaxtype", value = df1_sum.index)

## saving dataframe as csv file
df1_sum.to_csv('Summarized_Covid_Vax_SEs.csv')



# Percentage of total SE reported for each vaccine (d1,d2 vs vaxtype)
## Q: Which vax is more likely to present with side effects?

## (total SE 1 & 2 / total dose administered)
TotalSE_TotalDose = df1_sum[['daily_nonserious_mysj_dose1',
       'daily_nonserious_mysj_dose2']].apply(lambda x: percent(x, df1_sum['Total_dose_admin']))
TotalSE_TotalDose.insert(0, column = "vaxtype", value = TotalSE_TotalDose.index)
TotalSE_TotalDose.to_csv('TotalSE_percentage_byVax.csv')

## dose 1 and dose 2 % over Total administered, grouped by vaxtype
TotalSE_TotalDose.plot(kind='bar', stacked=True, color=['powderblue', 'palevioletred'], width=0.5)
plt.xlabel("Type of Vaccine")
plt.ylabel("Percentage (%)")
plt.title("Percentage of non-serious side effects \nreported based on Vaccination type", fontsize=16)
plt.legend(labels = ['Dose 1', 'Dose 2'])


## (total SE1/ total D1 ; total SE2/ total D2)
TotalSEoverDose = pd.DataFrame()
TotalSEoverDose['TotalSE1_D1_pct'] = percent(df1_sum['daily_nonserious_mysj_dose1'], df1_sum['Total_D1_admin'])
TotalSEoverDose['TotalSE2_D2_pct'] = percent(df1_sum['daily_nonserious_mysj_dose2'], df1_sum['Total_D2_admin'])
TotalSEoverDose= TotalSEoverDose.transpose()

z = TotalSEoverDose.rename({'TotalSE1_D1_pct':'Dose 1', 'TotalSE2_D2_pct':'Dose 2'})
z.plot(kind='bar', stacked=False, color=['skyblue', 'pink', 'plum'])
plt.xlabel("")
plt.ylabel("Percentage (%)")
plt.title("Percentage of non-serious side effects reported \npost-vaccination for Dose 1 and Dose 2 respectively", fontsize=16)
plt.legend(title='Vaccination Type')



# Percentage of occurence of SE for each vaccine
## Q: Which are the common symptoms associated with each vaccines?


#grouping column names
d1_cols = ['d1_site_swelling', 'd1_site_redness',
'd1_tiredness', 'd1_headache', 'd1_muscle_pain', 'd1_joint_pain',
'd1_weakness', 'd1_fever', 'd1_vomiting', 'd1_chills', 'd1_rash']

d2_cols = ['d2_site_swelling', 'd2_site_redness', 'd2_tiredness', 'd2_headache',
'd2_muscle_pain', 'd2_joint_pain', 'd2_weakness', 'd2_fever',
'd2_vomiting', 'd2_chills', 'd2_rash']


## Dose 1
# dataframe with only dose 1 SE, apply percentage function
D1symp_pct = df1_sum[d1_cols].apply(lambda x: percent(x, df1_sum['daily_nonserious_mysj_dose1'])) 
D1symp_pct = round(D1symp_pct,2)
D1symp_pct.to_csv('Dose1_symptoms_percentage.csv')

#### bar graph of  D1 SE% group by vaxtype
D1symp_pct.plot(kind='bar')
plt.xlabel("Type of Vaccine")
plt.ylabel("Percentage (%)")
plt.title("Dose 1: Percentage of non-serious side effects reported \n for each Vaccine", fontsize=16)
plt.legend(labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash'])
plt.figure(figsize=(14,14))

#### bar graph of D1 SE% group by SE
D1symp_pct_bySE = D1symp_pct.transpose()

D1symp_pct_bySE.plot(kind='bar')
plt.xlabel("Side Effects")
plt.ylabel("Percentage (%)")
plt.title("Dose 1: Comparison of non-serious side effects reported \npost-vaccination between different vaccines", fontsize=16)
plt.legend(title = 'Vaccination Type')



### Dose 2        
D2symp_pct = df1_sum[d2_cols].apply(lambda x: percent(x, df1_sum['daily_nonserious_mysj_dose2']))
D2symp_pct = round(D2symp_pct,2)
D2symp_pct.to_csv('Dose2_symptoms_percentage.csv')

#### bar graph of  D1 SE% group by vaxtype
D2symp_pct.plot(kind='bar')
plt.xlabel("Type of Vaccine")
plt.ylabel("Percentage (%)")
plt.title("Dose 2: Percentage of non-serious side effects reported \npost-vaccination by Vaccination type", fontsize=16)
plt.legend(labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash'], loc='best', fontsize= 8)
plt.figure(figsize=(14,14))
#### bar graph of D1 SE% group by SE
D2symp_pct_bySE = D2symp_pct.transpose()

D2symp_pct_bySE.plot(kind='bar')
plt.xlabel("Side effects")
plt.ylabel("Percentage (%)")
plt.title("Dose 2: Comparison of non-serious side effects reported \npost-vaccination between different vaccines", fontsize=16)
plt.legend(title = 'Vaccination Type')



## Comparing side effects between dose 1 and dose 2 for each vaccine
# create dataframe for dose 1 and dose 2
D1_SE = df1_sum[d1_cols]
D2_SE = df1_sum[d2_cols]


## AZ SE comparison between dose
fig1, (ax1,ax2) = plt.subplots(1,2,figsize=(15,8)) #ax1,ax2 refer to your two pies

labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash']
values = D1_SE.loc['astrazeneca']
ax1.pie(values,labels = labels, autopct = '%1.1f%%') #plot first pie
ax1.set_title('Dose 1', fontsize=20)


labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash']
values = D2_SE.loc['astrazeneca']
ax2.pie(values,labels = labels, autopct = '%1.1f%%') #plot first pie
ax2.set_title('Dose 2' , fontsize=20)

fig1.suptitle('Astrazeneca Side Effects', fontsize=30)



## Pfizer SE comparison between dose
fig2, (ax1,ax2) = plt.subplots(1,2,figsize=(15,8)) #ax1,ax2 refer to your two pies

labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash']
values = D1_SE.loc['pfizer']
ax1.pie(values,labels = labels, autopct = '%1.1f%%') #plot first pie
ax1.set_title('Dose 1', fontsize=20)


labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash']
values = D2_SE.loc['pfizer']
ax2.pie(values,labels = labels, autopct = '%1.1f%%') #plot first pie
ax2.set_title('Dose 2' , fontsize=20)

fig2.suptitle('Pfizer Side Effects', fontsize=30)


## Sinovac SE comparison between dose
fig3, (ax1,ax2) = plt.subplots(1,2,figsize=(15,8)) #ax1,ax2 refer to your two pies

labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash']
values = D1_SE.loc['sinovac']
ax1.pie(values,labels = labels, autopct = '%1.1f%%') #plot first pie
ax1.set_title('Dose 1', fontsize=20)


labels = ['Site swelling', 'Site redness', 'Tiredness', 'Headache',
                     'Muscle pain' , 'Joint pain', 'Weakness', 'Fever', 
                     'Vomiting', 'Chills', 'Rash']
values = D2_SE.loc['sinovac']
ax2.pie(values,labels = labels, autopct = '%1.1f%%') #plot first pie
ax2.set_title('Dose 2' , fontsize=20)

fig3.suptitle('Sinovac Side Effects', fontsize=30)








# =============================================================================
# #analysis - D1 vs D2 among reported SE
# D1_totalSE_percent = percent(df1_sum['daily_nonserious_mysj_dose1'], df1_sum['daily_total'])
# D2_totalSE_percent = percent(df1_sum['daily_nonserious_mysj_dose2'], df1_sum['daily_total'])
# 
# 
# =============================================================================

# =============================================================================
# 
# #percentage of SE reported for vaccine administered (e.g of D1 pfizer)
# pfizer_totalSE = percent((df1_sum.at['pfizer', 'daily_total']), df1_sum.at['pfizer','pfizer1'])
# astra_totalSE = percent((df1_sum.at['astrazeneca', 'daily_total']), df1_sum.at['astrazeneca','pfizer1'])
# 
# 
# =============================================================================










df2 = pd.read_csv("Total_side_effectbyvaccine.csv")
