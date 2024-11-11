# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241102

# 

# Choose the desired limitation in orbitIDVMC.

# orbitIDLimit = [0, 'All orbits']
orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']

# figureOrTableType = 'T' # Temperature
figureOrTableType = 'S' # static stability

allLatitudes = True
createFigures = True
createTables = True


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



def analyseCorrelation (Temperatures, RFRs):

    linearFit = DataTools.linearLeastSquare (Temperatures, RFRs)
    
    pearsonStatistics = stats.pearsonr (Temperatures, RFRs)
    spearmanStatistics = stats.spearmanr (Temperatures, RFRs)

    return linearFit, pearsonStatistics, spearmanStatistics



def createPlot ( Temperatures, 
                 dTemperatures,
                 RFRs,
                 dRFRs,
                 iAltitude,
                 latitudeRange = [],
                 allLatitudes = True,
                 fit = [],
                 pearsonStatistics = [],
                 spearmanStatistics = [],                  
                 figureOrTableType = 'temperature' ):

            
    plt.clf ()

    plt.scatter (Temperatures, RFRs)
    
    if allLatitudes:
    
        plt.title ( 'All latitudes - orbits >= {}'.format ( orbitIDLimit [0] ) )
        
    else:
    
        plt.title ( 'Latitudes between {:3d}˚ and {:3d}˚ - orbits >= {}'.format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ), orbitIDLimit [0] ) )

            
    if figureOrTableType == 'T':
    
        xLabelString = 'Temperature {}km (VeRa) (K)'.format (iAltitude + 50)
 
        
    if figureOrTableType == 'S':  
    
        xLabelString = 'Static Stability {}km (VeRa) (K/km)'.format (iAltitude + 50)
        
    
    plt.xlabel (xLabelString)
    plt.ylabel ( 'Radiance Factor Ratio (VMC)')
        
    HandyTools.plotErrorBars ( Temperatures, RFRs, 
                               xErrors = dTemperatures,
                               yErrors = dRFRs, colours = 'blue' )

  
    plt.title ('Altitude {:2d}km;  #points = {:2d}\nPearson = {:6.3f} +/- {:7.4f}, Spearman = {:6.3f} +/- {:7.4f}'. 
               format (iAltitude + 50, len (Temperatures), pearsonStatistics [0], pearsonStatistics [2], spearmanStatistics [0], spearmanStatistics [2] ), 
               fontsize = 11 )
        
#     plt.plot ( fit [5], fit [6], c = 'black', alpha = 0.2, 
#                label = 'RF = {:7.5f} ($\pm$ {:7.5f}) {} + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], figureOrTableType, fit [1], fit [3], fit [4] ) )
#     plt.legend ( loc = 'upper left', fontsize = 9 )
    
    
    if allLatitudes:

        HandyTools.createPathToFile ( fullPath = '../plots_{}/AllLatitudes'.format (figureOrTableType) )  
          
        plt.savefig ( '../plots_{}/AllLatitudes/Temperature{}km_vs_RadianceFactorRatio_all_latitudes.png'.format (figureOrTableType, iAltitude + 50) )

    else:
    
        HandyTools.createPathToFile ( fullPath = '../plots_{}/Latitudes_{:3d}_{:3d}'.format (figureOrTableType, int ( latitudeRange [0] ), int ( latitudeRange [1] ) ))
        
        plt.savefig ( '../plots_{}/Latitudes_{:3d}_{:3d}/Temperature{}km_vs_RadianceFactorRatio_latitudes_{:3d}_{:3d}.png'.
         format ( figureOrTableType, int ( latitudeRange [0] ), int ( latitudeRange [1] ), iAltitude + 50, int ( latitudeRange [0] ), int ( latitudeRange [1] ) ) )




