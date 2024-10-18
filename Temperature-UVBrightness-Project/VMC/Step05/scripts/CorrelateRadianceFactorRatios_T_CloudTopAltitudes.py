# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240928

# Analysis of the cloud top temperatures vs radiance factor ratios.

# Chose the desired limitation in orbitIDVMC.

# orbitIDLimit = [0, 'All orbits']
orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']
createTable = True
createFigures = False
fitAndPlot = False


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

altitudeLevel = 70 #km

orbitIDVeRa = []

latitudesVeRa = []
altitudesCloudTop = []

cloudTopTemperatureVeRa = []
dCloudTopTemperatureVeRa = []

for profileSet in profileSets:

    iAltitudeLevel = int ( radiusOfVenus + altitudeLevel - profileSet ['FilteredProfiles'][0][0][0] )
    
    for iProfile in range ( len ( profileSet ['OrbitID'] ) ):
    
        if int ( profileSet ['OrbitID'][iProfile].split ('_')[0] ) >= orbitIDLimit [0]:

            orbitIDVeRa.append ( profileSet ['OrbitID'][iProfile].split ('_')[0] )
                
            profileVeRa = profileSet ['FilteredProfiles'][iProfile]
            
            latitudesVeRa.append ( profileVeRa [5][iAltitudeLevel] )
        
        
            # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
            #  VMCSelectedImages [0][6] is the latitude of the VeRa profile.    
            iCloudTopBin = 9 - abs ( int ( latitudesVeRa [-1] / 10 ) ) - 1
            altitudesCloudTop.append ( int ( figure14Data [0][2][iCloudTopBin] + 0.5 ) )
            
            # Determine the index in the filtered VeRa temperature profile that corresponds to the cloud top altitude.
            iAltitudeCloudTopInVeRaProfile = ( radiusOfVenus + altitudesCloudTop [-1] ) - int ( profileVeRa [0][0] )

            # Store the cloud top temperature and its uncertainty.            
            cloudTopTemperatureVeRa.append ( profileVeRa [1][iAltitudeCloudTopInVeRaProfile] )
            dCloudTopTemperatureVeRa.append ( profileVeRa [2][iAltitudeCloudTopInVeRaProfile] )



cloudTopTemperatureVeRa = np.asarray (cloudTopTemperatureVeRa)
dCloudTopTemperatureVeRa = np.asarray (dCloudTopTemperatureVeRa)

cloudTopAltitudesUnique = list ( set (altitudesCloudTop) )

cloudTopTemperatureVeRaUnCorrected = []
cloudTopTemperatureGradientCorrection = []
cloudTopTemperatureThermalTideCorrection = []
cloudTopTemperatureVeRaCorrected = []
dcloudTopTemperatureVeRaCorrected = []
radiadanceFactorsRatiosMedianPerOrbitCorrected = []
dRadiadanceFactorsRatiosMedianPerOrbitCorrected = []
cloudTopAltitudes = []
latitudes = []


iVeRaProfileForVMCImagesCorrected = []

