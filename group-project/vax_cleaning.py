#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

filepath = '/Users/azfar/Documents/GitHub/group-project/Data Files'

# Import original datasets into specified DataFrames
df_t_vax = pd.read_csv(filepath+'/vax_malaysia.csv')
df_aefi = pd.read_csv(filepath+'/aefi.csv')

# Truncate unnecessary columns
df_t_vax.drop(columns=['cansino','cansino3','cansino4','pending1','pending2',
                       'pending3','pending4'], inplace=True)
df_t_vax.drop(columns=['daily_partial','daily_full','daily_booster',
                       'daily_booster2'], inplace=True)
df_t_vax.drop(df_t_vax.columns[[2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,
                                20,21,22]], axis=1, inplace=True)

# Consolidate the different vaccine doses into single columns
cols = ['pfizer1','pfizer2','pfizer3','pfizer4']
df_t_vax['pfizer'] = df_t_vax[cols].sum(1)
df_t_vax.drop(cols, axis=1, inplace=True)

cols1 = ['sinovac1','sinovac2','sinovac3','sinovac4']
df_t_vax['sinovac'] = df_t_vax[cols1].sum(1)
df_t_vax.drop(cols1, axis=1, inplace=True)

cols2 = ['astra1','astra2','astra3','astra4']
df_t_vax['astra'] = df_t_vax[cols2].sum(1)
df_t_vax.drop(cols2, axis=1, inplace=True)

cols3 = ['sinopharm1','sinopharm2','sinopharm3','sinopharm4']
df_t_vax['sinopharm'] = df_t_vax[cols3].sum(1)
df_t_vax.drop(cols3, axis=1, inplace=True)

# Save the edited DataFrame into a new .csv file
df_t_vax.to_csv(filepath+'/totalvax.csv', index=False)

total_pfizer = df_t_vax['pfizer'].sum()
total_astra = df_t_vax['astra'].sum()
total_sinovac = df_t_vax['sinovac'].sum()
total_sinopharm = df_t_vax['sinopharm'].sum()

df_doses = pd.DataFrame({
    'pfizer' : ['Pfizer', total_pfizer],
    'astrazeneca' : ['Astra', total_astra],
    'sinovac' : ['Sinovac', total_sinovac],
    'sinopharm' : ['Sinopharm', total_sinopharm]},
    index=['vaxtype','total_doses'])

# Cleaning AEFI dataset
vaxgroups = df_aefi.groupby('vaxtype')
aefi_p = vaxgroups.get_group('pfizer').drop(columns=['date','vaxtype']).sum()
aefi_a = vaxgroups.get_group('astrazeneca').drop(columns=['date','vaxtype']).sum()
aefi_sv = vaxgroups.get_group('sinovac').drop(columns=['date','vaxtype']).sum()
aefi_sp = vaxgroups.get_group('sinopharm').drop(columns=['date','vaxtype']).sum()

# New DataFrame for cummulative sum of reported AEFI, sorted by brand
df_aefi_total = pd.DataFrame({
    'pfizer' : aefi_p,
    'astrazeneca' : aefi_a,
    'sinovac' : aefi_sv,
    'sinopharm' : aefi_sp
    })

df_clean = pd.concat([df_doses, df_aefi_total])
df_clean = df_clean.T
df_clean.to_csv(filepath+'/for_analysis.csv', index=False)

# ANALYTICS, part 1
serious_pfizer = df_clean['pfizer'].loc['daily_serious_npra'] / df_clean['pfizer'].loc['total_doses']
serious_astra = df_clean['astrazeneca'].loc['daily_serious_npra'] / df_clean['astrazeneca'].loc['total_doses']
serious_sv = df_clean['sinovac'].loc['daily_serious_npra'] / df_clean['sinovac'].loc['total_doses']
serious_sp = df_clean['sinopharm'].loc['daily_serious_npra'] / df_clean['sinopharm'].loc['total_doses']