def performAnalysis ( tableContent = None,
                      latitudeDependenceTableFile = '',
                      iAltitudeColumns = [],
                      iOrbitID = [],
                      latitudeRange = [],
                      numberOfPermutations = 1000,
                      allLatitudes = True,
                      createFigures = True,
                      createTables = True,
                      figureOrTableType = 'T' ):


    
    if allLatitudes:
        
        if figureOrTableType == 'T':
        
            tableContentLatitudeDependence = \
             HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', latitudeDependenceTableFile) )


        if figureOrTableType == 'S':

            tableContentLatitudeDependence = \
             HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', latitudeDependenceTableFile) )

    

    if createTables:

        if allLatitudes:
        
            tableFileName = '{}_Correlation_All_Latitudes.dat'.format (figureOrTableType)
        
        else:
        
            tableFileName = '{}_Correlation_Latitudes_{}_{}.dat'.format ( figureOrTableType, latitudeRange [0], latitudeRange [1] )
        
        

        tableFileOpen = open ( '../' + tableFileName, 'w' )     
        
        
        if allLatitudes and figureOrTableType == 'T':
        
            headerLines = [
            '',
            ' Temperature at each altitude level has been corrected for latitude variability by subtracting the linear relation from table {}'.format (latitudeDependenceTableFile),
            ' Pearson Coef. = Pearson correlation coefficient (-1,+1)',
            ' dPearson Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
            ' Spearman Coef. = Spearman R correlation coefficient (-1,+1)',
            ' dSpearman Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
            '',
            ' Altitude   Pearson Coef  dPearson Coef    Spearman Coef. dSpearman Coef   #Points',
            '   (km)'
            ]
        
        else:
        
            headerLines = [
            '',
            ' Pearson Coef. = Pearson correlation coefficient (-1,+1)',
            ' dPearson Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
            ' Spearman Coef. = Spearman R correlation coefficient (-1,+1)',
            ' dSpearman Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations),
            '',
            ' Altitude   Pearson Coef  dPearson Coef    Spearman Coef. dSpearman Coef   #Points',
            '   (km)'
            ]
        
        
        headerString = HandyTools.getTableHeader (tableFileName, creationScript = 'CreateTablesAndFigures_CorrelationAnalysis.py', headerLines = headerLines)
        print (headerString , file = tableFileOpen)


    # Loop over the altitude-columns
    for iAltitude, iColumn in enumerate (iAltitudeColumns):

        print ('iAltitude = ', iAltitude)
        VeRaTemperatures = tableContent [0][iColumn][iOrbitID]
        dVeRaTemperatures = tableContent [0][iColumn + 1][iOrbitID]
        #  tableContent [0][4][iOrbitID]  = latitude of the VeRa temperature sounding.
        
        # Only correct the temperatures at each altitude level for latitude variability if  allLatitudes  has been set to True. 
        #  If static stability has been chosen (figureOrTableType = 'S'), then do not apply correction.
        if allLatitudes and figureOrTableType == 'T':
        
            VeRaTemperatures = \
             tableContent [0][iColumn][iOrbitID] - \
             ( tableContentLatitudeDependence [0][1][iAltitude] * tableContent [0][4][iOrbitID] + tableContentLatitudeDependence [0][3][iAltitude] )
            
            dVeRaTemperatures = np.sqrt ( dVeRaTemperatures ** 2 + 
                                          ( tableContentLatitudeDependence [0][2][iAltitude] * tableContent [0][4][iOrbitID] ) ** 2 +
                                          tableContentLatitudeDependence [0][4][iAltitude] ** 2 )


