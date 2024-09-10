# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240908

# Create plots of the cloud top temperatures from the VeRa derived temperature profiles and the results from Marcq et al. 2020 
#  (Climatology of SO2 and UV absorber at Venus' cloud top from SPICAV-UV T nadir dataset. Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002)) 
#  as a function of latitude, as well as the VMC-derived UV radiance factors as a function of latitude.


# Set which plots to produce.
plotToProduce = { 'Cloud top temperature vs latitude': False,
                  'Cloud top temperature gradient vs latitude' : True,
                  'Radiance factors vs latitude': False }


# Chose the desired limitation in orbitIDs.

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
tableContent = HandyTools.readTable ('../VMCSelectedImages_CloudTopAltitudes.dat')
numberOfImages = len ( tableContent[0][0] )


# Go through the table and extract the latitudes and radiance factors per orbit by taking the median values for all the images in each orbit.
iLine = 0
orbitIDs = []
latitudesPerOrbit = []
radiadanceFactorsPerOrbit = []
radiadanceFactorsUncertaintiesPerOrbit  = []
while iLine < numberOfImages:

    orbitIDs.append ( tableContent[0][0][iLine] )
    latitudesInOrbit = []
    radiadanceFactorsInOrbit = []
    radiadanceFactorsUncertaintiesInOrbit = []
    while iLine < numberOfImages and tableContent[0][0][iLine] == orbitIDs [-1]:

        latitudesInOrbit.append ( tableContent[0][8][iLine] )
        radiadanceFactorsInOrbit.append ( tableContent[0][16][iLine] )
        radiadanceFactorsUncertaintiesInOrbit.append ( tableContent[0][17][iLine] )
        iLine += 1

    latitudesPerOrbit.append ( DataTools.getMedianAndQuantilesPYtoCPP (latitudesInOrbit)[0] )
    radianceFactorsMedian = DataTools.getMedianAndQuantilesPYtoCPP (radiadanceFactorsInOrbit, uncertainties = radiadanceFactorsUncertaintiesInOrbit)
    radiadanceFactorsPerOrbit.append ( radianceFactorsMedian [0] )
    radiadanceFactorsUncertaintiesPerOrbit.append ( radianceFactorsMedian [-1] )

orbitIDs  = np.asarray (orbitIDs)
latitudesPerOrbit = np.asarray (latitudesPerOrbit)
radiadanceFactorsPerOrbit = np.asarray (radiadanceFactorsPerOrbit)
radiadanceFactorsUncertaintiesPerOrbit = np.asarray (radiadanceFactorsUncertaintiesPerOrbit)


# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020.
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

cloudTopTemperatureGradientVeRa = []
dCloudTopTemperatureGradientVeRa = []

cloudTopTemperatureGradientVeRaAverage = []
dCloudTopTemperatureGradientVeRaAverage = []

cloudTopTemperatureGradientVeRaMedian = []
dCloudTopTemperatureGradientVeRaMedian = []

