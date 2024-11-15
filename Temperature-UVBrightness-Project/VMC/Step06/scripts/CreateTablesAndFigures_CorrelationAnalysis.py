# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241112

# 

# Choose the desired limitation in orbitIDVMC.

orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']

# figureOrTableType = 'T' # Temperature
figureOrTableType = 'S' # static stability

allLatitudes = True
createFigures = True
createTables = True

correctionType = 'uncorrected'
# correctionType = 'normalised'
# correctionType = 'subtracted'


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
                 figureOrTableType = 'temperature',
                 correctionType = 'uncorrected' ):

            
    plt.clf ()

    plt.scatter (Temperatures, RFRs)
    
    if allLatitudes:
    
        plt.title ( 'Latitudes between 0˚ and -90˚'.format ( orbitIDLimit [0] ) )
        
    else:
    
        plt.title ( 'Latitudes between {:3d}˚ and {:3d}˚'.format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ), orbitIDLimit [0] ) )

            
    if figureOrTableType == 'T':
    
        xLabelString = '({}) Temperature {}km (VeRa) (K)'.format (correctionType, iAltitude + 50)
 
        
    if figureOrTableType == 'S':  
    
        xLabelString = 'Static Stability {}km (VeRa) (K/km)'.format (iAltitude + 50)
        
    
    plt.xlabel (xLabelString)
    plt.ylabel ( 'Radiance Factor Ratio (VMC)')
        
    HandyTools.plotErrorBars ( Temperatures, RFRs, 
                               xErrors = dTemperatures,
                               yErrors = dRFRs, colours = 'blue', alpha = 0.3 )

  
    plt.title ('Altitude {:2d}km;  #points = {:2d}\nPearson = {:6.3f} +/- {:7.4f}, Spearman = {:6.3f} +/- {:7.4f}'. 
               format (iAltitude + 50, len (Temperatures), pearsonStatistics [0], pearsonStatistics [2], spearmanStatistics [0], spearmanStatistics [2] ), 
               fontsize = 11 )
        
#     plt.plot ( fit [5], fit [6], c = 'black', alpha = 0.2, 
#                label = 'RF = {:7.5f} ($\pm$ {:7.5f}) {} + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], figureOrTableType, fit [1], fit [3], fit [4] ) )
#     plt.legend ( loc = 'upper left', fontsize = 9 )
    
    
    if allLatitudes:
    
        if figureOrTableType == 'T':

            fullPath = '../plots_{}_{}/AllLatitudes'.format (figureOrTableType, correctionType)          
            figureFileName = '../plots_{}_{}/AllLatitudes/Temperature{}km_vs_RadianceFactorRatio_all_latitudes.png'.format (figureOrTableType, correctionType, iAltitude + 50)

        else:

            fullPath = '../plots_{}/AllLatitudes'.format (figureOrTableType)          
            figureFileName = '../plots_{}/AllLatitudes/Temperature{}km_vs_RadianceFactorRatio_all_latitudes.png'.format (figureOrTableType, iAltitude + 50)
        

        HandyTools.createPathToFile (fullPath = fullPath)        
        plt.savefig (figureFileName)
                

    else:
    
        if figureOrTableType == 'T':
    
            fullPath = '../plots_{}_{}/Latitudes_{}_{}'.format (figureOrTableType, correctionType, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )            
            figureFileName = '../plots_{}_{}/Latitudes_{}_{}/Temperature{}km_vs_RadianceFactorRatio_latitudes_{}_{}.png'.\
             format ( figureOrTableType, correctionType, int ( latitudeRange [0] ), int ( latitudeRange [1] ), iAltitude + 50, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )

        else:
        
            fullPath = '../plots_{}/Latitudes_{}_{}'.format (figureOrTableType, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )            
            figureFileName = '../plots_{}/Latitudes_{}_{}/Temperature{}km_vs_RadianceFactorRatio_latitudes_{}_{}.png'.\
             format ( figureOrTableType, int ( latitudeRange [0] ), int ( latitudeRange [1] ), iAltitude + 50, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )


    HandyTools.createPathToFile (fullPath = fullPath)        
    plt.savefig (figureFileName)



def performAnalysis ( tableContent = None,
                      latitudeDependenceTableFile = '',
                      iAltitudeColumns = [],
                      iOrbitIDs = [],
                      latitudeRange = [],
                      numberOfPermutations = 1000,
                      allLatitudes = True,
                      createFigures = True,
                      createTables = True,
                      figureOrTableType = 'T',
                      correctionType = 'uncorrected' ):


    
