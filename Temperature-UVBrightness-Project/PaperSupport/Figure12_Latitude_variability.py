# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241112

# Create figure 12


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
sys.path.append ( os.path.abspath ('..') ) 
from analysisConfiguration import *


# Load the content of the  RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat  table, that contains the RFR and the temperatures between 50 and 80km altitude.
RFRvsStaticStability = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat') )
RVSvsStaticStabilityStatistics = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'SVeRa_vs_latitude_statistics_50-80kmAltitude.dat') )


orbitIDs = np.asarray ( RFRvsStaticStability [0][0] )
latitudesPerOrbit = np.asarray ( RFRvsStaticStability [0][4] )

iValidOrbits = np.where ( orbitIDs >= orbitIDLimit [0] )[0]

altitudesToPlot = [60, 69, 80]
iColumnAltitudeToPlot = [ 5 + (altitudeToPlot - 50) * 2   for altitudeToPlot in altitudesToPlot ]

altitudesToAnalyse = [ 50 + i  for i in range (31) ]
iColumnAltitudeToAnalyse = [ 5 + (altitudeToAnalyse - 50) * 2   for altitudeToAnalyse in altitudesToAnalyse ]

spearmanStatistics = []
dSpearmanStatistics = []
pearsonStatistics = []
dPearsonStatistics = []
for iAltitude in range (31):

    pearsonStatistics.append ( RVSvsStaticStabilityStatistics [0][6][iAltitude] )
    dPearsonStatistics.append ( RVSvsStaticStabilityStatistics [0][7][iAltitude]) 

    spearmanStatistics.append (  RVSvsStaticStabilityStatistics [0][8][iAltitude] )
    dSpearmanStatistics.append (  RVSvsStaticStabilityStatistics [0][9][iAltitude] )




plt.clf ()
plt.title ('Spearman Correlation Coefficient S(z) vs latitude')
plt.scatter (altitudesToAnalyse, spearmanStatistics)
HandyTools.plotErrorBars (altitudesToAnalyse, spearmanStatistics, yErrors = dSpearmanStatistics)
plt.ylim (-1.05, 1.05)

plt.xlabel ('Altitude (km)')
plt.ylabel ('Spearman Correlation Coefficient')

plt.savefig ('Figure12d.png')
plt.close ()



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
    subPlotAxis [iPlot].set_title ( 'Static Stability at {}km versus latitude'.format ( altitudesToPlot [iPlot] ) )

    if iPlot == len (altitudesToPlot) - 1:
    
        subPlotAxis [iPlot].set_xlabel ( 'latitude (˚)' )


    subPlotAxis [iPlot].set_xlim (-95,0)
    subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 10)] )
    subPlotAxis [iPlot].set_xticks ( ticks = [tick  for tick in range (-90, 0, 5)], minor = True )
    
    subPlotAxis [iPlot].set_ylabel ('S (K/km)', color = colour)
    
    subPlotAxis [iPlot].scatter ( latitudesPerOrbit [iValidOrbits],
                                  RFRvsStaticStability [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], c = 'blue', s = 25, 
                                  label = 'Spearman CC = {:5.2f} ± {:6.3f}'.format ( spearmanStatistics [altitudesToPlot [iPlot] - 50], 
                                                                                     dSpearmanStatistics [altitudesToPlot [iPlot] - 50] ) )
    
    subPlotAxis [iPlot].tick_params (axis='y', labelcolor = colour)
    
    
    HandyTools.plotErrorBars ( latitudesPerOrbit [iValidOrbits],
                               RFRvsStaticStability [0][ iColumnAltitudeToPlot [iPlot] ][iValidOrbits], 
                               yErrors = RFRvsStaticStability [0][ iColumnAltitudeToPlot [iPlot] + 1 ][iValidOrbits],
                               colours = 'blue',
                               axis = subPlotAxis [iPlot] )
    

    subPlotAxis [iPlot].legend (fontsize = 8)


plt.savefig ('Figure12.png')

plt.close ()


    
    
    
    




