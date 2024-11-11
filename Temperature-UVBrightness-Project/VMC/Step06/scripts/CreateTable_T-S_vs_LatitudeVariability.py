# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241107

# Calculate the Pearson and Spearman correlation coefficients for the relation the Radiance Factor Ratio and the
#  temperature  (RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat)  or static stability  (RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat)
#  for each of the 31 altitude levels between 50 and 80km.


# Chose the desired limitation in orbitIDs.

# orbitIDLimit = [0, 'All orbits']
orbitIDLimit = [1188, 'Radiance Factor Ratios vs Latitude']

# tableType = 'temperature'
tableType = 'staticStability'



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
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *



def analyseCorrelation (X, Y):

    linearFit = DataTools.linearLeastSquare (X, Y)
    
    pearsonStatistics = stats.pearsonr (X, Y)
    spearmanStatistics = stats.spearmanr (X, Y)

    return linearFit, pearsonStatistics, spearmanStatistics


numberOfPermutations = 1000

# Load the content of the  RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat  or  the  RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat  table, 
#  that contains the RFR and the temperatures or static stability  between 50 and 80km altitude and perform the statistical analysis.


if tableType == 'temperature':

    RFRvsTorS = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat') )

    tableFileName = os.path.join (VMCWorkBookDirectory, 'Step06', 'TVeRa_vs_latitude_statistics_50-80kmAltitude.dat') 
    headerLines = [
    '',
    ' T (latitude) = latitude * a + b (latitude range between -90˚ and 0˚)',
    ' r^2 = goodness of fit (0,1) as defined by: sum ( (y - (a * x + b)) ** 2 )  / sum ( (y - dataAverage) ** 2 ), with dataAverage = np.sum (y) / N ',
    ' Pearson Coef. = Pearson correlation coefficient (-1,+1)',
    ' dPearson Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
    ' Spearman Coef. = Spearman R correlation coefficient (-1,+1)',
    ' dSpearman Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
    '',
    ' Altitude   a      da        b      db     r^2   Pearson Coef  dPearson Coef   Spearman Coef  dSpearman Coef',
    '   (km)   (K/˚)  (K/˚)     (K/˚)   (K/˚)'
    ]



if tableType == 'staticStability':

    RFRvsTorS = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat') )
    tableFileName = os.path.join (VMCWorkBookDirectory, 'Step06', 'SVeRa_vs_latitude_statistics_50-80kmAltitude.dat') 
    headerLines = [
    '',
    ' S (latitude) = latitude * a + b (latitude range between -90˚ and 0˚)',
    ' r^2 = goodness of fit (0,1) as defined by: sum ( (y - (a * x + b)) ** 2 )  / sum ( (y - dataAverage) ** 2 ), with dataAverage = np.sum (y) / N ',
    ' Pearson Coef. = Pearson correlation coefficient (-1,+1)',
    ' dPearson Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
    ' Spearman Coef. = Spearman R correlation coefficient (-1,+1)',
    ' dSpearman Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
    '',
    ' Altitude   a      da        b      db     r^2   Pearson Coef  dPearson Coef   Spearman Coef  dSpearman Coef',
    '   (km)      (K/km/˚)         (K/km/˚) '
    ]



orbitIDs = np.asarray ( RFRvsTorS [0][0] )
latitudesPerOrbit = np.asarray ( RFRvsTorS [0][4] )

iValidOrbits = np.where ( orbitIDs >= orbitIDLimit [0] )[0]

altitudesToAnalyse = [ 50 + i  for i in range (31) ]
iColumnAltitudeToAnalyse = [ 5 + (altitudeToAnalyse - 50) * 2   for altitudeToAnalyse in altitudesToAnalyse ]

linearFits = []

spearmanStatistics = []
dSpearmanStatistics = []
pearsonStatistics = []
dPearsonStatistics = []


# Create the table file to write the results.
fileOpen = open (tableFileName, 'w')
headerString = HandyTools.getTableHeader (tableFileName, creationScript = 'CreateTable_T-S_vs_LatitudeVariability.py', headerLines = headerLines)
print (headerString, file = fileOpen)


# Go through all the altitudes and evaluate the relation between temperature at that level and latitude.
for iAltitude in range (31):

    print ('iAltitude = ', iAltitude)

    spearmanStatisticPermutations = []
    pearsonStatisticPermutations = []
    for iPermutation in range (numberOfPermutations):
    
        temperaturesAtLatitudePermutation = \
         DataTools.getDataValuesWithGaussianNoise ( 
          RFRvsTorS [0][ iColumnAltitudeToAnalyse [iAltitude] ][iValidOrbits], 
          DataTools.getNanFreeNumpyArray ( RFRvsTorS [0][ iColumnAltitudeToAnalyse [iAltitude] + 1 ][iValidOrbits], replaceWithValue = True ) )

        linearFit, pearsonStatistic, spearmanStatistic = \
         analyseCorrelation ( latitudesPerOrbit [iValidOrbits], temperaturesAtLatitudePermutation )
       
        spearmanStatisticPermutations.append (spearmanStatistic.statistic)
        pearsonStatisticPermutations.append (pearsonStatistic.statistic)
    

    
    linearFit, pearsonStatistic, spearmanStatistic = \
     analyseCorrelation ( latitudesPerOrbit [iValidOrbits], RFRvsTorS [0][ iColumnAltitudeToAnalyse [iAltitude] ][iValidOrbits] )

    linearFits.append (linearFit)

    spearmanStatistics.append (spearmanStatistic.statistic)
    spearmanStatisticsAverage, spearmanStatisticsStandardDeviation, spearmanStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (pearsonStatisticPermutations)
    dSpearmanStatistics.append (spearmanStatisticsStandardDeviation)

    pearsonStatistics.append (pearsonStatistic.statistic)
    pearsonStatisticsAverage, pearsonStatisticsStandardDeviation, pearsonStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (spearmanStatisticPermutations)
    dPearsonStatistics.append (pearsonStatisticsStandardDeviation) 


    print ('    {:2d}   {:6.3f} {:7.4f}   {:6.2f}  {:5.3f}  {:6.3f}    {:6.3f}        {:7.4F}         {:6.3f}         {:7.4f} '.\
     format (iAltitude + 50, linearFit [0], linearFit [2], linearFit [1], linearFit [3], linearFit [4], 
             pearsonStatistic.statistic, pearsonStatisticsStandardDeviation, 
             spearmanStatistic.statistic, spearmanStatisticsStandardDeviation ), file = fileOpen)



fileOpen.close ()

    
    
    




