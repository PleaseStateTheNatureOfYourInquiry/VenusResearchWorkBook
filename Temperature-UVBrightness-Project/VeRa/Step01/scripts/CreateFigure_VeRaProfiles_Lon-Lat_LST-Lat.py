# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240419

# Create a plot of the distribution of VeRa-soundings in terms of latitude-longitude and latitude - Local Solar Time.

# Standard imports.
import os
import sys

import matplotlib.pyplot as plt 
import numpy as np

# Custom imports.
from HandyTools import HandyTools
from VeRaTools import VeRaTools

# Import settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Read the information from the two files.
VeRa_SelectedProfiles = \
 VeRaTools.readValuesFromVeRaTable ( os.path.join (VeRaWorkBookDirectory, 'Step01', 'VeRa_LocalSolarTime_OneBarLevel_PerOrbit_SelectedProfiles.dat') )

VeRa_SPoleProfiles = \
 VeRaTools.readValuesFromVeRaTable ( os.path.join (VeRaWorkBookDirectory, 'Step01', 'VeRa_LocalSolarTime_OneBarLevel_PerOrbit_SPoleProfiles.dat') )

      
# Create the Longitude - Latitude plot.  
plt.figure (1)
plt.clf ()

plt.scatter ( VeRa_SelectedProfiles [7], VeRa_SelectedProfiles [6], marker = 'x', c = 'green', label = 'VEX mission' )
plt.scatter ( VeRa_SPoleProfiles [7], VeRa_SPoleProfiles [6], marker = 'x', c = 'orange', label = 'S. Polar Dynamics Campaign' )
plt.ylim (-90,10)
plt.xlim (0,360)
plt.xlabel ('Longitude (˚)')
plt.ylabel ('Latitude (˚)')
plt.title ('VeRa Profiles Longitude vs Latitude')
plt.legend (loc = 'upper right')

plt.savefig ( os.path.join (VeRaWorkBookDirectory, 'Step01', 'plots', 'VeRaProfiles_Lon-Lat_Figure.png') )
plt.close ()


# Create the LST - Longitude plot.
plt.figure (2)
plt.clf ()

plt.scatter ( VeRa_SelectedProfiles [3], VeRa_SelectedProfiles [6], marker = 'x', c = 'green', label = 'VEX mission' )
plt.scatter ( VeRa_SPoleProfiles [3], VeRa_SPoleProfiles [6], marker = 'x', c = 'orange', label = 'S. Polar Dynamics Campaign' )
plt.ylim (-90,10)
plt.xlim (6,18)
plt.xlabel ('Local Solar Time (h)')
plt.ylabel ('Latitude (˚)')
plt.title ('VeRa Profiles Local Solar Time vs Latitude')
plt.legend (loc = 'upper left')

plt.savefig ( os.path.join (VeRaWorkBookDirectory, 'Step01', 'plots', 'VeRaProfiles_LocalSolarTime-Lat_Figure.png') )
plt.close ()