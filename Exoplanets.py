# -*- coding: utf-8 -*-
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv

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

LowerLimit=0.1
UpperLimit=10
df = df.drop(df[(df.Mass < LowerLimit) & (df.Mass > UpperLimit)].index)

Print(f"After removing datasets where the mass is too small or to big, there are now {len(df)} datasets")