#     if allLatitudes:
    if True:

        
        if figureOrTableType == 'T':
        
            tableContentLatitudeDependence = \
             HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', latitudeDependenceTableFile) )


        if figureOrTableType == 'S':

            tableContentLatitudeDependence = \
             HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', latitudeDependenceTableFile) )

    

    if createTables:

        if allLatitudes:
        
            tableFileName = '{}_Correlation_All_Latitudes_{}.dat'.format (figureOrTableType, correctionType)
        
        else:
        
            tableFileName = '{}_Correlation_Latitudes_{}_{}_{}.dat'.format ( figureOrTableType, latitudeRange [0], latitudeRange [1], correctionType)
        
        

        tableFileOpen = open ( os.path.join (VMCWorkBookDirectory, 'Step06', tableFileName), 'w' )     
        
        
        headerLines = [ '' ]
        if figureOrTableType == 'T':

            if correctionType == 'normalised':

                headerLines.append ( ' Temperature at each altitude level has been corrected for latitude variability by dividing by the linear relation from table {}'.format (latitudeDependenceTableFile) )
            
            
            if correctionType == 'subtracted':
 
                 headerLines.append ( ' Temperature at each altitude level has been corrected for latitude variability by subtracting the linear relation from table {}'.format (latitudeDependenceTableFile) )

        
        headerLines.append ( ' Pearson Coef. = Pearson correlation coefficient (-1,+1)' )
        headerLines.append ( ' dPearson Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations) )
        headerLines.append ( ' Spearman Coef. = Spearman R correlation coefficient (-1,+1)' )
        headerLines.append ( ' dSpearman Coef. = Uncertainty in the Pearson correlation coefficient (-1,+1) based on {} permutations.'.format (numberOfPermutations) )
        headerLines.append ( '' )
        headerLines.append ( ' Altitude   Pearson Coef  dPearson Coef    Spearman Coef. dSpearman Coef   #Points' )
        headerLines.append ( '   (km)' )
        
        headerString = HandyTools.getTableHeader (tableFileName, creationScript = 'CreateTablesAndFigures_CorrelationAnalysis.py', headerLines = headerLines)
        print (headerString , file = tableFileOpen)


    # Loop over the altitude-columns
    for iAltitude, iColumn in enumerate (iAltitudeColumns):

#         print ('iAltitude = ', iAltitude)
        VeRaTemperatures = tableContent [0][iColumn][iOrbitIDs]
        dVeRaTemperatures = tableContent [0][iColumn + 1][iOrbitIDs]
        #  tableContent [0][4][iOrbitIDs]  = latitude of the VeRa temperature sounding.
        
        # Only correct the temperatures at each altitude level for latitude variability if  allLatitudes  has been set to True. 
        #  If static stability has been chosen (figureOrTableType = 'S'), then do not apply correction.
#         if allLatitudes and figureOrTableType == 'T':
        if figureOrTableType == 'T':

            if correctionType == 'subtracted':
            
                VeRaTemperatures = \
                 tableContent [0][iColumn][iOrbitIDs] - \
                 ( tableContentLatitudeDependence [0][1][iAltitude] * tableContent [0][4][iOrbitIDs] + tableContentLatitudeDependence [0][3][iAltitude] )
                
                dVeRaTemperatures = np.sqrt ( dVeRaTemperatures ** 2 + 
                                              ( tableContentLatitudeDependence [0][2][iAltitude] * tableContent [0][4][iOrbitIDs] ) ** 2 +
                                                tableContentLatitudeDependence [0][4][iAltitude] ** 2 )


            elif correctionType == 'normalised':

                denominator = tableContentLatitudeDependence [0][1][iAltitude] * tableContent [0][4][iOrbitIDs] + tableContentLatitudeDependence [0][3][iAltitude]

                VeRaTemperatures = tableContent [0][iColumn][iOrbitIDs] / denominator
                
                dVeRaTemperatures = \
                 np.sqrt ( (dVeRaTemperatures / denominator) ** 2 + 
                           (tableContentLatitudeDependence [0][2][iAltitude] * tableContent [0][iColumn][iOrbitIDs] * tableContent [0][4][iOrbitIDs] / denominator ** 2) ** 2 +
                           (tableContentLatitudeDependence [0][4][iAltitude] * tableContent [0][iColumn][iOrbitIDs] / denominator ** 2) ** 2 )
                                              



        fit, pearsonStatisticOriginal, spearmanrStatisticOriginal = analyseCorrelation ( VeRaTemperatures, tableContent [0][1][iOrbitIDs] )
        
        pearsonStatistics = []
        spearmanStatistics = []
        for iPermatation in range (numberOfPermutations):
        
            fit, pearsonStatisticPermutation, spearmanrStatisticPermutation = \
             analyseCorrelation ( DataTools.getDataValuesWithGaussianNoise ( VeRaTemperatures, 
                                                                             DataTools.getNanFreeNumpyArray( dVeRaTemperatures, replaceWithValue = True ) ), 
                                  DataTools.getDataValuesWithGaussianNoise ( tableContent [0][1][iOrbitIDs], 
                                                                             DataTools.getNanFreeNumpyArray ( tableContent [0][2][iOrbitIDs], replaceWithValue = True ) ) )

            pearsonStatistics.append (pearsonStatisticPermutation.statistic)
            spearmanStatistics.append (spearmanrStatisticPermutation.statistic)

        
        pearsonStatisticsAverage, pearsonStatisticsStandardDeviation, pearsonStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (pearsonStatistics)
        spearmanStatisticsAverage, spearmanStatisticsStandardDeviation, spearmanStatisticsVariance = DataTools.getAverageVarAndSDPYtoCPP (spearmanStatistics)
        
        
        if createFigures:
        
            createPlot ( VeRaTemperatures, dVeRaTemperatures, 
                         tableContent [0][1][iOrbitIDs], tableContent [0][2][iOrbitIDs],
                         iAltitude, 
                         latitudeRange = latitudeRange,
                         allLatitudes = allLatitudes,
                         fit = fit, 
                         pearsonStatistics = [pearsonStatisticOriginal.statistic, pearsonStatisticsAverage, pearsonStatisticsStandardDeviation],
                         spearmanStatistics = [spearmanrStatisticOriginal.statistic, spearmanStatisticsAverage, spearmanStatisticsStandardDeviation], 
                         figureOrTableType = figureOrTableType,
                         correctionType = correctionType )
    
 
        if createTables:
        
            print ( '   {:2d}          {:6.3f}       {:7.4f}            {:6.3f}       {:7.4f}          {:3d}'.
                    format ( iAltitude + 50, 
                             pearsonStatisticOriginal.statistic, 
                             pearsonStatisticsStandardDeviation,
                             spearmanrStatisticOriginal.statistic,
                             spearmanStatisticsStandardDeviation,
                             len ( tableContent [0][iColumn][iOrbitIDs] ) ), file = tableFileOpen )
            
            
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


iOrbitIDs = np.where ( orbitIDs >= orbitIDLimit [0] ) [0]
latitudeRanges = [ [0, -40], [-40, -60], [-60, -90] ]

if allLatitudes:
        
    performAnalysis ( tableContent = tableContent, 
                      latitudeDependenceTableFile = latitudeDependenceTableFile,
                      iAltitudeColumns = iAltitudeColumns, 
                      iOrbitIDs = iOrbitIDs,
                      latitudeRange = [],
                      allLatitudes = allLatitudes,
                      createFigures = createFigures,
                      createTables = createTables,
                      figureOrTableType = figureOrTableType,
                      correctionType = correctionType )


else:   
    
    for latitudeRange in latitudeRanges:
    
        iLatitudes = np.where ( np.logical_and ( latitudes [iOrbitIDs] <= latitudeRange [0], latitudes [iOrbitIDs] > latitudeRange [1] ) ) [0]
        
        performAnalysis ( tableContent = tableContent,
                          latitudeDependenceTableFile = latitudeDependenceTableFile,
                          iAltitudeColumns = iAltitudeColumns, 
                          iOrbitIDs = iOrbitIDs [iLatitudes], 
                          latitudeRange = [ latitudeRange [0], latitudeRange [1] ],
                          allLatitudes = allLatitudes,
                          createFigures = createFigures,
                          createTables = createTables,
                          figureOrTableType = figureOrTableType,
                          correctionType = correctionType )




if createFigures:
    
    plt.close (1)
    

