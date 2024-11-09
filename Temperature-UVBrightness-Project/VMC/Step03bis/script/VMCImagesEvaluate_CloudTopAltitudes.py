# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240827

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

from VMCTools import VMCTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *



# Load the content of the table created in VMC/Step01. In this table the VeRa derived temperastures are taken at 70km altitude, which is the assumed cloud top altitude 
#  for all latitudes.
tableContent = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step01', 'VMCSelectedImages.dat') )
tableContentPerLine = HandyTools.getTextFileContent ( os.path.join (VMCWorkBookDirectory, 'Step01','VMCSelectedImages.dat') )

# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020. Climatology of SO2 and UV absorber at Venus' cloud top from SPICAV-UV T nadir dataset. 
#  Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002).
figure14Data = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step03bis', 'Marcq_2020_Figure14.dat') )

# Load the profiles of both the nominal and extended mission as well as the South Polar Dynamics Campaign from the  .profiles  NumPy files created
#  in VeRa/Step02 (see VeRa/Step02bis for more details on the structure of the  .profiles  files).
profilesNominalAndExtendedMission = np.load ( os.path.join (VeRaWorkBookDirectory, 'Step02','VeRaSelectedProfiles.profiles'), allow_pickle = True).tolist ()
profilesSouthPolarDynamicsCampaign = np.load ( os.path.join (VeRaWorkBookDirectory, 'Step02', 'VeRaSouthPolarDynamicsCampaignProfiles.profiles'), allow_pickle = True).tolist ()



# Open the new table file that will contain information about all the selected images. 
# Use the header from the  VMCSelectedImages.dat  table file from VMC/Step01 and parts of the  VMC/Step01/VMCImagesEvaluate.py  script.
VMCSelectedImagesFileName = 'VMCSelectedImages_CloudTopAltitudes.dat'
fileOpen = open ( os.path.join (VMCWorkBookDirectory, 'Step03bis', VMCSelectedImagesFileName), 'w' )

headerLines = [
'',
'  LATVeRa and LONVeRa is for 70km altitude',
'  Target altitude of the cloud tops is determined from  Marcq_2020_Figure14.dat (Figure 14 in Marcq, R. et al., 2020. Climatology of SO2 and UV absorber at Venus cloud top from SPICAV-UV T nadir dataset. Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002))'
]

headerString = HandyTools.getTableHeader (VMCSelectedImagesFileName, creationScript = 'VMCImagesEvaluate_CloudTopAltitudes.py', headerLines = headerLines, addC_END = False)
print (headerString, file = fileOpen)

iLine = 6
while 'C_END' not in tableContentPerLine [iLine]:

    print (tableContentPerLine [iLine], file = fileOpen)
    iLine += 1

print (tableContentPerLine [iLine], file = fileOpen)


# Go through all the lines of the original table, get the latitude of the VeRa sounding, determine the corresponding cloud top altitude 
#  from the  Marcq_2020_Figure14.dat  table and extract the VeRa temperature at that level.
for iImage in range ( len ( tableContent [0][0] ) ):

    print ( ' image {}'.format ( tableContent [1][1][iImage] ) )
    # Find the correct VeRa profile using the orbitID (first column of  tableContent).
    orbitFound = False
    iVeRaProfile = 0
    while not orbitFound:
    
        if tableContent [0][0][iImage] >= 2775 and tableContent [0][0][iImage] <= 2811:
        
            if int ( profilesSouthPolarDynamicsCampaign ['OrbitID'][iVeRaProfile].split ('_')[0] ) == tableContent [0][0][iImage]:
            
                orbitFound = True
                profileVeRa = profilesSouthPolarDynamicsCampaign ['FilteredProfiles'][iVeRaProfile]
        
        else:
        
            if int ( profilesNominalAndExtendedMission ['OrbitID'][iVeRaProfile].split ('_')[0] ) == tableContent [0][0][iImage]:
            
                orbitFound = True
                profileVeRa = profilesNominalAndExtendedMission ['FilteredProfiles'][iVeRaProfile]
        
        iVeRaProfile += 1
            
    # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
    #  tableContent [0][6] is the latitude of the VeRa profile.    
    iCloudTopBin = 9 - abs ( int ( tableContent [0][6][iImage] / 10 ) ) - 1
    altitudeCloudTop = int ( figure14Data [0][2][iCloudTopBin] + 0.5 )
    
    # Determine the index in the filtered VeRa temperature profile that corresponds to the cloud top altitude.
    iAltitudeCloudTopInVeRaProfile = (radiusOfVenus + altitudeCloudTop) - int ( profileVeRa [0][0] )
    
    temperatureCloudTop = profileVeRa [1][iAltitudeCloudTopInVeRaProfile]
    dTemperatureCloudTop = profileVeRa [2][iAltitudeCloudTopInVeRaProfile]

#     print (iImage, tableContent [0][0][iImage], tableContent [0][6][iImage], altitudeCloudTop, iAltitudeCloudTopInVeRaProfile, temperatureCloudTop, dTemperatureCloudTop)    
    
    print ( ' {}   {}   {}    {:5.2f}       {:5.2f}      {:6.2f}    {:6.2f}    {:7.2f}         {:6.2f}      {:6.2f}  {:6.2f}      {:7.2f}      {:6.2f}   {:7.2f}     {:7.2f}         {:6d}             {:6.3f}           {:6.3f}        {:6.2f}   {:6.3f}       {:5.2f}             {:6.2f}           {:6.2f} '.
          format ( tableContent [0][0][iImage],
                   tableContent [1][1][iImage],
                   tableContent [1][2][iImage],
                   tableContent [0][3][iImage],
                   tableContent [0][4][iImage],
                   tableContent [0][5][iImage],
                   tableContent [0][6][iImage],
                   tableContent [0][7][iImage],
                   tableContent [0][8][iImage],
                   tableContent [0][9][iImage], tableContent [0][10][iImage],
                   tableContent [0][11][iImage],
                   tableContent [0][12][iImage], tableContent [0][13][iImage],
                   tableContent [0][14][iImage],
                   tableContent [0][15][iImage],
                   tableContent [0][16][iImage], 
                   tableContent [0][17][iImage],               
                   temperatureCloudTop,
                   dTemperatureCloudTop,   
                   tableContent [0][20][iImage],
                   tableContent [0][21][iImage],
                   tableContent [0][22][iImage] ), file = fileOpen )


fileOpen.close ()






