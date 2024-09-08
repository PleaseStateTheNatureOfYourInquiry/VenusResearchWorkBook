# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240908


# Standard imports.
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from HandyTools import HandyTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


VeRaProfiles = np.load ('../VeRaSouthPolarDynamicsCampaignProfiles.profiles', allow_pickle = True).tolist ()
# The   VeRaSouthPolarDynamicsCampaignProfiles.profiles   is created by the  VeRaAverageProfiles_CreateNumpyArray.py  script.
#     VeRaProfiles = {
#      'OrbitID' : [],
#      'ProfileID' : [],
#      'LatitudeOneBar' : [],
#      'LongitudeOneBar' : [],
#      'DayOfYear' : [],
#      'TimeOfDay' : [],
#      'LocalSolarTime' : [],
#      'FilteredProfiles' : [],
#      'NumberOfFilteredLevels' : [],
#      'OriginalProfiles' : [],
#      'NumberOfOriginalLevels' : []
#       }

# Each element of 'OriginalProfiles' is a list of seven lists (see the description of  VeRaTools.readVeRaTAB ), 
#  with index 0 and 1 the radius and temperature respectively.

iProfile = -1
VeRaFilteredProfile = VeRaProfiles ['FilteredProfiles'][iProfile]
VeraOriginalProfile = VeRaProfiles ['OriginalProfiles'][iProfile]


figure = plt.figure (1)
figure.set_figheight (6)
figure.set_figwidth (20)
figure.clf ()
figure.subplots_adjust (left = 0.05, right = 0.95)

axis1 = plt.subplot2grid ( shape = (1, 4), loc = (0, 0), colspan = 2 )
axis2 = plt.subplot2grid ( shape = (1, 4), loc = (0, 2), colspan = 1 )
axis3 = plt.subplot2grid ( shape = (1, 4), loc = (0, 3), colspan = 1 )


# The radius is from the  analysisConfiguration  file and set to 6052km.
# Left plot: filtered temperature profile example between 50-100km. Unfiltered profile in red.
axis1.scatter ( VeRaFilteredProfile [1], VeRaFilteredProfile [0] - radiusOfVenus, marker = 'o', c = 'blue' )
axis1.plot ( VeRaFilteredProfile [1], VeRaFilteredProfile [0] - radiusOfVenus, c = 'blue', label = 'filtered' )
axis1.plot ( VeraOriginalProfile [1], VeraOriginalProfile [0] - radiusOfVenus, c = 'orange', label = 'original' )
axis1.legend ()

axis1.set_ylim (50,100)
axis1.set_xlabel ('T (K)')
axis1.set_ylabel ('Altitude (km)')
axis1.set_title ( 'VeRa VEX Orbit {} - {}, LST {}h, Lat {}˚'.format ( VeRaProfiles ['OrbitID'][iProfile],  VeRaProfiles ['DayOfYear'][iProfile], VeRaProfiles ['LocalSolarTime'][iProfile], VeRaProfiles ['LatitudeOneBar'][iProfile] ) )

# Middle plot: The uncertainty in the average values in the filtered 
axis2.scatter ( VeRaFilteredProfile [2], VeRaFilteredProfile [0] - radiusOfVenus, marker = 'o', c = 'blue' )
axis2.plot ( VeRaFilteredProfile [2], VeRaFilteredProfile [0] - radiusOfVenus, c = 'blue' )
axis2.set_ylim (50,100)
axis2.set_xlabel ('Uncertainty (standard deviation) T (K)')

# Right plot: 
axis3.scatter ( VeRaFilteredProfile [9], VeRaFilteredProfile [0] - radiusOfVenus, marker = 'o', c = 'blue' )
iOne = np.where ( VeRaFilteredProfile [9] == 1 )[0]
axis3.scatter ( VeRaFilteredProfile [9][iOne], VeRaFilteredProfile [0][iOne] - radiusOfVenus, marker = 'x', c = 'red', label = 'one point' )
axis3.plot ( VeRaFilteredProfile [9], VeRaFilteredProfile [0] - radiusOfVenus, c = 'blue')
axis3.legend ()
axis3.set_ylim (50,100)
axis3.set_xlabel ('# points')


figure.savefig ( '../plots/VeRaProfiles_Orb{}_T-z_Figure.png'.format ( VeRaProfiles ['OrbitID'][iProfile] ) )

plt.close (figure)


plt.figure (2)
plt.clf ()

figure = plt.figure (2)
figure.set_figheight (6)
figure.set_figwidth (15)
figure.clf ()
figure.subplots_adjust (left = 0.05, right = 0.95)

axis1 = plt.subplot2grid ( shape = (1, 3), loc = (0, 0), colspan = 1 )
axis2 = plt.subplot2grid ( shape = (1, 3), loc = (0, 1), colspan = 1 )
axis3 = plt.subplot2grid ( shape = (1, 3), loc = (0, 2), colspan = 1 )


# dT/dz plot (left)   

axis1.scatter ( VeRaFilteredProfile [7], VeRaFilteredProfile [0] - radiusOfVenus, marker = 'o', c = 'blue' )
axis1.plot ( VeRaFilteredProfile [7] , VeRaFilteredProfile [0] - radiusOfVenus, c = 'blue' )
axis1.set_ylim (50,100)
axis1.set_xlabel ('dT/dz (K/km)')
axis1.set_ylabel ('Altitude (km)')
axis1.set_title ( 'VeRa VEX Orbit {} - {}, LST {}h, Lat {}˚'.
                  format ( VeRaProfiles ['OrbitID'][iProfile],  VeRaProfiles ['DayOfYear'][iProfile], 
                           VeRaProfiles ['LocalSolarTime'][iProfile], VeRaProfiles ['LatitudeOneBar'][iProfile] ), fontsize = 10 )





# Calculate the adiabatic lapse rate is from Fig. 18 from Seiff et al. 1980, which I measured and parametrized between 200 and 350K
# T1 = 200 K, -gamma1 = 11.6 + 9/14.5 * 0.4 K/km
# T2 = 250 K, -gamma2 = 10.8 + 5/14.5 * 0.4 K/km
# T3 = 350 K, -gamma3 = 9.6 + 6.7 / 14.5 * 0.4 K/km
gamma1 = 11.6 + (9/14.5) * 0.4 
gamma2 = 10.8 + (5/14.5) * 0.4
gamma3 =  9.6 + (6.7/14.5) * 0.4

gamma = []
for iLevel in range (VeRaProfiles ['NumberOfFilteredLevels'][iProfile]):

    if VeRaFilteredProfile [1][iLevel] < 250:
    
        gamma.append ( gamma1 + (VeRaFilteredProfile [1][iLevel] - 200.) * (gamma2 - gamma1) / (250. - 200.) )

    else:
    
        gamma.append ( gamma2 + (VeRaFilteredProfile [1][iLevel] - 250.) * (gamma3 - gamma2) / (350. - 250.) )


axis2.scatter ( gamma, VeRaFilteredProfile [0] - radiusOfVenus, marker = 'o', c = 'blue' )
axis2.plot (gamma, VeRaFilteredProfile [0] - radiusOfVenus, c = 'blue' )
axis2.set_ylim (50,100)
axis2.set_xlabel ('Adiabatic Lapse Rate (K/km)')
axis2.set_ylabel ('Altitude (km)')
axis2.set_title ('Parametrisation from Seiff et al. 1980')


             
# Static stability plot (right)   

axis3.scatter ( VeRaFilteredProfile [7] + gamma, VeRaFilteredProfile [0] - radiusOfVenus, marker = 'o', c = 'blue' )
axis3.plot ( VeRaFilteredProfile [7] + gamma, VeRaFilteredProfile [0] - radiusOfVenus, c = 'blue' )
axis3.set_ylim (50,100)
axis3.set_xlabel ('Static stability (K/km)')
axis3.set_ylabel ('Altitude (km)')
axis3.set_title ( 'VeRa VEX Orbit {} - {}, LST {}h, Lat {}˚'.
                  format ( VeRaProfiles ['OrbitID'][iProfile],  VeRaProfiles ['DayOfYear'][iProfile], 
                           VeRaProfiles ['LocalSolarTime'][iProfile], VeRaProfiles ['LatitudeOneBar'][iProfile] ), fontsize = 10 )


figure.savefig ( '../plots/VeRaProfiles_Orb{}_dTdz-z_Figure.png'.format ( VeRaProfiles ['OrbitID'][iProfile] ) )

plt.close (figure)
    