for profileSet in profileSets:

    iLatitudeLevel = int ( radiusOfVenus + latitudeLevel - profileSet ['FilteredProfiles'][0][0][0] )

    # This list will be used to extract the temperature lapse rates in the region where all the cloud tops fall: 65 - 74km.
    #  I use it to calculate an average temperature lapse rate, as compared to the lapse rate at the cloud top level.
    iLatitudeLevels = np.asarray ( [ int ( radiusOfVenus + latitudeLevel - profileSet ['FilteredProfiles'][0][0][0] )  for latitudeLevel in range (65,75) ] )
    
    for iProfile in range ( len ( profileSet ['OrbitID'] ) ):
    
        if int ( profileSet ['OrbitID'][iProfile].split ('_')[0] ) >= orbitIDLimit [0]:
                
            profileVeRa = profileSet ['FilteredProfiles'][iProfile]
            
            latitudesVeRa.append ( profileVeRa [5][iLatitudeLevel] )
        
        
            # Determine the index in the  Marcq_2020_Figure14.dat  table that corresponds to the VeRa latitude.
            #  tableContent [0][6] is the latitude of the VeRa profile.    
            iCloudTopBin = 9 - abs ( int ( latitudesVeRa [-1] / 10 ) ) - 1
            altitudesCloudTop.append ( int ( figure14Data [0][2][iCloudTopBin] + 0.5 ) )
            
            # Determine the index in the filtered VeRa temperature profile that corresponds to the cloud top altitude.
            iAltitudeCloudTopInVeRaProfile = ( radiusOfVenus + altitudesCloudTop [-1] ) - int ( profileVeRa [0][0] )

            # Store the cloud top temperature and its uncertainty.            
            cloudTopTemperatureVeRa.append ( profileVeRa [1][iAltitudeCloudTopInVeRaProfile] )
            dCloudTopTemperatureVeRa.append ( profileVeRa [2][iAltitudeCloudTopInVeRaProfile] )
            
            
            # Store the cloud top temperature lapse rate and its uncertainty.
            cloudTopTemperatureGradientVeRa.append ( profileVeRa [7][iAltitudeCloudTopInVeRaProfile] )
            dCloudTopTemperatureGradientVeRa.append ( profileVeRa [8][iAltitudeCloudTopInVeRaProfile] )


            # Calculate and store the average temperature lapse rate and its uncertainty in the 65 - 74km altitude range.
            averageTemperatureGradientPerProfile = DataTools.getAverageVarAndSDPYtoCPP ( DataTools.getNanFreeNumpyArray (profileVeRa [7][iLatitudeLevels]) )
            cloudTopTemperatureGradientVeRaAverage.append ( averageTemperatureGradientPerProfile [0] )
           
            cloudTopTemperatureGradientVeRaUncertainties = DataTools.getNanFreeNumpyArray (profileVeRa [8][iLatitudeLevels])
            dCloudTopTemperatureGradientVeRaAverage.append ( 
             max ( np.sum ( cloudTopTemperatureGradientVeRaUncertainties ** 2 ) / len (cloudTopTemperatureGradientVeRaUncertainties), 
                   averageTemperatureGradientPerProfile [1] ) )


            # Calculate and store the median temperature lapse rate and its uncertainty in the 65 - 74km altitude range.
            medianTemperatureGradientPerProfile = DataTools.getMedianAndQuantilesPYtoCPP ( 
             DataTools.getNanFreeNumpyArray ( profileVeRa [7][iLatitudeLevels] ), lowerQuantilePercentage = 33, upperQuantilePercentage = 67,
             uncertainties = DataTools.getNanFreeNumpyArray ( profileVeRa [8][iLatitudeLevels] ) )
            
            cloudTopTemperatureGradientVeRaMedian.append ( medianTemperatureGradientPerProfile [0] ) 
            errorBars = max ( medianTemperatureGradientPerProfile [2] - medianTemperatureGradientPerProfile [0], 
                              medianTemperatureGradientPerProfile [0] - medianTemperatureGradientPerProfile [1] )
            dCloudTopTemperatureGradientVeRaMedian.append ( max (medianTemperatureGradientPerProfile [3], errorBars) )


# Produce the plots chosen at the top of this script.
if plotToProduce ['Cloud top temperature vs latitude']:

    # Determine the linear fit parameters to the cloud top temperature versus latitude, whatever it could mean!
    fit = DataTools.linearLeastSquare (latitudesVeRa, cloudTopTemperatureVeRa, fractionBeyondXRange = 0.1)
    
    plt.clf ()
    
    fig, ax1 = plt.subplots ()
    
    colour = 'tab:blue'
    ax1.set_title ( '{} (# of point {})'.format (orbitIDLimit [1], len (latitudesVeRa)) )
    ax1.set_xlabel ( 'latitude (˚)' )
    ax1.set_xlim (-95,0)
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    ax1.set_ylabel ('Cloud top temperature (K) (VeRa)', color = colour)
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
    
    plt.savefig ( '../plots/cloudTopTemperatureVeRa_orbitLimit_{}.png'.format ( orbitIDLimit [0] ) )
    
    plt.close (1)
    plt.close (2)


