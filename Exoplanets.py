# -*- coding: utf-8 -*-
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import matplotlib.pyplot as plt

dataset = 'all_exoplanets_2021.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(dataset)

# Access data in the DataFrame using column names or indexing
#print(df['column_name'])
print("All possible available dats is \n" + f"{df.iloc[0]} \n")  # Access first row

#Relevant data
#Planet Name: indentification
#Num stars: ==1 
#Mass: Enough to maintain atmosphere, not too high though
#Eccentricity: Not too high as it will lead to uneven temperature
#Equilibrium Temperature, can only be calculated when distance from nearby star is known
#Does not take albedo or green house effect into account
#Distance: From Earth in parsec


Dropped_Columns=["Num Planets", "Discovery Method", "Orbital Period Days","Planet Host", "Discovery Year", "Discovery Facility", "Orbit Semi-Major Axis", "Insolation Flux", "Spectral Type", "Stellar Effective Temperature", "Stellar Radius", "Stellar Mass", "Stellar Metallicity", "Stellar Metallicity Ratio","Stellar Surface Gravity", "Gaia Magnitude"]

df=df.drop(columns=Dropped_Columns)

print("I have only kept the relvant data, that is \n" + f"{df.iloc[0]} \n")

print(f"As there is {len(df)} datasets we need to look into the most relevant ones")

df = df[df['Equilibrium Temperature'].notna()]

print(f"After removing datasets where the equilibrium temperature is unknown we have {len(df)} datasets")


df = df[df['Mass'].notna()]

print(f"I remove datasets where the mass of the planet is missing, there are now {len(df)} datasets")

LowerLimit=0.07 #Minimum mass to maintain athmosphere for about 4.5billion years
UpperLimit=10

df = df[(df['Mass'] >= LowerLimit) & (df['Mass'] <= UpperLimit)]

print(f"After removing datasets where the mass is too small or to big, there are now {len(df)} datasets")

df = df[(df['Num Stars'] == 1)]

print(f"After removing datasets with more than one star, there are now {len(df)} datasets")

MaxEccentricity=0.4 #Dont allow high eccentricity
df = df[(df['Eccentricity'] < MaxEccentricity)]

print(f"Only keeping datasets with eccentricity < {MaxEccentricity}, there are now {len(df)} datasets")


def SurfaceTemp(T):
    A=0.8 #Assumption of icy world with really high albedo
    Gmin=(1-A)**0.25
    print(Gmin)
    Gmax=2 #Assumption of a moderate athmosphere
    return Gmin*T, Gmax*T


def WaterPossible(T):
    [Tmin, Tmax]=SurfaceTemp(T)
    if Tmin < (273+60) and Tmax > 273:
        return True
    else:
        return False
    

df = df[df['Equilibrium Temperature'].apply(WaterPossible)]


[df['Tmin'],df['Tmax']] = SurfaceTemp(df['Equilibrium Temperature'])

df=df.drop(columns=['Num Stars', 'No.','Eccentricity'])


plt.plot(df["Planet Name"], df["Equilibrium Temperature"]-273, marker='o',color='g', label="Equilibrium Temperature")
plt.plot(df["Planet Name"], df["Tmin"]-273, marker='o', color='b', label="Minimum Temperature")
plt.plot(df["Planet Name"], df["Tmax"]-273, marker='o', color='r', label="Maximum Temperaure")

# Add titles and labels
plt.title("Possible Temperature Range for Each Planet")
plt.xlabel("Planet")
plt.ylabel("Temperature (C)")
plt.legend(title="Temperature Type")
plt.xticks(size=8, rotation=70)
plt.yticks(size=8)

#plt.fill_between(x, y1, y2, color='lightblue', alpha=0.5)



print(df)
print(len(df))
print(df)

