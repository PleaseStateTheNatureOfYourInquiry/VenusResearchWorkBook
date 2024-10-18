# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241012

# 

# Choose the desired limitation in orbitIDVMC.

# orbitIDLimit = [0, 'All orbits']
orbitIDLimit = [1188, 'Orbits >= 1188 (Ext. 2)']

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
    spearmanrStatistics = stats.spearmanr (Temperatures, RFRs)

    return linearFit, spearmanrStatistics



def createPlot (Temperatures, dTemperatures, RFRs, dRFRs, iAltitude, latitudeRange = [], allLatitudes = True, fit = [], spearmanrStatistics = None):

            
    plt.clf ()

    plt.scatter (Temperatures, RFRs)
    
    if allLatitudes:
    
        plt.title ( 'All latitudes - orbits >= {}'.format ( orbitIDLimit [0] ) )
        
    else:
    
        plt.title ( 'Latitudes between {:3d}˚ and {:3d}˚ - orbits >= {}'.format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ), orbitIDLimit [0] ) )

            
    plt.xlabel ( 'Cloud top temperature {}km (VeRa)'.format (iAltitude + 50) )
    plt.ylabel ( 'Radiance Factor Ratio (VMC)')
        
    HandyTools.plotErrorBars ( Temperatures, RFRs, 
                               xErrors = dTemperatures,
                               yErrors = dRFRs, colours = 'blue' )

      
    plt.plot ( fit [5], fit [6], c = 'black', alpha = 0.2, 
               label = 'RF = {:7.5f} ($\pm$ {:7.5f}) T + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], fit [1], fit [3], fit [4] ) )
    plt.legend ( loc = 'upper left', fontsize = 9 )
    
    if allLatitudes:
    
        plt.savefig ( '../plots/AllLatitudes/Temperature{}km_vs_RadianceFactorRatio_all_latitudes.png'.format (iAltitude + 50) )

    else:
    
        HandyTools.createPathToFile ( fullPath = '../plots/Latitudes_{:3d}_{:3d}'.format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ) ))
        
        plt.savefig ( '../plots/Latitudes_{:3d}_{:3d}/Temperature{}km_vs_RadianceFactorRatio_latitudes_{:3d}_{:3d}.png'.
         format ( int ( latitudeRange [0] ), int ( latitudeRange [1] ), iAltitude + 50, int ( latitudeRange [0] ), int ( latitudeRange [1] ) ) )



def performAnalysis (tableContent = None, iAltitudeColumns = [], iOrbitID = [], latitudeRange = [], allLatitudes = True, createFigures = True, createTables = True):


    # Loop over the altitude-columns
    for iAltitude, iColumn in enumerate (iAltitudeColumns):

        fit, spearmanrStatistics = analyseCorrelation ( tableContent [0][iColumn][iOrbitID], tableContent [0][1][iOrbitID] )

        print ()
        print (iAltitude + 50, fit [0], fit [2], fit [1], fit [3])
        print (spearmanrStatistics.statistic)

        if createFigures:
        
            createPlot ( tableContent [0][iColumn][iOrbitID], tableContent [0][iColumn + 1][iOrbitID], 
                         tableContent [0][1][iOrbitID], tableContent [0][2][iOrbitID],
                         iAltitude, 
                         latitudeRange = latitudeRange,
                         allLatitudes = allLatitudes,
                         fit = fit, 
                         spearmanrStatistics = spearmanrStatistics)
    
 
        if createTables:
        
            pass
    


tableContent = HandyTools.readTable ('../RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat')

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
                      iAltitudeColumns = iAltitudeColumns, 
                      iOrbitID = iOrbitID,
                      latitudeRange = [],
                      allLatitudes = allLatitudes,
                      createFigures = createFigures,
                      createTables = createTables )


else:   
    
    for cloudTopAltitude in cloudTopAltitudesToInclude:
    
        iOrbitID = np.where ( np.logical_and ( orbitIDs >= orbitIDLimit [0], cloudTopAltitudes == cloudTopAltitude ) ) [0]
        
        performAnalysis ( tableContent = tableContent, 
                          iAltitudeColumns = iAltitudeColumns, 
                          iOrbitID = iOrbitID, 
                          latitudeRange = [ min ( latitudes [iOrbitID] ), max ( latitudes [iOrbitID] ) ],
                          allLatitudes = allLatitudes,
                          createFigures = createFigures,
                          createTables = createTables )




if createFigures:
    
    plt.close (1)
    