# Create a plot of cloud top temperature vs RFR for each by cloud top altitude: 65, 71, 73 and 74km, though the last one does not have any corresponding
#  VMC images / points.
iPlot = 0
for cloudTopAltitude in cloudTopAltitudesUnique:

    iVeRaProfiles = np.where ( np.asarray (altitudesCloudTop) == cloudTopAltitude )[0]


    # The cloud top temperature correction relative to 71km altitude can be estimated by considering the temperature gradient to be on the order of -1K/km
    #  in the 65-74km altitude range across the latitudes.
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

            # Keep track of the latitude range for this cloud top altitude.
            if latitudesVeRa [iVeRaProfile] > latitudeMaximum:
            
                latitudeMaximum = latitudesVeRa [iVeRaProfile]
                
            if latitudesVeRa [iVeRaProfile] < latitudeMinimum:
            
                latitudeMinimum = latitudesVeRa [iVeRaProfile]
 
    
            cloudTopTemperatureVeRaUnCorrected.append ( cloudTopTemperatureVeRa [iVeRaProfile] )
            cloudTopTemperatureGradientCorrection.append (temperatureCorrection)
            cloudTopTemperatureThermalTideCorrection.append ( thermalTideCorrection [-1] )
            cloudTopTemperatureVeRaCorrected.append ( cloudTopTemperatureVeRa [iVeRaProfile] + temperatureCorrection - thermalTideCorrection [-1] )
            dcloudTopTemperatureVeRaCorrected.append ( dCloudTopTemperatureVeRa [iVeRaProfile] )
            radiadanceFactorsRatiosMedianPerOrbitCorrected.append ( radiadanceFactorsRatiosMedianPerOrbit [iVMCImage] )
            dRadiadanceFactorsRatiosMedianPerOrbitCorrected.append ( dradiadanceFactorsRatiosMedianPerOrbit [iVMCImage] )
            cloudTopAltitudes.append (cloudTopAltitude) 
            latitudes.append ( latitudesVeRa [iVeRaProfile] )    
  
    iVMCImages = np.asarray (iVMCImages) 
    iVeRaProfileForVMCImages = np.asarray (iVeRaProfileForVMCImages)
    thermalTideCorrection = np.asarray (thermalTideCorrection)
     
    # Create the plots for each of the cloud top altitudes.          
    if createFigures and len (iVMCImages):
    
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


        if fitAndPlot:
            
            fit = DataTools.linearLeastSquare ( cloudTopTemperatureVeRa [iVeRaProfileForVMCImages] - thermalTideCorrection, 
                                                radiadanceFactorsRatiosMedianPerOrbit [iVMCImages], 
                                                fractionBeyondXRange = 0.1 )
            
            print (cloudTopAltitude)
            print ('a = ', fit [0], fit [2])
            print ('b = ', fit [1], fit [3])
            print ('rSquared = ', fit [4])
            
            plt.plot ( fit [5], fit [6], c = 'black', alpha = 0.2,
                       label = 'RF = {:7.5f} ($\pm$ {:7.5f}) T + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], fit [1], fit [3], fit [4] ) )
            plt.legend ( loc = 'upper left', fontsize = 9 )

        plt.savefig ( '../plots/cloudTopTemperature_{:2d}km_vs_RadianceFactorRatio.png'.format (cloudTopAltitude) )



if createTable:


    tableFileName = os.path.abspath ('../cloudTopTemperature_vs_RadianceFactorRatio.dat')
    fileOpen = open (tableFileName, 'w')
    
    print (' ', file = fileOpen)
    print (' File: {}'.format (tableFileName), file = fileOpen)
    print (' Created at {}'.format ( HandyTools.getDateAndTimeString () ), file = fileOpen)
    
    
    print (' ', file = fileOpen)
    print (' T_cloudtop_corr = cloud top temperature corrected = T_cloud_uncorr + dT/dz_correction - T_tide_correction', file = fileOpen)
    print (' T_cloud_uncorr = cloud top temperature from VeRa uncorrected for any effects', file = fileOpen)
    print (' dT/dz_correction = cloud top temperature correction for the thermal gradient of -1K/km relative to the cloud top altitude of 71km.', file = fileOpen)
    print (' T_tide_correction = cloud top temperature correction for the thermal tide', file = fileOpen)
    print (' RFR = Radiance Factor Ratio median for the VMC image (from VMC Step03 - RadianceFactorRatiosPerOrbit.dat)', file = fileOpen)
    print (' z_cloudtop = cloud top altitude', file = fileOpen)
    print (' latitude = latitude of the VeRa sounding at 70km altitude', file = fileOpen)
    
    
    
    print (' ', file = fileOpen)
    print ('  T_cloud_corr   dT_cloud_corr   T_cloud_uncorr  dT/dz_correction  T_tide_correction    RFR     dRFR   z_cloudtop   latitude', file = fileOpen)
    print ('     (K)            (K)               (K)             (K)                (K)                             (km)          (˚)', file = fileOpen)
    print ('C_END', file = fileOpen)
        
    for iPoint in range ( len (cloudTopTemperatureVeRaCorrected) ):
        
        print ( '   {:8.5f}      {:8.5f}         {:8.5f}        {:4.1f}              {:8.5f}         {:5.3f}   {:6.4f}     {:2d}        {:7.2f}'.\
                format ( cloudTopTemperatureVeRaCorrected [iPoint], 
                         dcloudTopTemperatureVeRaCorrected [iPoint],
                         cloudTopTemperatureVeRaUnCorrected [iPoint],
                         cloudTopTemperatureGradientCorrection [iPoint],
                         cloudTopTemperatureThermalTideCorrection [iPoint],
                         radiadanceFactorsRatiosMedianPerOrbitCorrected [iPoint],
                         dRadiadanceFactorsRatiosMedianPerOrbitCorrected [iPoint],
                         cloudTopAltitudes [iPoint],
                         latitudes [iPoint] ), file = fileOpen )    

    fileOpen.close ()    



# Finally plot the corrected (thermal tide and temperature gradient variation) cloud top temperatures vs radiance factor ratios.
if createFigures:
    
    plt.figure (iPlot + 1)
    plt.clf ()
    
    plt.scatter ( cloudTopTemperatureVeRaCorrected, radiadanceFactorsRatiosMedianPerOrbitCorrected )
    plt.xlim (195,240)
    plt.ylim (0.6, 1.5)
    
    plt.title ( 'Corrected cloud top temperature' )
    plt.xlabel ( 'Cloud top temperature corrected to 71km (VeRa)'.format (cloudTopAltitude) )
    plt.ylabel ( 'Radiance Factor Ratio (VMC)')
    
    
    HandyTools.plotErrorBars ( cloudTopTemperatureVeRaCorrected, radiadanceFactorsRatiosMedianPerOrbitCorrected, 
                               xErrors = dcloudTopTemperatureVeRaCorrected,
                               yErrors = dRadiadanceFactorsRatiosMedianPerOrbitCorrected, colours = 'blue' )


    if fitAndPlot:
        
        fit = DataTools.linearLeastSquare (cloudTopTemperatureVeRaCorrected, radiadanceFactorsRatiosMedianPerOrbitCorrected, fractionBeyondXRange = 0.1)
        
        
        plt.plot ( fit [5], fit [6], c = 'black', alpha = 0.2, 
                   label = 'RF = {:7.5f} ($\pm$ {:7.5f}) T + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], fit [1], fit [3], fit [4] ) )
        plt.legend ( loc = 'upper left', fontsize = 9 )
    
    
    plt.savefig ( '../plots/cloudTopTemperatureCorrected_vs_RadianceFactorRatio.png' )
    plt.close (iPlot + 1)




























