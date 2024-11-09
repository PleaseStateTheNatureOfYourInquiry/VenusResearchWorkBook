# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241023

# Create plots of the cloud top temperatures from the VeRa derived temperature profiles and the results from Marcq et al. 2020 
#  (Climatology of SO2 and UV absorber at Venus' cloud top from SPICAV-UV T nadir dataset. Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002)) 
#  as a function of latitude, as well as the VMC-derived UV radiance factors as a function of latitude.


# Set which plots to produce.
plotToProduce = { 'Temperature vs latitude': True,
                  'Radiance Factor Ratios vs latitude': True }


# Chose the desired limitation in orbitIDs.

# orbitIDLimit = [0, 'All orbits']
orbitIDLimit = [1188, 'Radiance Factor Ratios vs Latitude']


# Standard imports.
import os
import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('..') ) 
from analysisConfiguration import *


def analyseCorrelation (X, Y):

    linearFit = DataTools.linearLeastSquare (X, Y)
    
    pearsonStatistics = stats.pearsonr (X, Y)
    spearmanStatistics = stats.spearmanr (X, Y)

    return linearFit, spearmanStatistics, pearsonStatistics



# Load the content of the  RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat  table, that contains the RFR and the temperatures between 50 and 80km altitude.
RFRvsTemperature = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat') )

orbitIDs = np.asarray ( RFRvsTemperature [0][0] )
latitudesPerOrbit = np.asarray ( RFRvsTemperature [0][4] )

iValidOrbits = np.where ( orbitIDs >= orbitIDLimit [0] )[0]

altitudesToPlot = [60, 69, 80]
iColumnAltitudeToPlot = [ 5 + (altitudeToPlot - 50) * 2   for altitudeToPlot in altitudesToPlot ]

altitudesToAnalyse = [ 50 + i  for i in range (31) ]
iColumnAltitudeToAnalyse = [ 5 + (altitudeToAnalyse - 50) * 2   for altitudeToAnalyse in altitudesToAnalyse ]

linearFits = []
spearmanStatistics = []
dSpearmanStatistics = []
pearsonStatistics = []
dPearsonStatistics = []
for iAltitude in range (31):

    spearmanStatisticPermutations = []
    pearsonStatisticPermutations = []
    for iPermutation in range (1000):
    
        temperaturesAtLatitudePermutation = \
         DataTools.getDataValuesWithGaussianNoise ( 
          RFRvsTemperature [0][ iColumnAltitudeToAnalyse [iAltitude] ][iValidOrbits], 
          DataTools.getNanFreeNumpyArray ( RFRvsTemperature [0][ iColumnAltitudeToAnalyse [iAltitude] + 1 ][iValidOrbits], replaceWithValue = True ) )

        linearFit, spearmanStatistic, pearsonStatistic = \
         analyseCorrelation ( latitudesPerOrbit [iValidOrbits], temperaturesAtLatitudePermutation )
       
        spearmanStatisticPermutations.append (spearmanStatistic.statistic)
        pearsonStatisticPermutations.append (pearsonStatistic.statistic)
    

    
    linearFit, spearmanStatistic, pearsonStatistic = \
     analyseCorrelation ( latitudesPerOrbit [iValidOrbits], RFRvsTemperature [0][ iColumnAltitudeToAnalyse [iAltitude] ][iValidOrbits] )

    linearFits.append (linearFit)

    spearmanStatistics.append (spearmanStatistic.statistic)
    spearmanStatisticsAverage, spearmanStatisticsStandardDeviation, spearmanStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (pearsonStatisticPermutations)
    dSpearmanStatistics.append (spearmanStatisticsStandardDeviation)
    print (iAltitude)
    print (spearmanStatistics [-1], spearmanStatisticsAverage, dSpearmanStatistics [-1])

    pearsonStatistics.append (pearsonStatistic.statistic)
    pearsonStatisticsAverage, pearsonStatisticsStandardDeviation, pearsonStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (spearmanStatisticPermutations)
    dPearsonStatistics.append (pearsonStatisticsStandardDeviation) 
    print (pearsonStatistics [-1], pearsonStatisticsAverage, dPearsonStatistics [-1])


plt.clf ()
plt.title ('Pearman Correlation Coefficient T(z) vs latitude')
plt.scatter (altitudesToAnalyse, pearsonStatistics)
HandyTools.plotErrorBars (altitudesToAnalyse, pearsonStatistics, yErrors = dPearsonStatistics)
plt.ylim (-1.05, 1.05)

plt.xlabel ('Altitude (km)')
plt.ylabel ('Pearman Correlation Coefficient')

plt.savefig ('Figure8d.png')
plt.close ()


