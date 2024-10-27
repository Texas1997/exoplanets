# -*- coding: utf-8 -*-
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import matplotlib.pyplot as plt

dataset = 'all_exoplanets_2021.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(dataset)

Dropped_Columns=["Num Planets", "Discovery Method", "Orbital Period Days","Planet Host", "Discovery Year", "Discovery Facility", "Orbit Semi-Major Axis", "Insolation Flux", "Spectral Type", "Stellar Effective Temperature", "Stellar Radius", "Stellar Mass", "Stellar Metallicity", "Stellar Metallicity Ratio","Stellar Surface Gravity", "Gaia Magnitude"]
df=df.drop(columns=Dropped_Columns)
df = df[df['Equilibrium Temperature'].notna()] #Removing datasets where the equilibrium temperature is unknown
df = df[df['Mass'].notna()] #Removing datasets where the mass is unknown


LowerLimit=0.07 #Minimum mass to maintain athmosphere for about 4.5billion years
UpperLimit=5 #Likely too be rocky and not a thick athmosphere like Venus
MaxEccentricity=0.4 #Dont allow high eccentricity
df = df[(df['Mass'] >= LowerLimit) & (df['Mass'] <= UpperLimit)]
df = df[(df['Eccentricity'] < MaxEccentricity)]


def SurfaceTemp(T): #Giving upper and lower limits for surface temperature based on equilibrium temperature
    A=0.8 #Assumption of icy world with really high albedo
    Gmin=(1-A)**0.25
    Gmax=2 #Assumption of a moderate athmosphere
    return Gmin*T, Gmax*T


def WaterPossible(T): #Returns true if it is at all possible to have a temperature between 0 and 60C somewehere on the planet
    [Tmin, Tmax]=SurfaceTemp(T)
    if Tmin < (273+60) and Tmax > 273:
        return True
    else:
        return False
    

df = df[df['Equilibrium Temperature'].apply(WaterPossible)]
[df['Tmin'],df['Tmax']] = SurfaceTemp(df['Equilibrium Temperature'])
df=df.drop(columns=['No.','Eccentricity'])

#Plot possible temperature range for each planet that could possibly be suitable for life
plt.plot(df["Planet Name"], df["Equilibrium Temperature"]-273, marker='o',color='g', label="Equilibrium Temperature")
plt.plot(df["Planet Name"], df["Tmin"]-273, marker='o', color='b', label="Minimum Temperature")
plt.plot(df["Planet Name"], df["Tmax"]-273, marker='o', color='r', label="Maximum Temperaure")
plt.fill_between(df["Planet Name"], df["Equilibrium Temperature"]-273, df["Tmin"]-273, color='lightblue', alpha=0.5)
plt.fill_between(df["Planet Name"], df["Equilibrium Temperature"]-273, df["Tmax"]-273, color='pink', alpha=0.5)

# Add titles and labels
plt.title("Possible Temperature Range for Each Planet")
plt.xlabel("Planet")
plt.ylabel("Temperature (C)")
plt.legend(title="Temperature Type")
plt.xticks(size=8, rotation=70)
plt.yticks(size=8)
plt.grid()


#Plot the relevant table
df=df.drop(columns=["Tmin", "Tmax"])
print(df)


