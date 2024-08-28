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


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020. Climatology of SO2 and UV absorber at Venus' cloud top from SPICAV-UV T nadir dataset. 
#  Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002).
figure14Data = HandyTools.readTable ('../Marcq_2020_Figure14.dat')

# Load the profiles of both the nominal and extended mission as well as the South Polar Dynamics Campaign from the  .profiles  NumPy files created
#  in VeRa/Step02 (see VeRa/Step02bis for more details on the structure of the  .profiles  files).
profilesNominalAndExtendedMission = np.load ('../../../VeRa/Step02/VeRaSelectedProfiles.profiles', allow_pickle = True).tolist ()
profilesSouthPolarDynamicsCampaign = np.load ('../../../VeRa/Step02/VeRaSouthPolarDynamicsCampaignProfiles.profiles', allow_pickle = True).tolist ()

profileSets = [profilesNominalAndExtendedMission, profilesSouthPolarDynamicsCampaign]

latitudeLevel = 70 #km

latitudesVeRa = []
altitudesCloudTop = []
cloudTopTemperatureVeRa = []
dCloudTopTemperatureVeRa = []

for profileSet in profileSets:

    iLatitudeLevel = int ( radiusOfVenus + latitudeLevel - profileSet ['FilteredProfiles'][0][0][0] )
    
    for iProfile in range ( len ( profileSet ['OrbitID'] ) ):
    
        if int ( profileSet ['OrbitID'][iProfile].split ('_')[0] ) >= 1188:
                
            profileVeRa = profileSet ['FilteredProfiles'][iProfile]
            
            latitudesVeRa.append ( profileVeRa [5][iLatitudeLevel] )
        
        
            # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
            #  tableContent [0][6] is the latitude of the VeRa profile.    
            iCloudTopBin = 9 - abs ( int ( latitudesVeRa [-1] / 10 ) ) - 1
            altitudesCloudTop.append ( int ( figure14Data [0][2][iCloudTopBin] + 0.5 ) )
            
            # Determine the index in the filtered VeRa temperature profile that corresponds to the cloud top altitude.
            iAltitudeCloudTopInVeRaProfile = ( radiusOfVenus + altitudesCloudTop [-1] ) - int ( profileVeRa [0][0] )
            
            cloudTopTemperatureVeRa.append ( profileVeRa [1][iAltitudeCloudTopInVeRaProfile] )
            dCloudTopTemperatureVeRa.append ( profileVeRa [2][iAltitudeCloudTopInVeRaProfile] )


fit = DataTools.linearLeastSquare (latitudesVeRa, cloudTopTemperatureVeRa, fractionBeyondXRange = 0.1)


plt.clf ()

fig, ax1 = plt.subplots ()

colour = 'tab:blue'
ax1.set_title ('Cloud top VeRa temperatures (blue) and altitudes (green)')
ax1.set_xlabel ( 'latitude (˚)' )
ax1.set_xlim (-95,0)
ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )

ax1.set_ylabel ('cloud top temperature (km)', color = colour)
ax1.scatter (latitudesVeRa, cloudTopTemperatureVeRa, c = 'blue', s = 25)
ax1.tick_params (axis='y', labelcolor = colour)

HandyTools.plotErrorBars (latitudesVeRa, cloudTopTemperatureVeRa, yErrors = dCloudTopTemperatureVeRa, colours = 'blue')

ax1.plot ( fit [5], fit [6], c = 'black', alpha = 0.2, label = 'T_cloud = {:5.2f} * lat + {:5.2f} ($r^2$ = {:5.3f})'.format ( fit [0], fit [1], fit [4] ) )
ax1.legend (loc = 'lower right', fontsize = 8)

# instantiate a second Axes that shares the same x-axis
ax2 = ax1.twinx ()  

colour = 'tab:green'
ax2.set_ylabel ('altitude cloud top (km)', color = colour)
ax2.scatter (latitudesVeRa, altitudesCloudTop, color = 'lightgreen', marker = 'D', s = 10)
ax2.tick_params (axis='y', labelcolor = colour)

plt.savefig ( '../plots/cloudTopTemperatureVeRa.png' )

plt.close (1)
plt.close (2)



