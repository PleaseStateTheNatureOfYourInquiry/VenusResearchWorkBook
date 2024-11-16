# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241112

# Create the tables and figures of the correlation between the Radiance Ratio Factor and the temperature (T) or static stability (S) for the altitude levels
#  between 50 and 80 km (31 levels).

# The temperature has latitudinal variation for all altitudes not in the 65-70km range. The variation can or not be corrected for, using the  
#  correctionType  string: "uncorrected", "normalised" or "subtracted" , at the top of the script.

# The  allLatitudes  boolean determines whether all latitudes are considered together, or the (three) latitude bins defined by 
#  latitudeRanges = [ [0, -40], [-40, -60], [-60, -90] ] .

# There is no significant variation of static stability with latitude, and hence no correction scheme is necessary.

# The plots are stored in folders: plot_S, plot_T_uncorrected, plot_T_normalised, plot_T_subtracted . 

# The tables that are created also have the  "uncorrected", "normalised" or "subtracted"  strings in the names, as well as a reference to the latitudes
#  (all latitudes, or bins). They contain the Spearman and Pearson correlation coefficients for each altitude, which correspond to the plots. 



# Choose the desired limitation in orbitIDVMC.
orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']

# Choose whether to calculate the RFR version temperature (T) or static stability (S).
# figureOrTableType = 'T'  # Temperature
figureOrTableType = 'S' # static stability


# If  allLatitudes  is True, then consider all latitudes together, otherwise split the analysis in the latitudes bins defined by  latitudeRanges  list.
allLatitudes = True
createFigures = False
createTables = True

# Select the type of temperature variation correction.
# correctionType = 'uncorrected'
# correctionType = 'normalised'
correctionType = 'subtracted'


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
        
# This is to draw the linear least square fitted lines, but since this can be misleading, it has been commented out.
#     plt.plot ( fit [5], fit [6], c = 'black', alpha = 0.2, 
#                label = 'RF = {:7.5f} ($\pm$ {:7.5f}) {} + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], figureOrTableType, fit [1], fit [3], fit [4] ) )
#     plt.legend ( loc = 'upper left', fontsize = 9 )
    
    
    if allLatitudes:
    
        if figureOrTableType == 'T':

            fullPath = '../plots_{}_{}/AllLatitudes'.format (figureOrTableType, correctionType)          
            figureFileName = '../plots_{}_{}/AllLatitudes/Temperature{}km_vs_RadianceFactorRatio_all_latitudes.png'.format (figureOrTableType, correctionType, iAltitude + 50)

        if figureOrTableType == 'S':

            fullPath = '../plots_{}/AllLatitudes'.format (figureOrTableType)          
            figureFileName = '../plots_{}/AllLatitudes/StaticStability{}km_vs_RadianceFactorRatio_all_latitudes.png'.format (figureOrTableType, iAltitude + 50)
        

        HandyTools.createPathToFile (fullPath = fullPath)        
        plt.savefig (figureFileName)
                

    else:
    
        if figureOrTableType == 'T':
    
            fullPath = '../plots_{}_{}/Latitudes_{}_{}'.format (figureOrTableType, correctionType, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )            
            figureFileName = '../plots_{}_{}/Latitudes_{}_{}/Temperature{}km_vs_RadianceFactorRatio_latitudes_{}_{}.png'.\
             format ( figureOrTableType, correctionType, int ( latitudeRange [0] ), int ( latitudeRange [1] ), iAltitude + 50, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )

        if figureOrTableType == 'S':
        
            fullPath = '../plots_{}/Latitudes_{}_{}'.format (figureOrTableType, int ( latitudeRange [0] ), int ( latitudeRange [1] ) )            
            figureFileName = '../plots_{}/Latitudes_{}_{}/StaticStability{}km_vs_RadianceFactorRatio_latitudes_{}_{}.png'.\
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



# Initially any latitudinal variation in temperature was corrected only when choosing all latitudes together (no bins), but it has been found better
#  to perform the correction (set with the  correctionType  string) for all situations.
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
        
            if figureOrTableType == 'T':
        
                tableFileName = '{}_Correlation_All_Latitudes_{}.dat'.format (figureOrTableType, correctionType)
                
            if figureOrTableType == 'S':
            
                tableFileName = '{}_Correlation_All_Latitudes.dat'.format (figureOrTableType)
        
        else:
        
            if figureOrTableType == 'T':
            
                tableFileName = '{}_Correlation_Latitudes_{}_{}_{}.dat'.format ( figureOrTableType, latitudeRange [0], latitudeRange [1], correctionType)
        
            if figureOrTableType == 'S':
            
                tableFileName = '{}_Correlation_Latitudes_{}_{}.dat'.format ( figureOrTableType, latitudeRange [0], latitudeRange [1])
        

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

        VeRaTemperatures = tableContent [0][iColumn][iOrbitIDs]
        dVeRaTemperatures = tableContent [0][iColumn + 1][iOrbitIDs]
        latitudes = tableContent [0][4][iOrbitIDs]

# Initially any latitudinal variation in temperature was corrected only when choosing all latitudes together (no bins), but it has been found better
#  to perform the correction (set with the  correctionType  string) for all situations.        
#         if allLatitudes and figureOrTableType == 'T':

        #  If static stability has been chosen (figureOrTableType = 'S'), then do not apply correction.
        if figureOrTableType == 'T':

            if correctionType == 'subtracted':
            
                VeRaTemperatures = \
                 tableContent [0][iColumn][iOrbitIDs] - \
                 ( tableContentLatitudeDependence [0][1][iAltitude] * latitudes + tableContentLatitudeDependence [0][3][iAltitude] )
                
                dVeRaTemperatures = np.sqrt ( dVeRaTemperatures ** 2 + 
                                              ( tableContentLatitudeDependence [0][2][iAltitude] * latitudes ) ** 2 +
                                                tableContentLatitudeDependence [0][4][iAltitude] ** 2 )


            elif correctionType == 'normalised':

                denominator = tableContentLatitudeDependence [0][1][iAltitude] * latitudes + tableContentLatitudeDependence [0][3][iAltitude]

                VeRaTemperatures = tableContent [0][iColumn][iOrbitIDs] / denominator
                
                dVeRaTemperatures = \
                 np.sqrt ( (dVeRaTemperatures / denominator) ** 2 + 
                           (tableContentLatitudeDependence [0][2][iAltitude] * tableContent [0][iColumn][iOrbitIDs] * latitudes / denominator ** 2) ** 2 +
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
       


# Table file names to read the Radiance Ratio Factors and temperarutes or static stability between 50-80km altitude.
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
    

