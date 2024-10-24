# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241007

# Create the table with the (median) Radiance Factor Ratios per orbit (VMC/Step03  RadianceFactorRatiosPerOrbit.dat table created with the script  
#  CreateRadianceFactorRatioTable.py) and the VeRa-derived temperatures at altitudes between 60 and 80km.


# Choose the desired limitation in orbitIDVMC.

orbitIDLimit = [0, 'All orbits']
# orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']

# Standard imports.
import os
import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np

# Custom imports.
from HandyTools import HandyTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020 (VMC/Step03bis)
radianceFactorRatios = HandyTools.readTable ('../../Step03/RadianceFactorRatiosPerOrbit.dat')

# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020 (VMC/Step03bis)
figure14Data = HandyTools.readTable ('../../Step03bis/Marcq_2020_Figure14.dat')


orbitIDVMC = radianceFactorRatios [1][0]
numberOfVMCOrbits = len (orbitIDVMC)
radiadanceFactorsRatiosMedianPerOrbit = np.asarray ( radianceFactorRatios [0][4] )
dRadiadanceFactorsRatiosMedianPerOrbit = np.asarray ( radianceFactorRatios [0][5] )
iVMCImages = []


# Load the profiles of both the nominal and extended mission as well as the South Polar Dynamics Campaign from the  .profiles  NumPy files created
#  in VeRa/Step02 (see VeRa/Step02bis for more details on the structure of the  .profiles  files).
profilesNominalAndExtendedMission = np.load ('../../../VeRa/Step02/VeRaSelectedProfiles.profiles', allow_pickle = True).tolist ()
profilesSouthPolarDynamicsCampaign = np.load ('../../../VeRa/Step02/VeRaSouthPolarDynamicsCampaignProfiles.profiles', allow_pickle = True).tolist ()

profileSets = [profilesNominalAndExtendedMission, profilesSouthPolarDynamicsCampaign]
startAltitude = 50
endAltitude = 80
referenceAltitude = 65
iReferenceAltitude = referenceAltitude - startAltitude + 1

orbitIDVeRa = []

latitudesVeRa = []
altitudesCloudTop = []

temperaturesVeRa = []
dTemperaturesVeRa = []

for profileSet in profileSets:

    # This list will be used to extract the temperature gradients in the region where all the cloud tops fall: 65 - 74km.
    #  I use it to calculate an average temperature gradient, as compared to the gradient at the cloud top level.

    
    iAltitudeLevels = np.asarray ( [ int ( altitudeLevel - ( profileSet ['FilteredProfiles'][0][0][0] - radiusOfVenus ) )  
                                     for altitudeLevel in range (startAltitude, endAltitude + 1) ] )
    
    
    for iProfile in range ( len ( profileSet ['OrbitID'] ) ):
    
        if int ( profileSet ['OrbitID'][iProfile].split ('_')[0] ) >= orbitIDLimit [0]:

            # Not all VeRa profiles have valid VMC images, hence keep track of the indices of the VeRa profiles and corresponding VMC images.
            iVMCImage = 0
            while iVMCImage < numberOfVMCOrbits and orbitIDVMC [iVMCImage] != profileSet ['OrbitID'][iProfile].split ('_')[0]:
                         
                iVMCImage += 1
                
            if iVMCImage < numberOfVMCOrbits: 
            
                iVMCImages.append (iVMCImage)

                orbitIDVeRa.append ( profileSet ['OrbitID'][iProfile].split ('_')[0] )
                    
                profileVeRa = profileSet ['FilteredProfiles'][iProfile]
    
                # Get the VeRa-latitude at 70km altitude.          
                latitudesVeRa.append ( profileVeRa [5][ iAltitudeLevels [iReferenceAltitude] ] )
    
                # VeRA temperature in the 60 - 80km altitude range and their uncertainties            
                temperaturesVeRa.append ( profileVeRa [1][iAltitudeLevels] )
                dTemperaturesVeRa.append ( profileVeRa [2][iAltitudeLevels] )
    
                # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
                #  VMCSelectedImages [0][6] is the latitude of the VeRa profile.    
                iCloudTopBin = 9 - abs ( int ( latitudesVeRa [-1] / 10 ) ) - 1
                altitudesCloudTop.append ( int ( figure14Data [0][2][iCloudTopBin] + 0.5 ) )
    



tableFileName = os.path.abspath ( '../RadianceFactorRatio_vs_TVeRa{:2d}-{:2d}kmAltitude.dat'.format (startAltitude, endAltitude) )
fileOpen = open (tableFileName, 'w')

print (' ', file = fileOpen)
print (' File: {}'.format (tableFileName), file = fileOpen)
print (' Created at {}'.format ( HandyTools.getDateAndTimeString () ), file = fileOpen)


print (' ', file = fileOpen)
print (' RFR = Radiance Factor Ratio median for the VMC image (from VMC Step03 - RadianceFactorRatiosPerOrbit.dat)', file = fileOpen)
print (' z_cloudtop = cloud top altitude', file = fileOpen)
print (' latitude = latitude of the VeRa sounding at {:2d}km altitude'.format (referenceAltitude), file = fileOpen)



print (' ', file = fileOpen)

lineStringList = [ 'T{:2d}   dT    '.format (altitude)  for altitude in range (startAltitude, endAltitude + 1) ]
lineString = '  OrbitID     RFR     dRFR   z_cloudtop   latitude   '

lineStringList.insert (0, lineString)
print (' '.join (lineStringList), file = fileOpen)


lineStringList = [ '(K)   (K)   '  for altitude in range (startAltitude, endAltitude + 1) ]
lineString = '                                (km)        (˚)      '

lineStringList.insert (0, lineString)
print (' '.join (lineStringList), file = fileOpen)


print ('C_END', file = fileOpen)
    
for iPoint in range ( len (iVMCImages) ):
    

    lineStringList = [ '{:5.1f}  {:3.1f}  '.format (T, dT)  for T, dT in zip (temperaturesVeRa [iPoint], dTemperaturesVeRa [iPoint] ) ]
    lineString = '   {}      {:5.3f}   {:6.4f}      {:2d}      {:7.2f}    '.format ( orbitIDVMC [ iVMCImages [iPoint] ], 
                                                                                     radiadanceFactorsRatiosMedianPerOrbit [ iVMCImages [iPoint] ],
                                                                                     dRadiadanceFactorsRatiosMedianPerOrbit [ iVMCImages [iPoint] ],
                                                                                     altitudesCloudTop [iPoint],
                                                                                     latitudesVeRa [iPoint] )
    lineStringList.insert (0, lineString)
                     
    print (' '.join (lineStringList), file = fileOpen)    

fileOpen.close ()    

























