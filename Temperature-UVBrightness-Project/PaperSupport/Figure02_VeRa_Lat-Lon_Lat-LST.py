# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241031

# Create a plot of the distribution of VeRa-soundings in terms of latitude-longitude and in terms of latitude - Local Solar Time.

# Standard imports.
import os
import sys

import matplotlib.pyplot as plt 
import numpy as np

# Custom imports.
from HandyTools import HandyTools

# Import settings.
sys.path.append ( os.path.abspath ('../') ) 
from analysisConfiguration import *


# Read the information.
profilesAndImages = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step01', 'VMCSelectedImages.dat') )
numberOfLines = len ( profilesAndImages [0][0] )
selectedOrbits = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step03', 'RadianceFactorRatiosPerOrbit.dat') )

iExtension2 = np.where ( np.logical_and ( selectedOrbits [0][0] >= 1136, selectedOrbits [0][0] <= 1583 ) ) [0]
iExtension3 = np.where ( np.logical_and ( selectedOrbits [0][0] >= 1584, selectedOrbits [0][0] <= 2451 ) ) [0]
iExtension4 = np.where ( np.logical_and ( selectedOrbits [0][0] >= 2452, selectedOrbits [0][0] <= 2774 ) ) [0]
iSPDC = np.where ( selectedOrbits [0][0] >= 2775 )[0]

extension2 = []
extension3 = []
extension4 = []
spdc = []

iLine = 0
for selectedOrbit in np.asarray (selectedOrbits [1][0]) [iExtension2]:

    while iLine < numberOfLines and profilesAndImages [1][0][iLine] != selectedOrbit:
    
        iLine += 1
        
    extension2.append ( [profilesAndImages [0][6][iLine], profilesAndImages [0][7][iLine], profilesAndImages [0][20][iLine] ] )


extension2 = np.asarray (extension2)


for selectedOrbit in  np.asarray (selectedOrbits [1][0]) [iExtension3]:

    while iLine < numberOfLines and profilesAndImages [1][0][iLine] != selectedOrbit:
    
        iLine += 1
        
    extension3.append ( [profilesAndImages [0][6][iLine], profilesAndImages [0][7][iLine], profilesAndImages [0][20][iLine] ] )


extension3 = np.asarray (extension3)

 
 
for selectedOrbit in  np.asarray (selectedOrbits [1][0]) [iExtension4]:

    while iLine < numberOfLines and profilesAndImages [1][0][iLine] != selectedOrbit:
    
        iLine += 1
        
    extension4.append ( [profilesAndImages [0][6][iLine], profilesAndImages [0][7][iLine], profilesAndImages [0][20][iLine] ] )


extension4 = np.asarray (extension4)
   
    
for selectedOrbit in  np.asarray (selectedOrbits [1][0]) [iSPDC]:

    while iLine < numberOfLines and profilesAndImages [1][0][iLine] != selectedOrbit:
    
        iLine += 1
        
    spdc.append ( [profilesAndImages [0][6][iLine], profilesAndImages [0][7][iLine], profilesAndImages [0][20][iLine] ] )


spdc = np.asarray (spdc)



# Create the Longitude - Latitude plot.  
plt.figure (1)
plt.clf ()

plt.scatter ( extension2 [:,1], extension2 [:,0], marker = 'x', c = 'purple', label = 'VEX Extension 2' )
plt.scatter ( extension3 [:,1], extension3 [:,0], marker = 'x', c = 'black', label = 'VEX Extension 3' )
plt.scatter ( extension4 [:,1], extension4 [:,0], marker = 'x', c = 'darkgrey', label = 'VEX Extension 4' )
plt.scatter ( spdc [:,1], spdc [:,0], marker = 'x', c = 'red', label = 'S. Polar Dynamics Campaign' )
plt.ylim (-90,10)
plt.xlim (0,360)
plt.xlabel ('Longitude (˚)')
plt.ylabel ('Latitude (˚)')
plt.title ('VeRa Profiles Longitude vs Latitude')

plt.legend (loc = 'upper right')


plt.savefig ('Figure02a_VeRaProfiles_Lon-Lat.png')

plt.close ()

# Create the LST - Longitude plot.
plt.figure (2)
plt.clf ()

plt.scatter ( extension2 [:,2], extension2 [:,0], marker = 'x', c = 'purple', label = 'VEX Extension 2' )
plt.scatter ( extension3 [:,2], extension3 [:,0], marker = 'x', c = 'black', label = 'VEX Extension 3' )
plt.scatter ( extension4 [:,2], extension4 [:,0], marker = 'x', c = 'darkgrey', label = 'VEX Extension 4' )
plt.scatter ( spdc [:,2], spdc [:,0], marker = 'x', c = 'red', label = 'S. Polar Dynamics Campaign' )
plt.ylim (-90,10)
plt.xlim (6,18)
plt.xlabel ('Local Solar Time (h)')
plt.ylabel ('Latitude (˚)')
plt.title ('VeRa Profiles Local Solar Time vs Latitude')

plt.legend (loc = 'upper left')

plt.savefig ('Figure02b_VeRaProfiles_LocalSolarTime-Lat.png')

plt.close ()