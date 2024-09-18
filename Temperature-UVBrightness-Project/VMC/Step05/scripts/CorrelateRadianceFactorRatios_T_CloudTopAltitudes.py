# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240917

# 

# Chose the desired limitation in orbitIDVMC.

# orbitIDLimit = [0, 'All orbits']
orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']


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



# Load the content of the  VMCSelectedImages_CloudTopAltitudes.dat  table created in VMC/Step01. 
#  In this table the VeRa derived temperatures are taken at 70km altitude, the cloud top temperature assumed (in Step01) constant for all latitudes.
VMCSelectedImages = HandyTools.readTable ('../../Step03bis/VMCSelectedImages_CloudTopAltitudes.dat')
numberOfVMCImages = len ( VMCSelectedImages [0][0] )

# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020 (VMC/Step03bis)
radianceFactorRatios = HandyTools.readTable ('../../Step03/RadianceFactorRatiosPerOrbit.dat')

orbitIDVMC = radianceFactorRatios [1][0]
numberOfVMCOrbits = len (orbitIDVMC)
radiadanceFactorsRatiosMedianPerOrbit = np.asarray ( radianceFactorRatios [0][4] )
dradiadanceFactorsRatiosMedianPerOrbit = np.asarray ( radianceFactorRatios [0][5] )



# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020 (VMC/Step03bis)
figure14Data = HandyTools.readTable ('../../Step03bis/Marcq_2020_Figure14.dat')


# Load the thermal tide correction as determined in VMC/Step04.
thermalTideTable = HandyTools.readTable ('../../Step04/ThermalTideCorrection.dat')



# Load the profiles of both the nominal and extended mission as well as the South Polar Dynamics Campaign from the  .profiles  NumPy files created
#  in VeRa/Step02 (see VeRa/Step02bis for more details on the structure of the  .profiles  files).
profilesNominalAndExtendedMission = np.load ('../../../VeRa/Step02/VeRaSelectedProfiles.profiles', allow_pickle = True).tolist ()
profilesSouthPolarDynamicsCampaign = np.load ('../../../VeRa/Step02/VeRaSouthPolarDynamicsCampaignProfiles.profiles', allow_pickle = True).tolist ()

profileSets = [profilesNominalAndExtendedMission, profilesSouthPolarDynamicsCampaign]

latitudeLevel = 70 #km

orbitIDVeRa = []

latitudesVeRa = []
altitudesCloudTop = []

cloudTopTemperatureVeRa = []
dCloudTopTemperatureVeRa = []

cloudTopTemperatureGradientVeRa = []
dCloudTopTemperatureGradientVeRa = []

cloudTopTemperatureGradientVeRaAverage = []
dCloudTopTemperatureGradientVeRaAverage = []

cloudTopTemperatureGradientVeRaMedian = []
dCloudTopTemperatureGradientVeRaMedian = []

