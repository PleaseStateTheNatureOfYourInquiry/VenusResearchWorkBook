# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241023

# Extract the fitted values from the SPICAV-UV data as obtained by Marcq, R. et al., 2020. Climatology of SO2 and UV absorber at Venus' cloud top from SPICAV-UV T nadir dataset. 
#  Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002).
# Emmanuel Marcq sent his files corresponding to orbits 427 to 2811. In this script I only use between 1188 and 2811, the ones corresponding to what I actually use for 
#  analysis in this study.

# Standard imports.
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Custom imports
from astropy.io import fits
from astropy.table import Table

from HandyTools import HandyTools
from DataTools import DataTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *

fitsFilesO3 = HandyTools.getFilesInDirectoryTree ( os.path.join (SPICAVUCDataDirectory, 'Ozone'), extension = 'FIT' )
fitsFilesNoO3 = HandyTools.getFilesInDirectoryTree ( os.path.join (SPICAVUCDataDirectory, 'NoOzone'), extension = 'FIT' )

cloudTopOffSet = 4.95 #km, E. Marcq private communication 20240823.

# Load the median values (red line) from the Figure 14 of Marcq, R. et al., 2020. Climatology of SO2 and UV absorber at Venus' cloud top from SPICAV-UV T nadir dataset. 
#  Icarus 355, 133368, (https://doi.org/10.1016/j.icarus.2019.07.002).
figure14Data = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step03bis', 'Marcq_2020_Figure14.dat') )


# binSize = 5
binSize = 10
numberOfBins = 180 // binSize 
binBorders = []
for iBin in range (numberOfBins):

    binBorders.append ( [-90 + iBin * binSize, -90 + (iBin + 1) * binSize] )


altitudes = []
dAltitudes = []
latitudes = []

fitsFilesRuns = [ [fitsFilesO3, 'with O3'], [fitsFilesNoO3, 'without O3'] ]

# Go through all results with and without O3 included.
# The with-O3 give the results as published 
for fitsFiles in fitsFilesRuns:

    orbitIDs = []
    for fitsFile in fitsFiles [0]:
    
        fitsContent = fits.open (fitsFile)
        
        # In my final selection of VMC data, I take orbits > 1188. Hence I select the same orbits range for SPICAV.
        # Emmanuel has sent me up to orbits 2811, to match my 'last' VMC orbit (te last orbit of the South Polar Dynamics Campaign).
        if int ( fitsContent [0].header ['Orbit'] ) < 1188:
        
            continue
        
        orbitIDs.append ( fitsContent [0].header ['Orbit'] )
         
        print (fitsContent [0].header ['Orbit'], fitsContent.filename ())
        
        retrievedParameters = Table ( fitsContent[1].data )
        geoParameters = Table ( fitsContent[8].data )
    
        numberOfDataPoints = len (retrievedParameters)
        for iData in range (numberOfDataPoints):
        
            if not np.isnan ( retrievedParameters [iData][0][2] ):
    
                latitudes.append ( geoParameters [iData][0] )
            
                altitudes.append ( retrievedParameters [iData][0][2] + cloudTopOffSet )
                dAltitudes.append ( retrievedParameters [iData][1][2] )
            
    
        
    # Bin the altitudes in bins with width  binSize  (10˚ is default), the first bin start with lower border at -90˚. 
    latitudeBinnings = [ []  for iBin in range (numberOfBins) ]    
    for latitude, altitude in zip (latitudes, altitudes):
    
        iBin = 0
        while not ( latitude > binBorders [iBin][0] and latitude <= binBorders [iBin][1] ):
        
            iBin += 1
        
        latitudeBinnings [iBin].append (altitude)
    
    
    # Take the median of the values in all bins.           
    altitudesBinned = [ np.median (latitudeBinning)  for latitudeBinning in latitudeBinnings ]
    latitudesBinned =  -90 + binSize / 2 + np.arange (numberOfBins) * binSize
    
    
    plt.clf ()
    
    plt.scatter (latitudes, altitudes, c = 'lightblue', s = 10)
    plt.scatter ( latitudesBinned, altitudesBinned, c = 'orange', s = 30, label = 'median (bin size {}˚)'.format (binSize) )
    plt.xlim (-95,90)
    plt.xticks ( ticks = [tick  for tick in range (-90, 90, 30)] )
    plt.xticks ( ticks = [tick  for tick in range (-90, 90, 10)], minor = True )
    
    plt.xlabel ('latitude (˚)')
    plt.ylabel ('altitude cloud top (km)')
    plt.title ('SPICAV-UV data from orbit {} to {}; {}'.format ( orbitIDs [0], orbitIDs [-1], fitsFiles [1] ) )
    

    # Plot the red line and uncertainties from Marcq et al. 2020 Figure 14 for comparison. Also red colour for the line.
    plt.scatter (figure14Data [0][0], figure14Data [0][2], c = 'red', s = 10)
    plt.plot (figure14Data [0][0], figure14Data [0][2], c = 'red', label = 'Marcq et al. 2020 Fig. 14')
    HandyTools.plotErrorBars ( xValues = figure14Data [0][0], 
                               yValues = figure14Data [0][2], 
                               yErrors = figure14Data [0][2] - figure14Data [0][1], 
                               yErrorsUpperLimit = figure14Data [0][3] - figure14Data [0][2], colours = 'red' )
    
    plt.legend ()    
    
    plt.savefig ( os.path.join ( VMCWorkBookDirectory, 'Step03bis', 'plots', 'SPICAV-UV-Orbits_{}-{}_{}_binsize_{}.png'.
                  format (orbitIDs [0], orbitIDs [-1], fitsFiles [1].replace (' ', ''), binSize) ) )
    