# Produce the plots chosen at the top of this script.
if plotToProduce ['Temperature vs latitude']:

    # Determine the linear fit parameters to the cloud top temperature versus latitude, whatever it could mean!
#     fit = DataTools.linearLeastSquare (latitudesVeRa, cloudTopTemperatureVeRa, fractionBeyondXRange = 0.1)
    
    plt.clf ()
     
    numberOfSubPlotRows = 3
    numberOfSubPlotColumns = 1
    scale = 3
    fig, subPlotAxis = plt.subplots ( numberOfSubPlotRows, numberOfSubPlotColumns, 
                                      figsize = (6, 10) )  
    plt.subplots_adjust( bottom = 0.1,  top = 0.9, left = 0.15, right = 0.95, wspace = 0.3, hspace = 0.3 ) 

    for iPlot in range ( len (altitudesToPlot) ):
        
        iFit = altitudesToPlot [iPlot] - 50
        colour = 'tab:blue'
        subPlotAxis [iPlot].set_title ( 'T_{} = {:5.2f} * lat + {:5.2f} ($r^2$ = {:5.3f})'.format ( altitudesToPlot [iPlot], 
                                                                                                    linearFits [iFit][0], 
                                                                                                    linearFits [iFit][1], 
                                                                                                    linearFits [iFit][4] ) )

        if iPlot == len (altitudesToPlot) - 1:
        
            subPlotAxis [iPlot].set_xlabel ( 'latitude (˚)' )


        subPlotAxis [iPlot].set_xlim (-95,0)
        subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
        subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
        
        subPlotAxis [iPlot].set_ylabel ('Temperature (K) (VeRa)', color = colour)
        
        subPlotAxis [iPlot].scatter ( latitudesPerOrbit [iValidOrbits],
                                      RFRvsTemperature [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], c = 'blue', s = 25)
        
        subPlotAxis [iPlot].tick_params (axis='y', labelcolor = colour)
        
        
        HandyTools.plotErrorBars ( latitudesPerOrbit [iValidOrbits],
                                   RFRvsTemperature [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], 
                                   yErrors = RFRvsTemperature [0][ iColumnAltitudeToPlot [iPlot] + 1 ][iValidOrbits],
                                   colours = 'blue',
                                   axis = subPlotAxis [iPlot] )
        
        subPlotAxis [iPlot].plot ( linearFits [iFit][5], linearFits [iFit][6], c = 'black', alpha = 0.2, 
                                   label = 'T = {:5.2f} * lat + {:5.2f} ($r^2$ = {:5.3f})'.format ( linearFits [iFit][0], linearFits [iFit][1], linearFits [iFit][4] ) )
#         subPlotAxis [iPlot].legend (loc = 'lower right', fontsize = 8)


    plt.savefig ('Figure08.png')
    
    plt.close ()



if plotToProduce ['Radiance Factor Ratios vs latitude']:



    radiadanceFactorRatiosPerOrbitAverage = np.asarray ( RFRvsTemperature [0][1] )
    dradiadanceFactorRatiosPerOrbitAverage = np.asarray ( RFRvsTemperature [0][2] )

    plt.clf ()
    
    fig, ax1 = plt.subplots ()


    colour = 'tab:blue'
    ax1.set_title ( '{} ({} points)'.format ( orbitIDLimit [1], len (iValidOrbits) ) )
    ax1.set_xlabel ( 'Latitude (˚)' )
    ax1.set_xlim (-95,0)
    ax1.set_ylim (0.6, 1.5)
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    ax1.set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    ax1.set_ylabel ('Average Radiance Factor Ratio per VMC Orbit', color = colour)
    ax1.scatter (latitudesPerOrbit [iValidOrbits], radiadanceFactorRatiosPerOrbitAverage [iValidOrbits], c = 'blue', s = 25)
    ax1.tick_params (axis='y', labelcolor = colour)

    HandyTools.plotErrorBars (latitudesPerOrbit [iValidOrbits], radiadanceFactorRatiosPerOrbitAverage [iValidOrbits], yErrors = dradiadanceFactorRatiosPerOrbitAverage [iValidOrbits], colours = 'blue')


    ax1.vlines (x = -90, ymin = 0.6, ymax = 1.5, color = 'green')
    ax1.vlines (x = -60, ymin = 0.6, ymax = 1.5, color = 'green')
    ax1.vlines (x = -40, ymin = 0.6, ymax = 1.5, color = 'green')

    
    plt.savefig ( 'Figure07_radianceFactorsRatiosAverageVMCPerOrbit_orbitLimit_{}.png'.format ( orbitIDLimit [0] ) )
    
    plt.close ()

    
    
    
    