for profileSet in profileSets:

    iLatitudeLevel = int ( radiusOfVenus + latitudeLevel - profileSet ['FilteredProfiles'][0][0][0] )

    # This list will be used to extract the temperature gradients in the region where all the cloud tops fall: 65 - 74km.
    #  I use it to calculate an average temperature gradient, as compared to the gradient at the cloud top level.
    iLatitudeLevels = np.asarray ( [ int ( radiusOfVenus + latitudeLevel - profileSet ['FilteredProfiles'][0][0][0] )  for latitudeLevel in range (65,75) ] )
    
    for iProfile in range ( len ( profileSet ['OrbitID'] ) ):
    
        if int ( profileSet ['OrbitID'][iProfile].split ('_')[0] ) >= orbitIDLimit [0]:

            orbitIDVeRa.append ( profileSet ['OrbitID'][iProfile].split ('_')[0] )
                
            profileVeRa = profileSet ['FilteredProfiles'][iProfile]
            
            latitudesVeRa.append ( profileVeRa [5][iLatitudeLevel] )
        
        
            # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
            #  VMCSelectedImages [0][6] is the latitude of the VeRa profile.    
            iCloudTopBin = 9 - abs ( int ( latitudesVeRa [-1] / 10 ) ) - 1
            altitudesCloudTop.append ( int ( figure14Data [0][2][iCloudTopBin] + 0.5 ) )
            
            # Determine the index in the filtered VeRa temperature profile that corresponds to the cloud top altitude.
            iAltitudeCloudTopInVeRaProfile = ( radiusOfVenus + altitudesCloudTop [-1] ) - int ( profileVeRa [0][0] )

            # Store the cloud top temperature and its uncertainty.            
            cloudTopTemperatureVeRa.append ( profileVeRa [1][iAltitudeCloudTopInVeRaProfile] )
            dCloudTopTemperatureVeRa.append ( profileVeRa [2][iAltitudeCloudTopInVeRaProfile] )
            
            
            # Store the cloud top temperature gradient and its uncertainty.
            cloudTopTemperatureGradientVeRa.append ( profileVeRa [7][iAltitudeCloudTopInVeRaProfile] )
            dCloudTopTemperatureGradientVeRa.append ( profileVeRa [8][iAltitudeCloudTopInVeRaProfile] )


            # Calculate and store the average temperature gradient and its uncertainty in the 65 - 74km altitude range.
            averageTemperatureGradientPerProfile = DataTools.getAverageVarAndSDPYtoCPP ( DataTools.getNanFreeNumpyArray ( profileVeRa [7][iLatitudeLevels] ) )
            cloudTopTemperatureGradientVeRaAverage.append ( averageTemperatureGradientPerProfile [0] )
           
            cloudTopTemperatureGradientVeRaUncertainties = DataTools.getNanFreeNumpyArray (profileVeRa [8][iLatitudeLevels])
            dCloudTopTemperatureGradientVeRaAverage.append ( 
             max ( np.sum ( cloudTopTemperatureGradientVeRaUncertainties ** 2 ) / len (cloudTopTemperatureGradientVeRaUncertainties), 
                   averageTemperatureGradientPerProfile [1] ) )


            # Calculate and store the median temperature gradient and its uncertainty in the 65 - 74km altitude range.
            medianTemperatureGradientPerProfile = DataTools.getMedianAndQuantilesPYtoCPP ( 
             DataTools.getNanFreeNumpyArray ( profileVeRa [7][iLatitudeLevels] ), lowerQuantilePercentage = 33, upperQuantilePercentage = 67,
             uncertainties = DataTools.getNanFreeNumpyArray ( profileVeRa [8][iLatitudeLevels] ) )
            
            cloudTopTemperatureGradientVeRaMedian.append ( medianTemperatureGradientPerProfile [0] ) 
            errorBars = max ( medianTemperatureGradientPerProfile [2] - medianTemperatureGradientPerProfile [0], 
                              medianTemperatureGradientPerProfile [0] - medianTemperatureGradientPerProfile [1] )
            dCloudTopTemperatureGradientVeRaMedian.append ( max (medianTemperatureGradientPerProfile [3], errorBars) )



cloudTopTemperatureVeRa = np.asarray (cloudTopTemperatureVeRa)
dCloudTopTemperatureVeRa = np.asarray (dCloudTopTemperatureVeRa)

cloudTopAltitudesUnique = list ( set (altitudesCloudTop) )

cloudTopTemperatureVeRaCorrected = []
dCloudTopTemperatureVeRaCorrected = []
radiadanceFactorsRatiosMedianPerOrbitCorrected = []
dradiadanceFactorsRatiosMedianPerOrbitCorrected = []


iVeRaProfileForVMCImagesCorrected = []

iPlot = 0
for cloudTopAltitude in cloudTopAltitudesUnique:

    iVeRaProfiles = np.where ( np.asarray (altitudesCloudTop) == cloudTopAltitude )[0]


    # The cloud top temperature correction relative to 71km altitude could be estimated 
    if cloudTopAltitude == 65:
    
        temperatureCorrection = -6
        
    elif cloudTopAltitude == 73:
    
        temperatureCorrection = 2

    else:
    
        temperatureCorrection = 0


    iVMCImages = []
    iVeRaProfileForVMCImages = []
    cloudTopTemperatureVeRaForVMCImages = []
    thermalTideCorrection = []  
    latitudeMinimum = 0
    latitudeMaximum = -90
    for iVeRaProfile in iVeRaProfiles:
    
        iVMCImage = 0
        while iVMCImage < numberOfVMCOrbits and orbitIDVMC [iVMCImage] != orbitIDVeRa [iVeRaProfile]:
                           
            iVMCImage += 1
            
        if iVMCImage < numberOfVMCOrbits: 
        
            iVMCImages.append (iVMCImage)
            iVeRaProfileForVMCImages.append (iVeRaProfile)

            # Search through the lines of the  thermalTideTable  for the corresponding VeRa profile.
            #  orbitIDVeRa [iVeRaProfile]  is a string variable, hence use  thermalTideTable [1] .
            iTermalTideTableLine = 0
            while thermalTideTable [1][0][iTermalTideTableLine] != orbitIDVeRa [iVeRaProfile]:
            
                iTermalTideTableLine += 1
                
            thermalTideCorrection.append ( thermalTideTable [0][5][iTermalTideTableLine] )

            # Determine the latitude range.
            if latitudesVeRa [iVeRaProfile] > latitudeMaximum:
            
                latitudeMaximum = latitudesVeRa [iVeRaProfile]
                
            if latitudesVeRa [iVeRaProfile] < latitudeMinimum:
            
                latitudeMinimum = latitudesVeRa [iVeRaProfile]