if plotToProduce ['Cloud top temperature gradient vs latitude']:

    # From  DataTools.QQPlot ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRa) ) I see that the  values of  cloudTopTemperatureGradientVeRa  are
    #  distributed in a Gaussian way, so that taking the average is a valid approach.
    
    
    averageTemperatureGradient = DataTools.getAverageVarAndSDPYtoCPP ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRa) )
    medianTemperatureGradient = DataTools.getMedianAndQuantilesPYtoCPP ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRa), 
                                                                          uncertainties = DataTools.getNanFreeNumpyArray (dCloudTopTemperatureGradientVeRa) )

    plt.clf () 
    
    fig, ax1 = plt.subplots ()
    
    colour = 'tab:blue'
    ax1.set_title ( '{} (# of point {})'.format (orbitIDLimit [1], len (latitudesVeRa)) )
    ax1.set_xlabel ( 'latitude (˚)' )
    ax1.set_xlim (-95,0)
    ax1.set_ylim (-11,20)
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    ax1.set_ylabel ('Cloud top dT/dz (K/km) (VeRa)', color = colour)

    ax1.scatter (latitudesVeRa, cloudTopTemperatureGradientVeRa, c = 'blue', s = 25)
    HandyTools.plotErrorBars (latitudesVeRa, cloudTopTemperatureGradientVeRa, yErrors = dCloudTopTemperatureGradientVeRa, colours = 'blue')
    
    ax1.tick_params (axis='y', labelcolor = colour)

    ax1.text (-50, 13, 'Average: {:5.2f} +/- {:5.2f} K/km'.format (averageTemperatureGradient [0], averageTemperatureGradient [1]), c = 'blue', fontsize = 10 )
    ax1.text (-50, 11, 'Median: {:5.2f} +/- {:5.2f} K/km'.format (medianTemperatureGradient [0], medianTemperatureGradient [3]), c = 'blue', fontsize = 10 )
    
    # instantiate a second Axes that shares the same x-axis
    ax2 = ax1.twinx ()  
    
    colour = 'tab:green'
    ax2.set_ylabel ('altitude cloud top (km)', color = colour)
    ax2.scatter (latitudesVeRa, altitudesCloudTop, color = 'lightgreen', marker = 'D', s = 10)
    ax2.tick_params (axis='y', labelcolor = colour)
    
    plt.savefig ( '../plots/temperatureGradientVeRa_CloudTops_orbitLimit_{}.png'.format ( orbitIDLimit [0] ) )
    
    plt.close (1)
    plt.close (2)



    # The average lapse rates in the 65 - 74 km altitude range
    averageTemperatureGradient = DataTools.getAverageVarAndSDPYtoCPP ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRaAverage) )
    medianTemperatureGradient = DataTools.getMedianAndQuantilesPYtoCPP ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRaAverage), 
                                                                          uncertainties = DataTools.getNanFreeNumpyArray (dCloudTopTemperatureGradientVeRaAverage) )

    plt.clf () 
    
    fig, ax1 = plt.subplots ()
    
    colour = 'tab:blue'
    ax1.set_title ( '{} (# of point {})'.format (orbitIDLimit [1], len (latitudesVeRa)) )
    ax1.set_xlabel ( 'latitude (˚)' )
    ax1.set_xlim (-95,0)
    ax1.set_ylim (-11,20)
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    ax1.set_ylabel ('Average dT/dz 65-74km (K/km) (VeRa)', color = colour)

    ax1.scatter (latitudesVeRa, cloudTopTemperatureGradientVeRaAverage, c = 'blue', s = 25)
    HandyTools.plotErrorBars (latitudesVeRa, cloudTopTemperatureGradientVeRaAverage, yErrors = dCloudTopTemperatureGradientVeRaAverage, colours = 'blue')
    
    ax1.tick_params (axis='y', labelcolor = colour)
    

    ax1.text (-50, 13, 'Average: {:5.2f} +/- {:5.2f} K/km'.format (averageTemperatureGradient [0], averageTemperatureGradient [1]), c = 'blue', fontsize = 10 )
    ax1.text (-50, 11, 'Median: {:5.2f} +/- {:5.2f} K/km'.format (medianTemperatureGradient [0], medianTemperatureGradient [3]), c = 'blue', fontsize = 10 )

    
    # instantiate a second Axes that shares the same x-axis
    ax2 = ax1.twinx ()  
    
    colour = 'tab:green'
    ax2.set_ylabel ('altitude cloud top (km)', color = colour)
    ax2.scatter (latitudesVeRa, altitudesCloudTop, color = 'lightgreen', marker = 'D', s = 10)
    ax2.tick_params (axis='y', labelcolor = colour)
    
    plt.savefig ( '../plots/temperatureGradientVeRa_Average65-74km_orbitLimit_{}.png'.format ( orbitIDLimit [0] ) )
    
    plt.close (1)
    plt.close (2)



    # The median lapse rates in the 65 - 74 km altitude range
    averageTemperatureGradient = DataTools.getAverageVarAndSDPYtoCPP ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRaMedian) )
    medianTemperatureGradient = DataTools.getMedianAndQuantilesPYtoCPP ( DataTools.getNanFreeNumpyArray (cloudTopTemperatureGradientVeRaMedian), 
                                                                          uncertainties = DataTools.getNanFreeNumpyArray (dCloudTopTemperatureGradientVeRaMedian) )

    plt.clf () 
    
    fig, ax1 = plt.subplots ()
    
    colour = 'tab:blue'
    ax1.set_title ( '{} (# of point {})'.format (orbitIDLimit [1], len (latitudesVeRa)) )
    ax1.set_xlabel ( 'latitude (˚)' )
    ax1.set_xlim (-95,0)
    ax1.set_ylim (-11,20)
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    ax1.set_ylabel ('Median dT/dz 65-74km (K/km) (VeRa)', color = colour)

    ax1.scatter (latitudesVeRa, cloudTopTemperatureGradientVeRaMedian, c = 'blue', s = 25)
    HandyTools.plotErrorBars (latitudesVeRa, cloudTopTemperatureGradientVeRaMedian, yErrors = dCloudTopTemperatureGradientVeRaMedian, colours = 'blue')
    
    ax1.tick_params (axis='y', labelcolor = colour)
    

    ax1.text (-50, 13, 'Average: {:5.2f} +/- {:5.2f} K/km'.format (averageTemperatureGradient [0], averageTemperatureGradient [1]), c = 'blue', fontsize = 10 )
    ax1.text (-50, 11, 'Median: {:5.2f} +/- {:5.2f} K/km'.format (medianTemperatureGradient [0], medianTemperatureGradient [3]), c = 'blue', fontsize = 10 )

    
    # instantiate a second Axes that shares the same x-axis
    ax2 = ax1.twinx ()  
    
    colour = 'tab:green'
    ax2.set_ylabel ('altitude cloud top (km)', color = colour)
    ax2.scatter (latitudesVeRa, altitudesCloudTop, color = 'lightgreen', marker = 'D', s = 10)
    ax2.tick_params (axis='y', labelcolor = colour)
    
    plt.savefig ( '../plots/temperatureGradientVeRa_Median65-74km_orbitLimit_{}.png'.format ( orbitIDLimit [0] ) )
    
    plt.close (1)
    plt.close (2)



