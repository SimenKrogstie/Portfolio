#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 21:16:59 2022

__author__ = "Simen Roko Krogstie"
__email__ = "simen.roko.krogstie@nmbu.no"
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Del 1
dataFil = "meteodata_aas_2012.csv"
temp_data = pd.read_table(open(dataFil), skiprows = 1, sep = ';')

# Del 2
df = pd.DataFrame(temp_data)
T_avg = df["T_avg"]
a = T_avg.to_numpy()

plt.plot(a)

# Del 3
def temp_year(day):
    A = 11
    Tavg = 5.91
    offset = 255
    omega = 2 * np.pi /365
    return Tavg + A * np.sin(omega*(day + offset))

day = np.linspace(0, 366, 366)
y = temp_year(day)

plt.plot(day, y, color='orange')
plt.xlabel('day of year')
plt.ylabel('temp [deg C]')
plt.legend(['Daily average measurment','Tavg + A * sin*(omega*(day + offset))'])
plt.title('Temperature readings for 2012')

#plt.savefig('graf_del4.png')
# Del 4
# a) 
Tavg_ny = np.mean(a) 
print(Tavg_ny)
# Estimert årsgjennomsnitt er 5.91
 
# b) 
# Jeg prøvde meg frem med ulike verdier for amplituden, og fant ut at A = 11
# passet best.