#             print (iVeRaProfile, orbitIDVeRa [iVeRaProfile], thermalTideTable [1][0][iTermalTideTableLine], thermalTideCorrection)
            
            cloudTopTemperatureVeRaCorrected.append ( cloudTopTemperatureVeRa [iVeRaProfile] + temperatureCorrection - thermalTideCorrection [-1] )
            dCloudTopTemperatureVeRaCorrected.append ( dCloudTopTemperatureVeRa [iVeRaProfile] )
            radiadanceFactorsRatiosMedianPerOrbitCorrected.append ( radiadanceFactorsRatiosMedianPerOrbit [iVMCImage] )
            dradiadanceFactorsRatiosMedianPerOrbitCorrected.append ( dradiadanceFactorsRatiosMedianPerOrbit [iVMCImage] ) 

  
    iVMCImages = np.asarray (iVMCImages) 
    iVeRaProfileForVMCImages = np.asarray (iVeRaProfileForVMCImages)
    thermalTideCorrection = np.asarray (thermalTideCorrection)
               
    if len (iVMCImages):
    
        iPlot += 1
        
        plt.figure (iPlot)
        plt.clf ()

        plt.scatter ( cloudTopTemperatureVeRa [iVeRaProfileForVMCImages] - thermalTideCorrection, radiadanceFactorsRatiosMedianPerOrbit [iVMCImages] )
        plt.xlim (195,240)
        plt.ylim (0.6, 1.5)

        plt.title ( '{:2d}km — latitudes from {:3.0f}˚ to {:-3.0f}˚'.format (cloudTopAltitude, latitudeMinimum, latitudeMaximum) )
        plt.xlabel ( 'Cloud top temperature at {:2d}km (K) (VeRa)'.format (cloudTopAltitude) )
        plt.ylabel ( 'Radiance Factor Ratio (VMC)')
        

        HandyTools.plotErrorBars ( cloudTopTemperatureVeRa [iVeRaProfileForVMCImages] - thermalTideCorrection, radiadanceFactorsRatiosMedianPerOrbit [iVMCImages], 
                                   xErrors = dCloudTopTemperatureVeRa [iVeRaProfileForVMCImages],
                                   yErrors = dradiadanceFactorsRatiosMedianPerOrbit [iVMCImages], colours = 'blue' )

        fit = DataTools.linearLeastSquare ( cloudTopTemperatureVeRa [iVeRaProfileForVMCImages] - thermalTideCorrection, 
                                            radiadanceFactorsRatiosMedianPerOrbit [iVMCImages], 
                                            fractionBeyondXRange = 0.1 )
        
        print (cloudTopAltitude)
        print ('a = ', fit [0], fit [2])
        print ('b = ', fit [1], fit [3])
        print ('rSquared = ', fit [4])
        
        plt.plot (fit [5], fit [6], c = 'black', alpha = 0.2)

        plt.savefig ( '../plots/cloudTopTemperature_{:2d}km_vs_RadianceFactorRatio.png'.format (cloudTopAltitude) )


iPlot += 1


plt.figure (iPlot)
plt.clf ()

plt.scatter ( cloudTopTemperatureVeRaCorrected, radiadanceFactorsRatiosMedianPerOrbitCorrected )
plt.xlim (195,240)
plt.ylim (0.6, 1.5)

plt.title ( '{:2d}km'.format (cloudTopAltitude) )
plt.xlabel ( 'Cloud top temperature corrected to 71km (VeRa)'.format (cloudTopAltitude) )
plt.ylabel ( 'Radiance Factor Ratio (VMC)')


HandyTools.plotErrorBars ( cloudTopTemperatureVeRaCorrected, radiadanceFactorsRatiosMedianPerOrbitCorrected, 
                           xErrors = dCloudTopTemperatureVeRaCorrected,
                           yErrors = dradiadanceFactorsRatiosMedianPerOrbitCorrected, colours = 'blue' )

fit = DataTools.linearLeastSquare (cloudTopTemperatureVeRaCorrected, radiadanceFactorsRatiosMedianPerOrbitCorrected, fractionBeyondXRange = 0.1)


print ('corrected')
print ('a = ',fit [0], fit [2])
print ('b =', fit [1], fit [3])
print ('rSquared = ', fit [4])

plt.plot (fit [5], fit [6], c = 'black', alpha = 0.2)

plt.savefig ( '../plots/cloudTopTemperatureCorrected_vs_RadianceFactorRatio.png' )
























