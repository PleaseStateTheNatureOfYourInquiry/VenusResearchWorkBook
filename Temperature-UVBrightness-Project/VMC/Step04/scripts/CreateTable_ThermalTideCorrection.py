# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241111

# The thermal tide table file is created by the script  /Users/maarten/Science/Venus/Temperature-UV_Analysis_2024/Analysis/VMC/Step04/scripts/createTable_ThermalTide_Akiba2021_Figure5.py 
#  and has the same content as the CSV file from the Zenodo repository at doi.org/10.5281/zenodo.5159027 (figure5), as part of the article by Akiba, M. et al. (2021). 
#   "Thermal tides in the upper cloud layer of Venus as deduced from the emission angle dependence of the brightness temperature by Akatsuki/ LIR."
#   Journal of Geophysical Research: Planets, 126, e2020JE006808. doi.org/10.1029/2020JE006808Abika

# The thermal tide amplitude is calculated by linear interpolation first in latitude and next in Local Solar Time. 

# Note that this thermal tide is for 69km altitude.
# The VeRa temperature and corresponding uncertainty at 69km altitude is exported in the table as well for comparison.

# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt


# Custom imports.
from HandyTools import HandyTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


thermalTidePerLST = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step04', 'temp_devi_contour_lt_to_lat_distributions_at_constant_altitude_each_value_whole_wider_period.dat') ) 
thermalTideLatitude = thermalTidePerLST [0][0]

# plt.figure (1)
# plt.clf ()
# 
# 
# for iLST in range (24):
# 
#     plt.plot ( latitude, thermalTidePerLST [0][iLST +1] )
# 

selectedImages = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step01', 'VMCSelectedImages.dat') )
imageIDSelectedImages = selectedImages [1][1]
latitudeSelectedImages = selectedImages [0][6]
LSTSelectedImages = selectedImages [0][-3]

# Read the NumPy arrays containing all the necessary VeRa profiles information.
VeRaSelectedProfiles = np.load ( os.path.join (VeRaWorkBookDirectory, 'Step02','VeRaSelectedProfiles.profiles'), allow_pickle = True ).tolist ()
VeRaSPoleProfiles = np.load ( os.path.join (VeRaWorkBookDirectory, 'Step02', 'VeRaSouthPolarDynamicsCampaignProfiles.profiles'), allow_pickle = True ).tolist ()



# Use the absolute path to write it properly in the header of the table file to be created.
tableFileName = os.path.abspath ( os.path.join (VMCWorkBookDirectory, 'Step04', 'ThermalTideCorrection.dat') )
fileOpen = open (tableFileName, 'w')

headerLines = [
'',
' Figure 5a from Akiba, M. et al. (2021). "Thermal tides in the upper cloud layer of Venus as deduced from the emission angle dependence of the brightness temperature by Akatsuki/ LIR."',
'  Journal of Geophysical Research: Planets, 126, e2020JE006808. https:// doi.org/10.1029/2020JE006808',
' Zenodo repository at doi.org/10.5281/zenodo.5159027 (figure5)',
'',
' LST = Local Solar Time ',
' T_VeRa = VeRa temperature at 69km altitude',
' dT_VeRa = uncertainty in T_VeRa',
' dT_tide = thermal tide amplitude',
'',
' The thermal tide file corresponding to Figure 5a is  temp_devi_contour_lt_to_lat_distributions_at_constant_altitude_each_value_whole_wider_period.dat  and ',
'  has been created using the script  /Users/maarten/Science/Venus/Temperature-UV_Analysis_2024/Analysis/VMC/Step04/scripts/createTable_ThermalTide_Akiba2021_Figure5.py',
'',
' Orbit      lat            LST         T_VeRa   dT_VeRa    dT_tide ',
'            (˚)            (h)           (K)      (K)        (K) '
]

headerString = HandyTools.getTableHeader (tableFileName, creationScript = 'CreateTable_ThermalTideCorrection.py', headerLines = headerLines)
print (headerString, file = fileOpen)

currentOrbit = ''
for iSelectedImage in range ( len ( selectedImages [0][0] ) ):

    if selectedImages [1][0][iSelectedImage] != currentOrbit:
        
        currentOrbit = selectedImages [1][0][iSelectedImage]

        # Nominal and extended mission.
        if currentOrbit < '2775':

            for iProfile in range ( len ( VeRaSelectedProfiles ['OrbitID'] ) ):
            
                if currentOrbit in VeRaSelectedProfiles ['OrbitID'][iProfile]:
                
                    iLevel = 69 - ( int ( VeRaSelectedProfiles ['FilteredProfiles'][iProfile][0][0] ) - radiusOfVenus )
                    TVeRa = VeRaSelectedProfiles ['FilteredProfiles'][iProfile][1][iLevel]
                    dTVeRa = VeRaSelectedProfiles ['FilteredProfiles'][iProfile][2][iLevel]

        
        # South Polar Dynamics Campaign.
        else:

            for iProfile in range ( len ( VeRaSPoleProfiles ['OrbitID'] ) ):
            
                if currentOrbit in VeRaSPoleProfiles ['OrbitID'][iProfile]:
                
                    iLevel = 69 - ( int ( VeRaSPoleProfiles ['FilteredProfiles'][iProfile][0][0] ) - radiusOfVenus )
                    TVeRa = VeRaSPoleProfiles ['FilteredProfiles'][iProfile][1][iLevel]
                    dTVeRa = VeRaSPoleProfiles ['FilteredProfiles'][iProfile][2][iLevel]
            
         
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
                  TVeRa, dTVeRa,
                  thermalTideInterpolated ), file = fileOpen )



fileOpen.close ()


