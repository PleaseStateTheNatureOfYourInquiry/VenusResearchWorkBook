# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241102

# Create the table with the average Radiance Factor Ratios per orbit (VMC/Step03  RadianceFactorRatiosPerOrbit.dat table created with the script  
#  CreateRadianceFactorRatioTable.py) and the VeRa-derived temperatures at altitudes between 50 and 80km.

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


# tableType = 'temperature'
tableType = 'staticStability'


# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020 (VMC/Step03bis)
radianceFactorRatios = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step03', 'RadianceFactorRatiosPerOrbit.dat') )

# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020 (VMC/Step03bis)
figure14Data = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step03bis', 'Marcq_2020_Figure14.dat') )


orbitIDVMC = radianceFactorRatios [1][0]
numberOfVMCOrbits = len (orbitIDVMC)


radiadanceFactorsRatiosAveragePerOrbit = np.asarray ( radianceFactorRatios [0][2] )
dRadiadanceFactorsRatiosAveragePerOrbit = np.asarray ( radianceFactorRatios [0][3] )

# radiadanceFactorsRatiosMedianPerOrbit = np.asarray ( radianceFactorRatios [0][4] )
# dRadiadanceFactorsRatiosMedianPerOrbit = np.asarray ( radianceFactorRatios [0][5] )


iVMCImages = []


# Load the profiles of both the nominal and extended mission as well as the South Polar Dynamics Campaign from the  .profiles  NumPy files created
#  in VeRa/Step02 (see VeRa/Step02bis for more details on the structure of the  .profiles  files).
profilesNominalAndExtendedMission = np.load ( os.path.join (VeRaWorkBookDirectory, 'Step02', 'VeRaSelectedProfiles.profiles'), allow_pickle = True).tolist ()
profilesSouthPolarDynamicsCampaign = np.load ( os.path.join (VeRaWorkBookDirectory, 'Step02',' VeRaSouthPolarDynamicsCampaignProfiles.profiles'), allow_pickle = True).tolist ()

profileSets = [profilesNominalAndExtendedMission, profilesSouthPolarDynamicsCampaign]
startAltitude = 50
endAltitude = 80
referenceAltitude = 65
iReferenceAltitude = referenceAltitude - startAltitude + 1


# Calculate the adiabatic lapse rate is from Fig. 18 from Seiff et al. 1980, which I measured and parametrized between 200 and 350K
# T1 = 200 K, -gamma1 = 11.6 + 9/14.5 * 0.4 K/km
# T2 = 250 K, -gamma2 = 10.8 + 5/14.5 * 0.4 K/km
# T3 = 350 K, -gamma3 = 9.6 + 6.7 / 14.5 * 0.4 K/km
gamma1 = 11.6 + (9/14.5) * 0.4 
gamma2 = 10.8 + (5/14.5) * 0.4
gamma3 =  9.6 + (6.7/14.5) * 0.4
                

orbitIDVeRa = []

latitudesVeRa = []
altitudesCloudTop = []

temperaturesVeRa = []
dTemperaturesVeRa = []


for profileSet in profileSets:
    
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
    
                # Get the VeRa-latitude at the  referenceAltitude  altitude.          
                latitudesVeRa.append ( profileVeRa [5][ iAltitudeLevels [iReferenceAltitude] ] )
    
                # VeRA temperature in the 50 - 80km altitude range and their uncertainties
                if tableType == 'temperature':
                            
                    temperaturesVeRa.append ( profileVeRa [1][iAltitudeLevels] )
                    dTemperaturesVeRa.append ( profileVeRa [2][iAltitudeLevels] )


                if tableType == 'staticStability':
                
                    gamma = []
                    dGamma = []
                    for iAltitudeLevel in iAltitudeLevels:
                                  
                        if profileVeRa [1][iAltitudeLevel] < 250:
                        
                            gamma.append ( gamma1 + (profileVeRa [1][iAltitudeLevel] - 200.) * (gamma2 - gamma1) / (250. - 200.) )
                            dGamma.append ( profileVeRa [2][iAltitudeLevel] * (gamma2 - gamma1) / (250. - 200.) ) 
                    
                        else:
                        
                            gamma.append ( gamma2 + (profileVeRa [1][iAltitudeLevel] - 250.) * (gamma3 - gamma2) / (350. - 250.) )
                            dGamma.append ( profileVeRa [2][iAltitudeLevel] * (gamma3 - gamma2) / (350. - 250.) ) 


