
#Import relevant packages
import numpy as np 
from random import random
from math import sqrt,exp
import matplotlib.pyplot as plt

#Calibrated threshold probability
soil_probability = 0.02    # 2%

#num_pores1 x num_pores2 matrix
num_pores1 = 20          
num_pores2 = 20

#Depth of Oak Ridges Moraine
layers = 155   # metres

#Repititions of saoking the top layer with rainwater. Soaked = all pores have water
downpour_time = 60 #minutes

#The surface layer that's bombarded with rainwater (Matrix of ones)
soaked_lattice = np.ones([num_pores1,num_pores2])

def percolate(probability, lattice):
    """This function analyzes a lattice and percolates it. Each element has an 
    associated random number between 1 and 0. If the number is greater
    than the threshold probability, the fluid can pass through the pore"""
    lattice2 = np.ones([num_pores1,num_pores2])
    for i in range(num_pores1):
        for j in range(num_pores2):
            if probability < random():
                lattice2[i,j] = 0*lattice[i,j]
            else: 
                lattice2[i,j] = 1*lattice[i,j]          
    return lattice2

#each element in lattice_layersplus represents an array of layers after a downpour
#the total number of arrays represents the total number of downpour
#first downpour = first array, eighth downpour = eighth array

lattice_layersplus = [[] for _ in range(downpour_time)]

#Array of how much water in aquifer per min
aquifer = []

#Main loop
for l in range(downpour_time):
    #This is taking downpour l and percolating the surface soaked lattice 
    perc_lattice = percolate(soil_probability,soaked_lattice)
    lattice_layersplus[l].append(perc_lattice)
    
    #for determining lattice right below the surface
    if l == 0:
        lattice = soaked_lattice - perc_lattice
    else:
        lattice = soaked_lattice - perc_lattice + lattice_layersplus[l-1][1]
    
    #Next loop to get rid of stacking of fluid at pores
    for i in range(num_pores1):
        for j in range(num_pores2):
            if lattice[i,j] >= 2:
                lattice[i,j] = 1
            else:
                pass
        
    for w in range(layers):
        #Create a condition that saves the last layer before the aquifer
        if w == layers - 1:
            aquifer_check = lattice    
        else:
            pass
        #Percolate a layer
        perc_lattice = percolate(soil_probability, lattice)
        lattice_layersplus[l].append(perc_lattice)
#        plt.imshow(perc_lattice)
#        plt.show() 

        
        #Determine how much liquid made it to aquifer
        if w == layers - 1:
            aquifer_lattice = aquifer_check - perc_lattice
            aquifer_amount = np.sum(aquifer_lattice)
            aquifer.append(aquifer_amount)
        else: 
            pass
        
        #determine the composition of next layer to be percolated
        if l == 0:
            lattice = lattice - perc_lattice
        else:
            lattice = lattice - perc_lattice + lattice_layersplus[l-1][w]
        
        #Next loop to get rid of stacking of fluid at pores
        for i in range(num_pores1):
            for j in range(num_pores2):
                if lattice[i,j] >= 2:
                    lattice[i,j] = 1
                else:
                    pass

#Settting up array for plot representing percentage of total water in aquifer
ratioplot = []
Time = np.linspace(0, downpour_time, downpour_time+1)
for n in range(len(aquifer)-1):
    Ratio = np.sum(aquifer[:n+1])/(num_pores1*num_pores2*Time[n+1])
    ratioplot.append(Ratio)
 
     
#plotting properties
plt.plot(Time[:-2], ratioplot, label = 'o')
plt.title('Percolation in the Oak Ridges Moraine with Constant Rainfall')
plt.xlabel('Minutes')
plt.ylabel('Completely percolated water: total water' )
plt.show()
    