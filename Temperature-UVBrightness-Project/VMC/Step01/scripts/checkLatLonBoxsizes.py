# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20250323

# 

# Standard imports.
import os
import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt


# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools

from VeRaTools import VeRaTools
from VMCTools import VMCTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


tableFileNameAndPath = os.path.join (VMCWorkBookDirectory, 'Step01', 'VMCSelectedImages_orbits_later_than_1188.dat')
tableContent = HandyTools.readTable (tableFileNameAndPath)

latitudeCentres = tableContent [0][8]
latitudeRanges = np.abs ( tableContent [0][10] - tableContent [0][9] )
latitudeRangesInKm = radiusOfVenus * latitudeRanges * np.pi / 180

longitudeCentres = tableContent [0][11]
longitudeRanges = np.abs ( tableContent [0][13] - tableContent [0][12] )
iLongitudeRangesReduce = np.where (longitudeRanges >= 180)[0]
longitudeRanges [iLongitudeRangesReduce] = np.abs ( longitudeRanges [iLongitudeRangesReduce] - 360 )
longitudeRangesInKm = radiusOfVenus * np.cos ( latitudeCentres * np.pi / 180 ) * longitudeRanges * np.pi / 180

# plt.figure (1)
# plt.clf ()
# plt.scatter (latitudeCentres, latitudeRangesInKm)
# plt.xlabel ('Latitude box centre (˚)')
# plt.ylabel ('Latitude range (km)')
# 
# 
# 
# plt.figure (2)
# plt.clf ()
# plt.scatter (latitudeCentres, longitudeRangesInKm)
# plt.xlabel ('Latitude box centre (˚)')
# plt.ylabel ('Longitude range (km)')


plt.figure (3)
plt.clf ()
plt.scatter (latitudeRangesInKm, longitudeRangesInKm, s = 10)
plt.xlabel ('Latitude range of box (km)')
plt.ylabel ('Longitude range of box (km)')
plt.title ('Latitude - longitude box sizes of selected VMC images')
plt.text ( 20,1700, 'average lon-range = {:4.0f}km'.format ( np.average (longitudeRangesInKm) ) )
plt.text ( 20,1600, 'average lat-range = {:4.0f}km'.format (  np.average (latitudeRangesInKm)  ) )

plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step01/plots', 'latitudeLongitudeBoxSizes.png') )


plt.clf ()
plt.scatter (latitudeRangesInKm, longitudeRangesInKm, s = 10)
plt.xlabel ('Latitude range of box (km)')
plt.ylabel ('Longitude range of box (km)')
plt.title ('Latitude - longitude box sizes of selected VMC images')
plt.xlim (0,100)
plt.ylim (0,150)
plt.text ( 5,130, 'minimum lon-range = {:2.0f}km'.format ( np.min (longitudeRangesInKm) ) )
plt.text ( 5,122, 'minimum lat-range = {:2.0f}km'.format (  np.min (latitudeRangesInKm)  ) )



plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step01/plots', 'latitudeLongitudeBoxSizes-0-100km.png') )














