# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241112

# Create the plots of the variability of temperature with latitude at three altitudes and the spearman + pearson correlation coefficients 
#  as a function of altitude. Also creates the RFR versus latitude plot.


# Set which plots to produce.
plotToProduce = { 'Temperature vs latitude': False,
                  'Static stability vs latitude' : True,
                  'Radiance Factor Ratios vs latitude': False }


# Chose the desired limitation in orbitIDs.

orbitIDLimit = [1188, 'Radiance Factor Ratios vs Latitude']


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


# Load the content of the  RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat  table, that contains the RFR and the temperatures between 50 and 80km altitude.
RFRvsTemperature = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat') )
temperatureVSLatitudeStatistics = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'TVeRa_vs_latitude_statistics_50-80kmAltitude.dat') )

RFRvsStaticStability = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat') )
staticStabilityVSLatitudeStatistics = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'SVeRa_vs_latitude_statistics_50-80kmAltitude.dat') )




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

spearmanStatisticsStaticStability = []
dSpearmanStatisticstaticStability = []
pearsonStatisticstaticStability = []
dPearsonStatisticstaticStability = []



for iAltitude in range (31):

    linearFits.append ( DataTools.linearLeastSquare ( latitudesPerOrbit [iValidOrbits], RFRvsTemperature [0][ iColumnAltitudeToAnalyse [iAltitude] ][iValidOrbits] ) )

    pearsonStatistics.append ( temperatureVSLatitudeStatistics [0][6][iAltitude] )
    dPearsonStatistics.append ( temperatureVSLatitudeStatistics [0][7][iAltitude]) 

    spearmanStatistics.append (  temperatureVSLatitudeStatistics [0][8][iAltitude] )
    dSpearmanStatistics.append (  temperatureVSLatitudeStatistics [0][9][iAltitude] )
    
    
    pearsonStatisticstaticStability.append ( staticStabilityVSLatitudeStatistics [0][6][iAltitude] )
    dPearsonStatisticstaticStability.append ( staticStabilityVSLatitudeStatistics [0][7][iAltitude] )
    
    spearmanStatisticsStaticStability.append ( staticStabilityVSLatitudeStatistics [0][8][iAltitude] )
    dSpearmanStatisticstaticStability.append ( staticStabilityVSLatitudeStatistics [0][9][iAltitude] )





plt.clf ()
plt.title ('Spearman / Pearson Correlation Coefficient T(z) vs latitude')

plt.scatter (altitudesToAnalyse, spearmanStatistics, label = 'Spearman correlation coef.')
HandyTools.plotErrorBars (altitudesToAnalyse, spearmanStatistics, yErrors = dSpearmanStatistics)

plt.scatter (altitudesToAnalyse, pearsonStatistics, label = 'Pearson correlation coef.', color = 'red')
HandyTools.plotErrorBars (altitudesToAnalyse, pearsonStatistics, yErrors = dPearsonStatistics, colours = 'red')

plt.legend ()

plt.ylim (-1.05, 1.05)

plt.xlabel ('Altitude (km)')
plt.ylabel ('Spearman / Pearson Correlation Coefficient')

plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step06', 'plots', 'SpearmanPearsonCorrelationCoefficient_T_vs_latitude.png') )
plt.close ()



plt.clf ()
plt.title ('Spearman / Pearson Correlation Coefficient S(z) vs latitude')

plt.scatter (altitudesToAnalyse, spearmanStatisticsStaticStability, label = 'Spearman correlation coef.')
HandyTools.plotErrorBars (altitudesToAnalyse, spearmanStatisticsStaticStability, yErrors = dSpearmanStatisticstaticStability)

plt.scatter (altitudesToAnalyse, pearsonStatisticstaticStability, label = 'Pearson correlation coef.', color = 'red')
HandyTools.plotErrorBars (altitudesToAnalyse, pearsonStatisticstaticStability, yErrors = dPearsonStatisticstaticStability, colours = 'red')

plt.legend ()

plt.ylim (-1.05, 1.05)

plt.xlabel ('Altitude (km)')
plt.ylabel ('Spearman / Pearson Correlation Coefficient')

plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step06', 'plots', 'SpearmanPearsonCorrelationCoefficient_S_vs_latitude.png') )
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
        subPlotAxis [iPlot].set_title ( 'VeRa Temperature at {}km versus latitude'.format ( altitudesToPlot [iPlot] ) )

        if iPlot == len (altitudesToPlot) - 1:
        
            subPlotAxis [iPlot].set_xlabel ( 'latitude (˚)' )


        subPlotAxis [iPlot].set_xlim (-95,0)
        subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
        subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
        
        subPlotAxis [iPlot].set_ylabel ('Temperature (K)', color = colour)
        
        subPlotAxis [iPlot].scatter ( latitudesPerOrbit [iValidOrbits],
                                      RFRvsTemperature [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], c = 'blue', s = 25, 
                                      label = 'Spearman CC = {:5.2f} ± {:6.3f}'.format ( spearmanStatistics [altitudesToPlot [iPlot] - 50], 
                                                                                         dSpearmanStatistics [altitudesToPlot [iPlot] - 50] ) )
        
        subPlotAxis [iPlot].tick_params (axis='y', labelcolor = colour)
        
        
        HandyTools.plotErrorBars ( latitudesPerOrbit [iValidOrbits],
                                   RFRvsTemperature [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], 
                                   yErrors = RFRvsTemperature [0][ iColumnAltitudeToPlot [iPlot] + 1 ][iValidOrbits],
                                   colours = 'blue',
                                   axis = subPlotAxis [iPlot] )
        
#         subPlotAxis [iPlot].plot ( linearFits [iFit][5], linearFits [iFit][6], c = 'green', alpha = 0.3, 
#                                    label = 'T = {:5.2f} * latitude + {:5.2f}; Pearson Corr. Coeff = {:5.2f} ± {:6.3f}'.
#                                     format ( linearFits [iFit][0], linearFits [iFit][1], 
#                                              pearsonStatistics [ altitudesToPlot [iPlot] - 50 ], dPearsonStatistics [ altitudesToPlot [iPlot] - 50 ] ) )

        subPlotAxis [iPlot].legend (fontsize = 8)


    plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step06', 'plots', 'Temperature_vs_latitude_variability_examples.png') )
    
    plt.close ()


if plotToProduce ['Static stability vs latitude']:

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
        subPlotAxis [iPlot].set_title ( 'VeRa Static Stability at {}km versus latitude'.format ( altitudesToPlot [iPlot] ) )

        if iPlot == len (altitudesToPlot) - 1:
        
            subPlotAxis [iPlot].set_xlabel ( 'latitude (˚)' )


        subPlotAxis [iPlot].set_xlim (-95,0)
        subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
        subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
        
        subPlotAxis [iPlot].set_ylabel ('Static Stability (K/km)', color = colour)
        
        subPlotAxis [iPlot].scatter ( latitudesPerOrbit [iValidOrbits],
                                      RFRvsStaticStability [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], c = 'blue', s = 25, 
                                      label = 'Spearman CC = {:5.2f} ± {:6.3f}'.format ( spearmanStatisticsStaticStability [altitudesToPlot [iPlot] - 50], 
                                                                                         dSpearmanStatisticstaticStability [altitudesToPlot [iPlot] - 50] ) )
        
        subPlotAxis [iPlot].tick_params (axis='y', labelcolor = colour)
        
        
        HandyTools.plotErrorBars ( latitudesPerOrbit [iValidOrbits],
                                   RFRvsStaticStability [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], 
                                   yErrors = RFRvsStaticStability [0][ iColumnAltitudeToPlot [iPlot] + 1 ][iValidOrbits],
                                   colours = 'blue',
                                   axis = subPlotAxis [iPlot] )
        
#         subPlotAxis [iPlot].plot ( linearFits [iFit][5], linearFits [iFit][6], c = 'green', alpha = 0.3, 
#                                    label = 'T = {:5.2f} * latitude + {:5.2f}; Pearson Corr. Coeff = {:5.2f} ± {:6.3f}'.
#                                     format ( linearFits [iFit][0], linearFits [iFit][1], 
#                                              pearsonStatistics [ altitudesToPlot [iPlot] - 50 ], dPearsonStatistics [ altitudesToPlot [iPlot] - 50 ] ) )

        subPlotAxis [iPlot].legend (fontsize = 8)


    plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step06', 'plots', 'StaticStability_vs_latitude_variability_examples.jpg') )
    
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


    ax1.vlines (x = -90, ymin = 0.6, ymax = 1.5, color = 'green', alpha = 0.5)
    ax1.vlines (x = -60, ymin = 0.6, ymax = 1.5, color = 'green', alpha = 0.5)
    ax1.vlines (x = -40, ymin = 0.6, ymax = 1.5, color = 'green', alpha = 0.5)

    
    plt.savefig ( os.path.join (VMCWorkBookDirectory, 'Step06', 'plots', 'Radiance_vs_latitude_variability.png' ) )
    
    plt.close ()

    
    
    
    




