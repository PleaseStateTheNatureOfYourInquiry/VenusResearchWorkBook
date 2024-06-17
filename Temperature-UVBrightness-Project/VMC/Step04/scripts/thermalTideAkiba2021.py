# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v202400610

# The thermal tide table file is created by the script  /Users/maarten/Science/Venus/Temperature-UV_Analysis_2024/Analysis/VMC/Step04/scripts/createTable_ThermalTide_Akiba2021_Figure5.py 
#  and has the same content as the CSV file from the Zenodo repository at doi.org/10.5281/zenodo.5159027 (figure5), as part of the article by Akiba, M. et al. (2021). 
#   "Thermal tides in the upper cloud layer of Venus as deduced from the emission angle dependence of the brightness temperature by Akatsuki/ LIR."
#   Journal of Geophysical Research: Planets, 126, e2020JE006808. doi.org/10.1029/2020JE006808Abika

# The thermal tide amplitude is calculated by linear interpolation first in latitude and next in Local Solar Time. 

# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt


# Custom imports.
from HandyTools import HandyTools


thermalTidePerLST = HandyTools.readTable ('../temp_devi_contour_lt_to_lat_distributions_at_constant_altitude_each_value_whole_wider_period.dat')

thermalTideLatitude = thermalTidePerLST [0][0]

# plt.figure (1)
# plt.clf ()
# 
# 
# for iLST in range (24):
# 
#     plt.plot ( latitude, thermalTidePerLST [0][iLST +1] )
# 

selectedImages = HandyTools.readTable ('..Step01/VMCSelectedImages.dat')
imageIDSelectedImages = selectedImages [1][1]
latitudeSelectedImages = selectedImages [0][6]
LSTSelectedImages = selectedImages [0][-1]


# Use the absolute path to write it properly in the header of the table file to be created.
tableFileName = os.path.abspath ('../ThermalTideCorrection.dat')
fileOpen = open (tableFileName, 'w')

print (' ', file = fileOpen)
print (' File: {}'.format (tableFileName), file = fileOpen)
print (' Created at {}'.format ( HandyTools.getDateAndTimeString () ), file = fileOpen)

print (' ', file = fileOpen)
print (' Figure 5a from Akiba, M. et al. (2021). "Thermal tides in the upper cloud layer of Venus as deduced from the emission angle dependence of the brightness temperature by Akatsuki/ LIR."', file = fileOpen)
print ('  Journal of Geophysical Research: Planets, 126, e2020JE006808. https:// doi.org/10.1029/2020JE006808', file = fileOpen)
print (' Zenodo repository at doi.org/10.5281/zenodo.5159027 (figure5)', file = fileOpen)

print (' ', file = fileOpen)
print (' LST = Local Solar Time ', file = fileOpen)


print (' ', file = fileOpen)
print (' The thermal tide file corresponding to Figure 5a is  temp_devi_contour_lt_to_lat_distributions_at_constant_altitude_each_value_whole_wider_period.dat  and ', file = fileOpen)
print ('  has been created using the script  /Users/maarten/Science/Venus/Temperature-UV_Analysis_2024/Analysis/VMC/Step04/scripts/createTable_ThermalTide_Akiba2021_Figure5.py', file = fileOpen)

print (' ', file = fileOpen)
print (' The thermal tide amplitude (dT_tide) is calculated by linear interpolation first in latitude and next in Local Solar Time. ', file = fileOpen)

print (' ', file = fileOpen)
print (' Orbit      lat     Local Solar Time   T_VeRa   dT_VeRa    dT_tide ', file = fileOpen)
print ('            (˚)            (h)           (K)      (K)        (K) ', file = fileOpen)
print ('C_END', file = fileOpen)

currentOrbit = ''
for iSelectedImage in range ( len ( selectedImages [0][0] ) ):

    if selectedImages [1][0][iSelectedImage] != currentOrbit:
        
        currentOrbit = selectedImages [1][0][iSelectedImage]
        
        iLSTSelectedImage = int ( LSTSelectedImages [iSelectedImage] ) + 1
    
        if latitudeSelectedImages [iSelectedImage] <= -62.5:
        
            iThermalTideLatitude = 0
            thermalTideInterpolatedLatitudeLSTLowerBoundary = thermalTidePerLST [0][iLSTSelectedImage][iThermalTideLatitude]
            thermalTideInterpolatedLatitudeLSTUpperBoundary = thermalTidePerLST [0][iLSTSelectedImage + 1][iThermalTideLatitude]
    
            
        elif latitudeSelectedImages [iSelectedImage] >= 62.5:
        
            iThermalTideLatitude = -1
            thermalTideInterpolatedLatitudeLSTLowerBoundary = thermalTidePerLST [0][iLSTSelectedImage][iThermalTideLatitude]
            thermalTideInterpolatedLatitudeLSTUpperBoundary = thermalTidePerLST [0][iLSTSelectedImage + 1][iThermalTideLatitude]
            
    
        else:
        
            iThermalTideLatitude = np.where ( np.asarray (thermalTideLatitude) >= np.asarray ( latitudeSelectedImages [iSelectedImage] ) )[0][0]
        
            
    
            thermalTideInterpolatedLatitudeLSTLowerBoundary = \
             thermalTidePerLST [0][iLSTSelectedImage][iThermalTideLatitude - 1] + \
             ( latitudeSelectedImages [iSelectedImage] - thermalTideLatitude [iThermalTideLatitude - 1] ) * \
             ( thermalTidePerLST [0][iLSTSelectedImage][iThermalTideLatitude] - thermalTidePerLST [0][iLSTSelectedImage][iThermalTideLatitude - 1]  ) / \
             ( thermalTideLatitude [iThermalTideLatitude] - thermalTideLatitude [iThermalTideLatitude - 1] )
        
            thermalTideInterpolatedLatitudeLSTUpperBoundary = \
             thermalTidePerLST [0][iLSTSelectedImage + 1][iThermalTideLatitude - 1] + \
             ( latitudeSelectedImages [iSelectedImage] - thermalTideLatitude [iThermalTideLatitude - 1] ) * \
             ( thermalTidePerLST [0][iLSTSelectedImage + 1][iThermalTideLatitude] - thermalTidePerLST [0][iLSTSelectedImage + 1][iThermalTideLatitude - 1]  ) / \
             ( thermalTideLatitude [iThermalTideLatitude] - thermalTideLatitude [iThermalTideLatitude - 1] )
    
        thermalTideInterpolated = thermalTideInterpolatedLatitudeLSTLowerBoundary + ( LSTSelectedImages [iSelectedImage] - (iLSTSelectedImage - 1) ) * \
         ( thermalTideInterpolatedLatitudeLSTUpperBoundary - thermalTideInterpolatedLatitudeLSTLowerBoundary ) / 1

    
        print (' {}     {:6.2f}         {:6.3f}        {:6.2f}   {:6.3f}   {:9.6f}'.
         format ( currentOrbit, 
                  latitudeSelectedImages [iSelectedImage], 
                  LSTSelectedImages [iSelectedImage],
                  selectedImages [0][-3][iSelectedImage], selectedImages [0][-2][iSelectedImage],
                  thermalTideInterpolated ), file = fileOpen )



fileOpen.close ()