#                     print (profileSet ['OrbitID'][iProfile], iAltitudeLevels [15], profileVeRa [7][ iAltitudeLevels [15] ], gamma [15], profileVeRa [8][iAltitudeLevels [15]], dGamma [15])
                    temperaturesVeRa.append ( profileVeRa [7][iAltitudeLevels] + np.asarray (gamma) )
                    dTemperaturesVeRa.append ( np.sqrt ( profileVeRa [8][iAltitudeLevels] ** 2 + np.asarray (dGamma) ** 2 ) )

    
                # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
                #  VMCSelectedImages [0][6] is the latitude of the VeRa profile.    
                iCloudTopBin = 9 - abs ( int ( latitudesVeRa [-1] / 10 ) ) - 1
                altitudesCloudTop.append ( int ( figure14Data [0][2][iCloudTopBin] + 0.5 ) )
    


if tableType == 'temperature':

    tableFileName = 'RadianceFactorRatio_vs_TVeRa{:2d}-{:2d}kmAltitude.dat'.format (startAltitude, endAltitude)


if tableType == 'staticStability':

    tableFileName = 'RadianceFactorRatio_vs_SVeRa{:2d}-{:2d}kmAltitude.dat'.format (startAltitude, endAltitude)


fileOpen = open ( os.path.join (VMCWorkBookDirectory, 'Step06', tableFileName), 'w' )

headerLines = [
'',
' RFR = Radiance Factor Ratio average for the VMC image (from VMC Step03 - RadianceFactorRatiosPerOrbit.dat)',
' z_cloudtop = cloud top altitude',
' latitude = latitude of the VeRa sounding at {:2d}km altitude'.format (referenceAltitude),
''
]

headerString = HandyTools.getTableHeader (tableFileName, creationScript = 'CreateTable_RadianceFactorRatios_vs_T-SVeRa.py', headerLines = headerLines, addC_END = False)
print (headerString, file = fileOpen)

if tableType == 'temperature':

    lineStringList = [ 'T{:2d}   dT    '.format (altitude)  for altitude in range (startAltitude, endAltitude + 1) ]
    lineString = '  OrbitID     RFR     dRFR   z_cloudtop   latitude   '
    
    lineStringList.insert (0, lineString)
    print (' '.join (lineStringList), file = fileOpen)
    
    
    lineStringList = [ '(K)   (K)   '  for altitude in range (startAltitude, endAltitude + 1) ]
    lineString = '                                (km)        (˚)      '
    
    lineStringList.insert (0, lineString)
    print (' '.join (lineStringList), file = fileOpen)


if tableType == 'staticStability':

    lineStringList = [ 'S{:2d}   dS    '.format (altitude)  for altitude in range (startAltitude, endAltitude + 1) ]
    lineString = '  OrbitID     RFR     dRFR   z_cloudtop   latitude   '
    
    lineStringList.insert (0, lineString)
    print (' '.join (lineStringList), file = fileOpen)
    
    
    lineStringList = [ '    (K/km)  '  for altitude in range (startAltitude, endAltitude + 1) ]
    lineString = '                                (km)        (˚)   '
    
    lineStringList.insert (0, lineString)
    print (' '.join (lineStringList), file = fileOpen)


print ('C_END', file = fileOpen)


for iPoint in range ( len (iVMCImages) ):
    
    if tableType == 'temperature':

        lineStringList = [ '{:5.1f}  {:3.1f}  '.format (T, dT)  for T, dT in zip (temperaturesVeRa [iPoint], dTemperaturesVeRa [iPoint] ) ]
        lineString = '   {}      {:5.3f}   {:6.4f}      {:2d}      {:7.2f}    '.format ( orbitIDVMC [ iVMCImages [iPoint] ], 
                                                                                         radiadanceFactorsRatiosAveragePerOrbit [ iVMCImages [iPoint] ],
                                                                                         dRadiadanceFactorsRatiosAveragePerOrbit [ iVMCImages [iPoint] ],
                                                                                         altitudesCloudTop [iPoint],
                                                                                         latitudesVeRa [iPoint] )
        lineStringList.insert (0, lineString)
                         
        print (' '.join (lineStringList), file = fileOpen)    

 
    if tableType == 'staticStability':

        lineStringList = [ '{:5.1f}  {:3.1f}  '.format (T, dT)  for T, dT in zip (temperaturesVeRa [iPoint], dTemperaturesVeRa [iPoint] ) ]
        lineString = '   {}      {:5.3f}   {:6.4f}      {:2d}      {:7.2f}    '.format ( orbitIDVMC [ iVMCImages [iPoint] ], 
                                                                                         radiadanceFactorsRatiosAveragePerOrbit [ iVMCImages [iPoint] ],
                                                                                         dRadiadanceFactorsRatiosAveragePerOrbit [ iVMCImages [iPoint] ],
                                                                                         altitudesCloudTop [iPoint],
                                                                                         latitudesVeRa [iPoint] )
        lineStringList.insert (0, lineString)
                         
        print (' '.join (lineStringList), file = fileOpen)    



fileOpen.close ()    

























