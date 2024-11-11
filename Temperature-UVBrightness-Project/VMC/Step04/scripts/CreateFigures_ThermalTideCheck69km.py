# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241111

# Take the thermal tide at 69km altitude  ThermalTideCorrection.dat (Step04) and the RFR - Temperature also at 69km altitude 
#  from  RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat  in Step06.
# Apply the thermal tide correction and see the effect on the Pearson and Spearman Correlation Coefficients.

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

from VeRaTools import VeRaTools
from VMCTools import VMCTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


def analyseCorrelation (Temperatures, RFRs):
    
    pearsonStatistics = stats.pearsonr (Temperatures, RFRs)
    spearmanStatistics = stats.spearmanr (Temperatures, RFRs)

    return pearsonStatistics, spearmanStatistics


# Load the RFR - Temperature table.
RFRvsTemperature = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat') )

orbitIDs = RFRvsTemperature [0][0]
RFRs = RFRvsTemperature [0][1]
dRFRs = RFRvsTemperature [0][2]
latitudes = RFRvsTemperature [0][4]

Temperatures = RFRvsTemperature [0][43]
dTemperatures = RFRvsTemperature [0][44]


# Load the thermal tide amplitude table for 69km altitude.
thermalTideCorrection = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step04', 'ThermalTideCorrection.dat') )

# Take orbits with ID >= validOrbitID
validOrbitID = 1188
latitudesRanges = [[-90, -60], [-60, -40], [-40, 0]]
statisticTableFiles = [ 'T_Correlation_Latitudes_-83.8_-62.06.dat', 
                        'T_Correlation_Latitudes_-59.14_-43.12.dat',
                        'T_Correlation_Latitudes_-39.69_-14.97.dat' ]


for iLatitudeRange, latitudeRange in enumerate (latitudesRanges):

    iValidLatitudes = np.where ( np.logical_and ( latitudes > latitudeRange [0], latitudes <= latitudeRange [1] ) )[0]
    iValidOrbits = np.where ( orbitIDs [iValidLatitudes] >= validOrbitID )[0]
    iValidPoints = iValidLatitudes [iValidOrbits]
    
    TemperaturesCorrected = []
    dTemperaturesCorrected = []
           
    for iValidPoint in iValidPoints:
    
        iLine = 0
        while thermalTideCorrection[0][0][iLine] != orbitIDs [iValidPoint]:
        
            iLine += 1 
        
        TemperaturesCorrected.append ( Temperatures [iValidPoint] - thermalTideCorrection[0][5][iLine] )


    plt.figure (iLatitudeRange)
    plt.clf ()


    # Plot the uncorrected T vs RFR.
    pearsonStatistics = stats.pearsonr ( Temperatures [iValidPoints], RFRs [iValidPoints] )
    spearmanStatistics = stats.spearmanr ( Temperatures [iValidPoints], RFRs [iValidPoints] )

    statisticUncorrected = HandyTools.readTable ( os.path.join ( VMCWorkBookDirectory, 'Step06', statisticTableFiles [iLatitudeRange] ) ) 

    plt.scatter ( Temperatures [iValidPoints], RFRs [iValidPoints], color = 'blue', 
                  label = 'Pearson, Spearman corr. coeff. = {:6.3f} +/- {:7.4f}, {:6.3f} +/- {:7.4f}'.
                   format ( statisticUncorrected [0][1][19], statisticUncorrected [0][2][19],
                            statisticUncorrected [0][3][19], statisticUncorrected [0][4][19] ) )
    HandyTools.plotErrorBars ( Temperatures [iValidPoints], RFRs [iValidPoints], 
                               xErrors = dTemperatures [iValidPoints],
                               yErrors = dRFRs [iValidPoints], colours = 'blue' )



    # Plot the thermal tide corrected T vs RFR and calculate the Pearson and Spearman correlation coefficients and the estimate of their uncertainties.
    pearsonStatisticsPermutation = []
    spearmanStatisticsPermutation = []
    for iPermutation in range (1000):
    
        pearsonStatistics, spearmanStatistics = \
         analyseCorrelation ( DataTools.getDataValuesWithGaussianNoise ( TemperaturesCorrected, 
                                                                         DataTools.getNanFreeNumpyArray( dTemperatures [iValidPoints], replaceWithValue = True ) ), 
                              DataTools.getDataValuesWithGaussianNoise ( RFRs [iValidPoints], 
                                                                         DataTools.getNanFreeNumpyArray ( dRFRs [iValidPoints], replaceWithValue = True ) ) )

        pearsonStatisticsPermutation.append (pearsonStatistics.statistic)
        spearmanStatisticsPermutation.append (spearmanStatistics.statistic)

        
        pearsonStatisticsAverage, pearsonStatisticsStandardDeviation, pearsonStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (pearsonStatisticsPermutation)
        spearmanStatisticsAverage, spearmanStatisticsStandardDeviation, spearmanStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (spearmanStatisticsPermutation)

                
    pearsonStatistics, spearmanStatistics = analyseCorrelation ( TemperaturesCorrected, RFRs [iValidPoints] )
       
    plt.scatter ( TemperaturesCorrected, RFRs [iValidPoints], color = 'red',
                  label = 'Pearson, Spearman corr. coeff. = {:6.3f} +/- {:7.4f}, {:6.3f} +/- {:7.4f}'.
                   format ( pearsonStatistics.statistic, pearsonStatisticsStandardDeviation,
                            spearmanStatistics.statistic, spearmanStatisticsStandardDeviation ) )
    HandyTools.plotErrorBars ( TemperaturesCorrected, RFRs [iValidPoints], 
                               xErrors = dTemperatures [iValidPoints],
                               yErrors = dRFRs [iValidPoints], colours = 'red' )
    
    plt.legend (fontsize = 8)
    
    plt.title ( 'Latitudes between {:3d}˚ and {:3d}˚: Thermal tide correction (red)'.format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ) ) )
        
    plt.xlabel ('Temperature 69km (VeRa) (K)')
    plt.ylabel ('Radiance Factor Ratio (VMC)')

    plt.savefig ( os.path.join ( VMCWorkBookDirectory, 'Step04', 'plots', 
                                 'Temperature69km_vs_RadianceFactorRatio_latitudes_{}_{}'.format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ) ) ) )
       
    plt.close ()
     