if plotToProduce ['Radiance factors vs latitude']:


    plt.clf ()
    
    fig, ax1 = plt.subplots ()
    
    iValidOrbits = np.where ( orbitIDs >= orbitIDLimit [0] )[0]
    
    
    colour = 'tab:blue'
    ax1.set_title ( '{} (# of point {})'.format ( orbitIDLimit [1], len (iValidOrbits) ) )
    ax1.set_xlabel ( 'latitude (˚)' )
    ax1.set_xlim (-95,0)
    ax1.set_ylim (0.4, 1.1)
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    ax1.set_ylabel ('Median Radiance Factors per VMC Orbit', color = colour)
    ax1.scatter (latitudesPerOrbit [iValidOrbits], radiadanceFactorsPerOrbit [iValidOrbits], c = 'blue', s = 25)
    ax1.tick_params (axis='y', labelcolor = colour)

    HandyTools.plotErrorBars (latitudesPerOrbit [iValidOrbits], radiadanceFactorsPerOrbit [iValidOrbits], yErrors = radiadanceFactorsUncertaintiesPerOrbit [iValidOrbits], colours = 'blue')

    
    # instantiate a second Axes that shares the same x-axis
    ax2 = ax1.twinx ()  
    
    colour = 'tab:green'
    ax2.set_ylabel ('altitude cloud top (km)', color = colour)
    ax2.scatter (latitudesVeRa, altitudesCloudTop, color = 'lightgreen', marker = 'D', s = 10)
    ax2.tick_params (axis='y', labelcolor = colour)
    
    plt.savefig ( '../plots/radianceFactorsVMCPerOrbit_orbitLimit_{}.png'.format ( orbitIDLimit [0] ) )
    
    plt.close (1)
    plt.close (2)
    




