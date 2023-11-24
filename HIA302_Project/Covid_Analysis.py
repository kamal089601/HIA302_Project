import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('aefi.csv')

result_2 = df[98:646].copy()

columns = result_2.columns

new_df = result_2.drop(['date', 'daily_serious_npra', 'daily_nonserious', 
         'daily_nonserious_npra', 'd1_site_pain', 'd2_site_pain'], axis=1, inplace=True)

result = result_2[result_2['vaxtype'].isin(['pfizer', 'sinovac', 'astrazeneca', 'sinopharm'])].groupby('vaxtype').sum()
grouped_data = result_2.groupby('vaxtype')['daily_total'].sum()
dose1_dose2 = result_2.groupby('vaxtype')[['daily_nonserious_mysj_dose1' , 'daily_nonserious_mysj_dose2']].sum()
side_effect_1 = result_2.groupby('vaxtype')[['d1_site_swelling', 'd1_site_redness','d1_tiredness'
                                             , 'd1_headache', 'd1_muscle_pain', 'd1_joint_pain'
                                             , 'd1_weakness', 'd1_fever', 'd1_vomiting'
                                             , 'd1_chills', 'd1_rash']].sum()
side_effect_2 = result_2.groupby('vaxtype')[['d2_site_swelling', 'd2_site_redness','d2_tiredness'
                                             , 'd2_headache', 'd2_muscle_pain', 'd2_joint_pain'
                                             , 'd2_weakness', 'd2_fever', 'd2_vomiting'
                                             , 'd2_chills', 'd2_rash']].sum()


#plotting vaxtype with the daily_total vaccine side effects
ax = grouped_data.plot(kind='bar', figsize=(10, 6))
plt.title('Daily Total Side Effect by Vaccine Type')
plt.xlabel('vaxtype')
plt.ylabel('daily_total')
plt.xticks(rotation=45)

for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    
plt.show()

#plotting vaxtype with side effect dose 1 and dose 2
ax = dose1_dose2.plot(kind='bar', stacked=True, figsize=(10, 6))

plt.title('Comparison of Vaccine Doses by Vaccine Type')
plt.xlabel('Vaccine Type')
plt.ylabel('Dose 1 and dose 2 side effect')
plt.xticks(rotation=45)

for i, (index, row) in enumerate(dose1_dose2.iterrows()):
    y_offset = 0
    for col in dose1_dose2.columns:
        value = row[col]
        if value != 0:  # Skipping zero values
            ax.annotate(value, (i, y_offset + value / 2), ha='center')
        y_offset += value
        
plt.show()

#Side effect of vaccine dose 1
# Number of vaccine types (i.e., number of groups)
num_vaccine_types = len(side_effect_1)

# Number of side effects (i.e., number of bars in each group)
num_side_effects = len(side_effect_1.columns)

# Set the positions for the vaccine types with an additional gap
bar_width = 0.1  # Width of each bar
group_width = num_side_effects * bar_width  # The total width of each group
gap_width = 0.1  # The width of the gap between groups

# Positions of the leftmost bar in each group
pos = np.arange(num_vaccine_types) * (group_width + gap_width)

# Create a figure and a set of subplots
fig, ax = plt.subplots(figsize=(15, 8))

# Plotting each side effect
for i, side_effect in enumerate(side_effect_1.columns):
    ax.bar(pos + i * bar_width, side_effect_1[side_effect], bar_width, label=side_effect)

# Set the x-ticks to be the center position for each group of bars
ax.set_xticks(pos + group_width / 2 - bar_width / 2)

# Set the x-tick labels to be the vaccine types
ax.set_xticklabels(side_effect_1.index)

# Rotate x-tick labels for better readability
plt.xticks(rotation=45)

# Adding labels and title
plt.xlabel('Vaccine Type')
plt.ylabel('Number of Reports')
plt.title('Reported Side Effects by Vaccine Type')

# Adding legend
plt.legend()

# Show the plot
plt.show()

#Side effect of vaccine dose 2
# Number of vaccine types (i.e., number of groups)
num_vaccine_types = len(side_effect_2)

# Number of side effects (i.e., number of bars in each group)
num_side_effects = len(side_effect_2.columns)

# Set the positions for the vaccine types with an additional gap
bar_width = 0.1  # Width of each bar
group_width = num_side_effects * bar_width  # The total width of each group
gap_width = 0.1  # The width of the gap between groups

# Positions of the leftmost bar in each group
pos = np.arange(num_vaccine_types) * (group_width + gap_width)

# Create a figure and a set of subplots
fig, ax = plt.subplots(figsize=(15, 8))

# Plotting each side effect
for i, side_effect in enumerate(side_effect_2.columns):
    ax.bar(pos + i * bar_width, side_effect_2[side_effect], bar_width, label=side_effect)

# Set the x-ticks to be the center position for each group of bars
ax.set_xticks(pos + group_width / 2 - bar_width / 2)

# Set the x-tick labels to be the vaccine types
ax.set_xticklabels(side_effect_2.index)

# Rotate x-tick labels for better readability
plt.xticks(rotation=45)

# Adding labels and title
plt.xlabel('Vaccine Type')
plt.ylabel('Number of Reports')
plt.title('Reported Side Effects by Vaccine Type')

# Adding legend
plt.legend()

# Show the plot
plt.show()
