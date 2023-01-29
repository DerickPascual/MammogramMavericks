#!/usr/bin/env python
# coding: utf-8

# In[280]:


import pandas as pd

import numpy as np


# In[245]:


#reads census file and fitlers it to only women
census = pd.read_csv('sc-est2019-agesex-civ.csv')
female_census = census[census['SEX'] == 2]

#array of all the states + D.C.
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
states_weighted_pops = []
#dividing total population of women into 4 target age groups for every state
for state in states:
    state_census = female_census[female_census['NAME'] == state]
    state_4049 = state_census[(state_census['AGE'] >= 40) & (state_census['AGE'] <= 49)]
    total_state_4049 = state_4049["POPEST2019_CIV"].sum()
    state_5064 = state_census[(state_census['AGE'] >= 50) & (state_census['AGE'] <= 64)]
    total_state_5064 = state_5064["POPEST2019_CIV"].sum()
    state_6574 = state_census[(state_census['AGE'] >= 65) & (state_census['AGE'] <= 74)]
    total_state_6574 = state_4049["POPEST2019_CIV"].sum()
    state_75 = state_census[(state_census['AGE'] >= 75) & (state_census['AGE'] <= 85)]
    total_state_75 = state_75["POPEST2019_CIV"].sum()
#multipying each population age group by a statistcal weighting for every state
    age_distribution = [int(total_state_4049),int(total_state_5064),int(total_state_6574),int(total_state_75)]
    age_weights = [0.602,0.757,0.781,0.542]
    weighted_state_pop = 0
#summing weighted age group populations for each state to find total critical populations
    for i in range(len(age_distribution)):
        weighted_state_pop += age_distribution[i] * age_weights[i]
    states_weighted_pops.append(weighted_state_pop)
#creating a dictionary for integration into a dataframe
states1 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE","DC", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

data = {'State': states1, 'Critical Population': states_weighted_pops}
print(states_weighted_pops)
# Convert the dictionary to a data frame
df = pd.DataFrame(data)

# Print the data frame
print(df)
print(states_weighted_pops)


# In[281]:



critical_population = np.array([920767.487, 114800.397, 1269903.815, 542352.387, 7034553.961999999, 1000686.8869999999, 696460.6610000001, 182495.152, 111414.833, 4126265.0549999997, 1966310.4759999998, 252603.30700000003, 300490.137, 2338461.5810000002, 1206607.2610000002, 552294.3600000001, 499323.34699999995, 822894.488, 827395.61, 265963.226, 1153973.283, 1304706.368, 1846747.443, 995383.6830000001, 545360.551, 1112945.055, 186061.232, 326061.52, 546401.721, 263906.497, 1730427.1600000001, 365019.82699999993, 3656160.2600000002, 1973340.3490000002, 119486.242, 2152930.3, 682135.278, 762064.54, 2401654.779, 200421.92500000002, 959038.609, 146788.785, 1267199.514, 4980634.13, 481879.684, 118205.642, 1577975.533, 1335880.942, 342052.962, 1056509.483, 97662.37200000002])
facilities_per_state = np.array([142, 33, 171, 82, 761, 138, 114, 30, 16, 628, 277, 37, 49, 335, 179, 145, 109, 144, 145, 48, 132, 155, 271, 210, 99, 159, 47, 93, 69, 44, 247, 46, 550, 270, 48, 333, 116, 108, 343, 34, 110, 48, 192, 568, 64, 15, 205, 149, 64, 215, 30])

plt.scatter(critical_population, facilities_per_state)
plt.xlabel("Critical Population")
plt.ylabel("Facilities")
plt.plot()

slope, intercept = np.polyfit(critical_population, facilities_per_state, deg=1)
plt.plot(critical_population, (slope*critical_population)+intercept)
print("slope = " + str(slope))
print("intercept = " + str(intercept))



# In[156]:


distances = []
for i in range(len(critical_population)):
    distance = facilities_per_state[i] - (slope*critical_population[i]+intercept)
    distances.append(distance)
    
state_to_distance = {}
for i in range(len(distances)):
    state_to_distance[states[i]] = distances[i]
    neg_dict = {}
for state,value in state_to_distance.items():
    if value < 0:
        neg_dict[state] = value


sum = 0
for num in neg_dict.values():
    sum += num
print(sum)

pps = {}
for state,value in neg_dict.items():
    portion = value/sum
    pps[state]= [portion]
print(pps)

percentages = pd.DataFrame(pps)



    


# In[157]:


percentages


# In[282]:


import squarify
import matplotlib.pyplot as plt
keys, values = [], []
for key, value in pps.items():
    keys.append(key)
    values.append(value)

regular_list = [item for sublist in values for item in sublist]
print(regular_list)
        
    
    
print(keys)
print(regular_list)
import squarify
import matplotlib.pyplot as plt

# Data
values = [0.017244338881954216, 0.014796699730856696, 0.018919087659749, 0.1628750591410145, 0.018941499476253666, 0.03349027815068756, 0.04210334876072615, 0.03445002111389311, 0.026280143546200313, 0.020581065317085097, 0.05445681763547917, 0.044197762375366934, 0.003468492699833141, 0.00797304299239199, 0.04150495116658301, 0.026798853042252036, 0.0420020183426251, 0.019431262927606583, 0.03012614057245279, 0.052821208607063366, 0.09464560337761832, 0.037470044015556425, 0.044704468587089624, 0.02044593988465688, 0.062255245405372354, 0.00987077433918479, 0.01814583225044701]
labels = ['Alaska 1.7%', 'Arizona 1.4%', 'Arkansas 1.8%', 'California 1.6%', 'Colorado 1.8', 'Delaware 3.3%', 'District of Columbia 4.2%', 'Hawaii 3.4%', 'Idaho 2.6%', 'Maine 2%', 'Maryland 5.4%', 'Massachusetts 4.4%', 'Missouri 3.4%', 'Montana 0.7%', 'Nevada 4.1%', 'NH 2.6%', 'New Mexico 4.2%', 'Oregon 1.9%', 'Rhode Island 3%', 'South Carolina 5.2%', 'Texas 9.4%', 'Utah 3.7%', 'Vermont 4.4%', 'Virginia 2%', 'Washington 6.2%', 'WV 0.9%', 'Wyoming 1.8%']

# Plotting
plt.figure(figsize=(13,9))
squarify.plot(sizes=values, label=labels, alpha=.8 )
plt.axis('off')
plt.show()


# In[ ]:





# In[ ]:




