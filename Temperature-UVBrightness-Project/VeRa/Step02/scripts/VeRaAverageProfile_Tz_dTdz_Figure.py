# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240419


# Standard imports.
import numpy as np
import matplotlib.pyplot as plt


# # The TAB file path and name.
# VeRaProfileTABFileName = '../../../../Data/VEX/VeRa/VeRa_Spole_2013/Orb2805/V32ICL2L04_AEX_133590806_60.TAB'
# 
# # Get the filtered profile.
# VeRaFilteredProfile = VeRaTools.getFilteredVeRaProfile (VeRaProfileTABFileName)

VeRaProfiles = np.load ('../VeRaSouthPolarDynamicsCampaignProfiles.profiles', allow_pickle = True).tolist ()

iProfile = -1
VeRaFilteredProfile = VeRaProfiles ['FilteredProfiles'][iProfile]


plt.figure (1)
plt.clf ()

# The radius of Venus = 6051.8km, hence 6098km ~ 48km altitude

plt.scatter ( VeRaFilteredProfile [1], VeRaFilteredProfile [0] - 6098 + 48, marker = 'o', c = 'blue' )
plt.plot ( VeRaFilteredProfile [1], VeRaFilteredProfile [0] - 6098 + 48, c = 'blue' )
plt.ylim (50,100)
plt.xlabel ('T (K)')
plt.ylabel ('Altitude (km)')
plt.title ( 'VeRa VEX Orbit {} - {}, LST {}h, Lat {}˚'.format ( VeRaProfiles ['OrbitID'][iProfile],  VeRaProfiles ['DayOfYear'][iProfile], VeRaProfiles ['LocalSolarTime'][iProfile], VeRaProfiles ['LatitudeOneBar'][iProfile] ) )
plt.savefig ( '../plots/VeRaProfiles_Orb{}_T-z_Figure.png'.format ( VeRaProfiles ['OrbitID'][iProfile] ) )

plt.close ()


plt.figure (2)
plt.clf ()

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

                
plt.scatter ( VeRaFilteredProfile [7] + gamma, VeRaFilteredProfile [0] - 6098 + 48, marker = 'o', c = 'blue' )
plt.plot ( VeRaFilteredProfile [7] + gamma, VeRaFilteredProfile [0] - 6098 + 48, c = 'blue' )
plt.ylim (50,100)
plt.xlabel ('Static stability (K/km)')
plt.ylabel ('Altitude (km)')
plt.title ( 'VeRa VEX Orbit {} - {}, LST {}h, Lat {}˚'.format ( VeRaProfiles ['OrbitID'][iProfile],  VeRaProfiles ['DayOfYear'][iProfile], VeRaProfiles ['LocalSolarTime'][iProfile], VeRaProfiles ['LatitudeOneBar'][iProfile] ) )
plt.savefig ( '../plots/VeRaProfiles_Orb{}_dTdz-z_Figure.png'.format ( VeRaProfiles ['OrbitID'][iProfile] ) )

plt.close ()
    