#             if not iAltitude % 10:
#             
#                 for i in range (len (VeRaTemperatures)):
#                 
#                     print ( tableContent [0][iColumn][iOrbitID [i]], VeRaTemperatures [i], tableContent [0][iColumn+1][iOrbitID [i]] , dVeRaTemperatures [i] )
# 


        fit, pearsonStatisticOriginal, spearmanrStatisticOriginal = analyseCorrelation ( VeRaTemperatures, tableContent [0][1][iOrbitID] )
        
        pearsonStatistics = []
        spearmanStatistics = []
        for iPermatation in range (numberOfPermutations):
        
            fit, pearsonStatisticPermutation, spearmanrStatisticPermutation = \
             analyseCorrelation ( DataTools.getDataValuesWithGaussianNoise ( VeRaTemperatures, 
                                                                             DataTools.getNanFreeNumpyArray( dVeRaTemperatures, replaceWithValue = True ) ), 
                                  DataTools.getDataValuesWithGaussianNoise ( tableContent [0][1][iOrbitID], 
                                                                             DataTools.getNanFreeNumpyArray ( tableContent [0][2][iOrbitID], replaceWithValue = True ) ) )

            pearsonStatistics.append (pearsonStatisticPermutation.statistic)
            spearmanStatistics.append (spearmanrStatisticPermutation.statistic)

        
        pearsonStatisticsAverage, pearsonStatisticsStandardDeviation, pearsonStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (pearsonStatistics)
        spearmanStatisticsAverage, spearmanStatisticsStandardDeviation, spearmanStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (spearmanStatistics)
        
        
        if createFigures:
        
            createPlot ( VeRaTemperatures, dVeRaTemperatures, 
                         tableContent [0][1][iOrbitID], tableContent [0][2][iOrbitID],
                         iAltitude, 
                         latitudeRange = latitudeRange,
                         allLatitudes = allLatitudes,
                         fit = fit, 
                         pearsonStatistics = [pearsonStatisticOriginal.statistic, pearsonStatisticsAverage, pearsonStatisticsStandardDeviation],
                         spearmanStatistics = [spearmanrStatisticOriginal.statistic, spearmanStatisticsAverage, spearmanStatisticsStandardDeviation], 
                         figureOrTableType = figureOrTableType )
    
 
        if createTables:
        
            print ( '   {:2d}          {:6.3f}       {:7.4f}            {:6.3f}       {:7.4f}          {:3d}'.
                    format ( iAltitude + 50, 
                             pearsonStatisticOriginal.statistic, 
                             pearsonStatisticsStandardDeviation,
                             spearmanrStatisticOriginal.statistic,
                             spearmanStatisticsStandardDeviation,
                             len ( tableContent [0][iColumn][iOrbitID] ) ), file = tableFileOpen )
            
            
    if createTables:
    
        tableFileOpen.close ()
       


# Set the correct file names to write and read.
if figureOrTableType == 'T':

    tableContent = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat') )
    latitudeDependenceTableFile = 'TVeRa_vs_latitude_statistics_50-80kmAltitude.dat'


if figureOrTableType == 'S':

    tableContent = HandyTools.readTable ('../RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat')
    latitudeDependenceTableFile = 'SVeRa_vs_latitude_statistics_50-80kmAltitude.dat'



orbitIDs = tableContent [0][0]
cloudTopAltitudes = tableContent [0][3]
latitudes = tableContent [0][4]

numberOfAltitudes = int ( ( len ( tableContent [0] ) - 5 ) / 2 + 0.5 )

iAltitudeColumns = [ 5 + iColumn * 2  for iColumn in range (0, numberOfAltitudes) ]


if createFigures:

    plt.figure (1)


cloudTopAltitudesToInclude = [65, 71, 73]
if allLatitudes:

    iOrbitID = np.where ( orbitIDs >= orbitIDLimit [0] ) [0]
    performAnalysis ( tableContent = tableContent, 
                      latitudeDependenceTableFile = latitudeDependenceTableFile,
                      iAltitudeColumns = iAltitudeColumns, 
                      iOrbitID = iOrbitID,
                      latitudeRange = [],
                      allLatitudes = allLatitudes,
                      createFigures = createFigures,
                      createTables = createTables,
                      figureOrTableType = figureOrTableType )


else:   
    
    for cloudTopAltitude in cloudTopAltitudesToInclude:
    
        iOrbitID = np.where ( np.logical_and ( orbitIDs >= orbitIDLimit [0], cloudTopAltitudes == cloudTopAltitude ) ) [0]
        
        performAnalysis ( tableContent = tableContent, 
                          iAltitudeColumns = iAltitudeColumns, 
                          iOrbitID = iOrbitID, 
                          latitudeRange = [ min ( latitudes [iOrbitID] ), max ( latitudes [iOrbitID] ) ],
                          allLatitudes = allLatitudes,
                          createFigures = createFigures,
                          createTables = createTables,
                          figureOrTableType = figureOrTableType )




if createFigures:
    
    plt.close (1)
    

