#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[3]:


#data
critical_population = np.array([863277.547, 110597.72899999999, 1188718.7189999998, 506535.943, 6616216.14, 949275.477, 645773.905, 170720.744, 104511.379, 3804495.915, 1872088.112, 231001.35500000004, 283689.763, 2183570.447, 1128802.077, 507659.03400000004, 462694.98699999996, 772861.926, 777435.676, 246376.43, 1085123.5650000002, 1213975.026, 1723292.851, 927031.5210000001, 511995.03099999996, 1035413.0389999999, 173410.41, 301981.002, 520335.315, 246846.50499999998, 1613718.8420000002, 341108.41299999994, 3393050.154, 1856906.283, 109216.426, 2001936.146, 638542.7600000001, 714682.9, 2211289.745, 184976.55100000004, 902795.2690000001, 135221.963, 1192018.6940000001, 4738655.52, 459993.72400000005, 110030.114, 1486606.799, 1259734.278, 317571.364, 983161.165, 91537.77200000001])
facilities_per_state = np.array([142, 33, 171, 82, 761, 138, 114, 30, 16, 628, 277, 37, 49, 335, 179, 145, 109, 144, 145, 48, 132, 155, 271, 210, 99, 159, 47, 93, 69, 44, 247, 46, 550, 270, 48, 333, 116, 108, 343, 34, 110, 48, 192, 568, 64, 15, 205, 149, 64, 215, 30])

#formatting table
plt.scatter(critical_population, facilities_per_state)
plt.xlabel("At-Risk Population")
plt.ylabel("Facilities")
plt.xlim(0, 7000000)
plt.ylim(0, 1000)
plt.ticklabel_format(style='plain')
plt.title("At-Risk Population versus Facilities")
plt.plot()


#making and plotting line of best fit
slope, intercept = np.polyfit(critical_population, facilities_per_state, deg=1)
plt.plot(critical_population, (slope*critical_population)+intercept)
print("slope = " + str(slope))
print("intercept = " + str(intercept))


# In[ ]:




