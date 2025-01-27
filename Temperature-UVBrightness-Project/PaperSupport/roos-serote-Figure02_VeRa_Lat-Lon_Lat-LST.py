# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20250120

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



figure = plt.figure (1)
figure.set_figheight (6)
figure.set_figwidth (15)
figure.clf ()
figure.subplots_adjust (left = 0.05, right = 0.95)

axis1 = plt.subplot2grid ( shape = (1, 2), loc = (0, 0), colspan = 1 )
axis2 = plt.subplot2grid ( shape = (1, 2), loc = (0, 1), colspan = 1 )


# Create the Longitude - Latitude plot.  
axis1.scatter ( extension2 [:,1], extension2 [:,0], marker = 'x', c = 'purple', label = 'VEX Extension 2' )
axis1.scatter ( extension3 [:,1], extension3 [:,0], marker = 'x', c = 'black', label = 'VEX Extension 3' )
axis1.scatter ( extension4 [:,1], extension4 [:,0], marker = 'x', c = 'darkgrey', label = 'VEX Extension 4' )
axis1.scatter ( spdc [:,1], spdc [:,0], marker = 'x', c = 'red', label = 'S. Polar Dynamics Campaign' )
axis1.set_ylim (-90,10)
axis1.set_xlim (0,360)
axis1.set_xlabel ('Longitude (˚)')
axis1.set_ylabel ('Latitude (˚)')
axis1.set_title ('VeRa Profiles Longitude vs Latitude')
axis1.legend (loc = 'upper right')

# Create the LST - Longitude plot.
axis2.scatter ( extension2 [:,2], extension2 [:,0], marker = 'x', c = 'purple', label = 'VEX Extension 2' )
axis2.scatter ( extension3 [:,2], extension3 [:,0], marker = 'x', c = 'black', label = 'VEX Extension 3' )
axis2.scatter ( extension4 [:,2], extension4 [:,0], marker = 'x', c = 'darkgrey', label = 'VEX Extension 4' )
axis2.scatter ( spdc [:,2], spdc [:,0], marker = 'x', c = 'red', label = 'S. Polar Dynamics Campaign' )
axis2.set_ylim (-90,10)
axis2.set_xlim (6,18)
axis2.set_xlabel ('Local Solar Time (h)')
axis2.set_ylabel ('Latitude (˚)')
axis2.set_title ('VeRa Profiles Local Solar Time vs Latitude')

axis2.legend (loc = 'upper left')

figure.savefig ('roos-serote-Figure02a-b.png', dpi=300)

