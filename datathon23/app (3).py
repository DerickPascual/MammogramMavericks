#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np
import geopandas as gp
import matplotlib.pyplot as plt
import plotly.express as px


# In[37]:


facility_df = pd.read_csv('beginner.csv')


# In[38]:


facility_df = facility_df.drop(columns=['Facility Name', 'Address 1', 'Address 2', 'Address 3', 'City'])


# In[39]:


# for loop that runs four times to shift all data so that state val is in state
for i in range(4):
    mask = facility_df['Unnamed: 9'].notnull()
    facility_df.loc[mask, :] = facility_df.loc[mask, :].shift(periods=-1, axis=1)


# In[40]:


facility_df = facility_df.drop(columns=['Zip Code', 'Phone', 'Fax', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'])


# In[41]:


state_abbreviations = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 
    'DC'
]


# In[42]:


mask = facility_df['State'].isin(state_abbreviations)


# In[43]:


facility_df=facility_df[mask]


# In[44]:


state_counts = facility_df['State'].value_counts()


# In[45]:


state_counts = pd.DataFrame(state_counts).reset_index()


# In[46]:


state_counts.columns = ['State', 'Facilities']


# In[47]:


# state_counts['State'] = state_counts['State'].map(state_map)


# In[48]:


# state_counts = state_counts.sort_values(by='State')


# In[49]:


# facility_counts = state_counts['Facilities'].values.tolist()


# In[50]:


# state_counts


# In[51]:


# state_counts = state_counts.rename(columns={'State'})


# In[52]:


# us = gpd.read_file('./us_states')


# In[53]:


# merged = us.merge(state_counts, on='NAME')


# In[54]:


# us_map = merged.plot(column='Facilities', cmap='Blues')


# In[55]:


census = pd.read_csv('sc-est2019-agesex-civ.csv')
female_census = census[census['SEX'] == 2]
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware','District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
states_weighted_pops = []
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

    age_distribution = [int(total_state_4049),int(total_state_5064),int(total_state_6574),int(total_state_75)]
    age_weights = [0.602,0.757,0.781,0.542]
    weighted_state_pop = 0
    for i in range(len(age_distribution)):
        weighted_state_pop += age_distribution[i] * age_weights[i]
    states_weighted_pops.append(weighted_state_pop)
states1 = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE","DC", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

data = {'State': states1, 'Critical Population': states_weighted_pops}

# Convert the dictionary to a data frame
population_df = pd.DataFrame(data)

# Print the data frame
print(population_df)


# In[56]:


state_df = state_counts.merge(population_df)


# In[57]:


state_df['At Risk Population/Facility'] = state_df['Critical Population'] / state_df['Facilities']


# In[58]:


state_df


# In[59]:


fig = px.choropleth(state_df,
                    locations='State',
                    locationmode='USA-states',
                    color='At Risk Population/Facility',
                    scope='usa',
                    color_continuous_scale=['#00FF00', '#FF0000'],
                    range_color=[2000, 10000],
                    title='Number of Facilities')

fig.show()


# In[60]:


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
distances = []
for i in range(len(critical_population)):
    distance = facilities_per_state[i] - (slope*critical_population[i]+intercept)
    distances.append(distance)
    
print(len(distances))
    
state_to_distance = {}
for i in range(len(distances)):
    state_to_distance[states[i]] = distances[i]
    
neg_dict = {}
for state,value in state_to_distance.items():
    if value < 0:
        neg_dict[state] = value
    else: 
        neg_dict[state] = 0

print(len(state_to_distance.values()))
print(len(neg_dict.values()))

sum = 0
for num in neg_dict.values():
    sum += num
print(sum)

pps = {}
for state,value in neg_dict.items():
    portion = value/sum
    pps[state]= [portion]
print(pps)

print(len(pps))
percentages = pd.DataFrame(pps)


# In[61]:


facilities = 2000

percentages.loc[0] = percentages.loc[0] * facilities

percentages = percentages.T

percentages = percentages.reset_index()



# In[62]:


percentages.columns = ['State', 'Additional Facilities']


# In[63]:


state_map = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
             'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 
             'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 
             'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 
             'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 
             'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 
             'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 
             'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 
             'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 
             'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 
             'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 
             'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 
             'WI': 'Wisconsin', 'WY': 'Wyoming'}


# In[64]:


state_df['State'] = state_df['State'].map(state_map)


# In[65]:


facilities_w_additional = state_df.merge(percentages, on="State")


# In[66]:


facilities_w_additional['Facilities plus Additional Facilities'] = facilities_w_additional['Facilities'] + facilities_w_additional['Additional Facilities']


# In[67]:


facilities_w_additional['At Risk Population/New Facilities'] = facilities_w_additional['Critical Population'] / facilities_w_additional['Facilities plus Additional Facilities']


# In[68]:


states = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}


# In[69]:


facilities_w_additional['State'] = facilities_w_additional['State'].map(states)


# In[70]:


fig = px.choropleth(facilities_w_additional,
                    locations='State',
                    locationmode='USA-states',
                    color='At Risk Population/New Facilities',
                    scope='usa',
                    color_continuous_scale=['#00FF00', '#FF0000'],
                    range_color=[2000, 10000],
                    title='Number of Facilities')

fig.show()


# In[ ]:





# In[ ]:




