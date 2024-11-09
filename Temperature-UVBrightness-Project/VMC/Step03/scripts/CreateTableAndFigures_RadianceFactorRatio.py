# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241022

# Extract the Radiance Factors  from table file   VMCSelectedImages.dat  created in Step01 of the images of the selected orbits
#  (VMCOrbitBoundaries) and normalise each Radiance Factor to the model phase curve from table file  PhaseCurveFit_i<84_e<81.dat  created in Step02: 
#  the Radiance Factor Ratio (RFR). 
#
# The RFRs corresponds to the latitude-longitude wind advected boxes for each image. There is a large variation in the amount of individual pixels
#  on the Venus disk that are in a box, due to variations in the time difference between the time of the image and the time of the VeRa-measurement
#  and due to the observing geometry. Most boxes have several hundreds of points, but some have less than 10. The minimum number of point can be set
#  with  numberOfPointInLatitudeLongitudeBoxMinimum .


# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16

# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


createTable = True
createPlots = False

# The plots of the Radiance Factor Ratio vs T_VeRa - T_VMC or Phase Angle per valid orbit will be laid out on a grid.
numberOfSubPlotRows = 4
numberOfSubPlotColumns = 3
numberOfPlotsOnPage = numberOfSubPlotRows * numberOfSubPlotColumns
scale = 3
if createPlots:

    fig, subPlotAxis = plt.subplots (numberOfSubPlotRows, numberOfSubPlotColumns, figsize = (numberOfSubPlotRows * scale, numberOfSubPlotColumns * scale) )
    # Create the spacing from the border and between the plots (wspace and hspace).
    plt.subplots_adjust( bottom = 0.05,  top = 0.95, left = 0.05, right = 0.95, wspace = 0.3, hspace = 0.3 ) 



# Plot RFR vs T_VeRa - T_VMC or Phase Angle per orbit.
#  The first element in this list is the index of the value to take from the  VMCSelectedImages  file.

# Plot RFR vs T_VeRa - T_VMC per orbit.
abcissaList = [ 5, 'T_VMC - T_VeRa (h)', 'VeRaVMCTimeDifference' ]


# # Plot RFR vs phase angle per orbit.
# abcissaList = [14, 'Phase Angle (˚)', 'PhaseAngle']
    


#
def getAverageAndMedianRadianceFactorRatiosInOrbit (radianceFactorRatiosInOrbit, dRadianceFactorRatiosInOrbit):

    radianceFactorRatiosInOrbit = np.asarray (radianceFactorRatiosInOrbit)
    dRadianceFactorRatiosInOrbit = np.asarray (dRadianceFactorRatiosInOrbit)

    numberOfRadianceFactorRatios = len (radianceFactorRatiosInOrbit)
    if numberOfRadianceFactorRatios:
        
        radianceFactorRatiosAverage = DataTools.getAverageVarAndSDPYtoCPP (radianceFactorRatiosInOrbit)
        
        radianceFactorRatiosAverageInOrbit = radianceFactorRatiosAverage [0] 
        dRadianceFactorRatiosAverageInOrbit =  max ( radianceFactorRatiosAverage [1], 
                                                     np.sum ( np.sqrt (dRadianceFactorRatiosInOrbit ** 2) ) / numberOfRadianceFactorRatios )
    
    
     
        # Call the  getMedianAndQuantilesPYtoCPP  function of DataTools, with the uncertainties for each point and a 1000 random experiments:
        #  the presence of the uncertainties list triggers the estimation of the uncertainty in the median. 
        radianceFactorRatiosMedian = DataTools.getMedianAndQuantilesPYtoCPP ( radianceFactorRatiosInOrbit, 33, 67, 
                                                                              uncertainties = dRadianceFactorRatiosInOrbit, 
                                                                              numberOfUncertaintyExperiments = 1000 )
        
        radianceFactorRatiosMedianInOrbit = radianceFactorRatiosMedian [0]
        dRadianceFactorRatiosMedianInOrbit = max ( ( radianceFactorRatiosMedian [2] - radianceFactorRatiosMedian [1] ) / 2, radianceFactorRatiosMedian [3] )


        return radianceFactorRatiosAverageInOrbit, dRadianceFactorRatiosAverageInOrbit, radianceFactorRatiosMedianInOrbit, dRadianceFactorRatiosMedianInOrbit
    
    else:
    
        return 0, 0, 0, 0



# Add a figure to the next subplot.
def addFigureToPage ( iSubPlot, 
                      numberOfSubPlotRows,
                      numberOfSubPlotColumns,
                      subPlotAxis, 
                      radianceFactorRatiosInOrbit,
                      dRadianceFactorRatiosInOrbit,
                      abcissaData,
                      VMCOrbitID,
                      latitude,
                      averageAndMedianValues ):

    iRow = iSubPlot // numberOfSubPlotColumns
    iColumn = iSubPlot % numberOfSubPlotColumns
    
    subPlotAxis [iRow, iColumn].scatter (abcissaData, radianceFactorRatiosInOrbit)
    HandyTools.plotErrorBars ( abcissaData, 
                               radianceFactorRatiosInOrbit, yErrors = dRadianceFactorRatiosInOrbit, colours = 'blue',
                               axis = subPlotAxis [iRow, iColumn] )
    
    
    abcissaDataRange = max (abcissaData) - min (abcissaData)
    xlim_minimum = int ( min (abcissaData) - 0.1 * abcissaDataRange )
    xlim_maximum = int ( max (abcissaData) + 0.1 * abcissaDataRange )
    subPlotAxis [iRow, iColumn].set_xlim (xlim_minimum, xlim_maximum)
    
    subPlotAxis [iRow, iColumn].hlines ( y = averageAndMedianValues [0], xmin = xlim_minimum, xmax = xlim_maximum, color = 'red', linewidths = 1 )

    subPlotAxis [iRow, iColumn].fill_between ( x = [xlim_minimum, xlim_maximum], 
                                               y1 = [averageAndMedianValues [0] - averageAndMedianValues [1], averageAndMedianValues [0] - averageAndMedianValues [1]],
                                               y2 = [averageAndMedianValues [0] + averageAndMedianValues [1], averageAndMedianValues [0] + averageAndMedianValues [1]],
                                               color = 'red', alpha = 0.1)

    subPlotAxis [iRow, iColumn].hlines ( y = averageAndMedianValues [2], xmin = xlim_minimum, xmax = xlim_maximum, color = 'green', linewidths = 1 )

    subPlotAxis [iRow, iColumn].fill_between ( x = [xlim_minimum, xlim_maximum], 
                                               y1 = [averageAndMedianValues [2] - averageAndMedianValues [3], averageAndMedianValues [2] - averageAndMedianValues [3]],
                                               y2 = [averageAndMedianValues [2] + averageAndMedianValues [3], averageAndMedianValues [2] + averageAndMedianValues [3]],
                                               color = 'green', alpha = 0.1)

    
    subPlotAxis [iRow, iColumn].set_title ('Orbit {} (latitude {:5.2f}˚)'.format (VMCOrbitID, latitude), fontsize = 8)


    subPlotAxis [iRow, iColumn].tick_params ( axis='x', labelsize = 7 )
    subPlotAxis [iRow, iColumn].tick_params ( axis='y', labelsize = 7 )



# When a grid is complete, save it to a file and reset.
#  Before saving, add the horizontal and vertical axes labels on the left and bottom plots only.
def savePlotPage (iSubPlotPage, iSubPlot, abcissaList):

    # Add the horizontal axes labels to the bottom plots.
    iRow = (iSubPlot - 1) // numberOfSubPlotColumns
    iColumn = (iSubPlot - 1) % numberOfSubPlotColumns            
    while iColumn:
       
        subPlotAxis [iRow, iColumn].set_xlabel (abcissaList [1], fontsize = 7)          
        iColumn -= 1    


    subPlotAxis [iRow, 0].set_xlabel (abcissaList [1], fontsize = 7)

    # Add the vertical axes labels to the left plots.    
    while iRow:
    
        subPlotAxis [iRow, 0].set_ylabel ('RFR', fontsize = 7)
        iRow -= 1     

        
    subPlotAxis [0, 0].set_ylabel ('RFR', fontsize = 7)
        
        
    # Save this completed grid.
    plotPageFileName = '../plots/RadianceFactorRatio_vs_{}_{:02d}.png'.format (abcissaList [2], iSubPlotPage)
    HandyTools.createPathToFile (plotPageFileName)
    plt.savefig (plotPageFileName)



# This is the minimum amount of points that need to be present in a latitude-longitude box for this data value to be included.
#  It is the  - #Points in box -  column in the  VMCSelectedImages.dat  file.
numberOfPointInLatitudeLongitudeBoxMinimum = 0

# Limit the phase angle of the data values to include.
phaseAngleLimit = 130

# Load the data from the table files.

VMCSelectedImagesFileName = 'VMCSelectedImages.dat'
VMCSelectedImages = HandyTools.readTable ( os.path.join ( VMCWorkBookDirectory, 'Step01', '{}'.format (VMCSelectedImagesFileName) ) )
numberOfVMCImages = len ( VMCSelectedImages [0][0] )

phaseCurveFitFileName = 'PhaseCurveFit_i<84_e<81.dat'
phaseCurve =  HandyTools.readTable ( os.path.join ( VMCWorkBookDirectory, 'Step02', '{}'.format (phaseCurveFitFileName) ) )


# Go through all the images in the  VMCSelectedImages.dat  table and collect all the valid data points from the selected images per orbit.
iImage = 0
VMCOrbitIDsUnique = [ VMCSelectedImages [1][0][iImage] ]

radianceFactorRatiosInOrbit = []
dRadianceFactorRatiosInOrbit = []
latitudesInOrbit = []
abcissaDataInOrbit = []

radianceFactorRatiosAveragePerOrbit = []
dRadianceFactorRatiosAveragePerOrbit = []

radianceFactorRatiosMedianPerOrbit = []
dRadianceFactorRatiosMedianPerOrbit = []

latitudesPerOrbit = []

numberOfValuesPerOrbit = []

iSubPlot = -1
iSubPlotPage = 0
for iImage in range (numberOfVMCImages):

    VMCOrbitID = VMCSelectedImages [1][0][iImage]
    numberOfPointInLatLonBox = VMCSelectedImages [0][15][iImage]
    
    # The phase angle is binned in 1˚ bins, hence take the integer.
    phaseAngle = int ( VMCSelectedImages [0][14][iImage] )


    # When the image at  iImage  has a new  orbitID  then the all the images from the previous orbit have been collected, and the
    #  statistics for this orbit can be calculated.
    # Select the images based on the orbits IDs, the phase angle and the minimum number of points in the latitude-longitude boxes.  
    if VMCOrbitID != VMCOrbitIDsUnique [-1] or iImage == numberOfVMCImages - 1:
    
        averageAndMedianValues = getAverageAndMedianRadianceFactorRatiosInOrbit (radianceFactorRatiosInOrbit, dRadianceFactorRatiosInOrbit)
        
        radianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [0] )
        dRadianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [1] )
        
        radianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [2] )
        dRadianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [3] )
        
        latitudesPerOrbit.append ( DataTools.getMedianAndQuantilesPYtoCPP (latitudesInOrbit)[0] )
        
        numberOfValuesPerOrbit.append ( len (radianceFactorRatiosInOrbit) )

        
        # Add the RFR vs VeRaVMC time difference plot to the plot page.
        if createPlots and VMCOrbitIDsUnique [-1] > '1188' and len (radianceFactorRatiosAveragePerOrbit):

            iSubPlot += 1        
            if iSubPlot // (numberOfSubPlotRows * numberOfSubPlotColumns):
            
                iSubPlotPage += 1
                savePlotPage (iSubPlotPage, iSubPlot, abcissaList)
                plt.close (fig)  

                fig, subPlotAxis = plt.subplots ( numberOfSubPlotRows, numberOfSubPlotColumns, 
                                                  figsize = (numberOfSubPlotRows * scale, numberOfSubPlotColumns * scale) )  
                plt.subplots_adjust( bottom = 0.05,  top = 0.95, left = 0.05, right = 0.95, wspace = 0.3, hspace = 0.3 ) 
                            
                iSubPlot = 0
                

            addFigureToPage ( iSubPlot,
                              numberOfSubPlotRows,
                              numberOfSubPlotColumns,
                              subPlotAxis, 
                              radianceFactorRatiosInOrbit,
                              dRadianceFactorRatiosInOrbit,
                              abcissaDataInOrbit,
                              VMCOrbitIDsUnique [-1], 
                              latitudesPerOrbit [-1],
                              averageAndMedianValues )


        # Reset for the next orbit    
        VMCOrbitIDsUnique.append (VMCOrbitID)
        radianceFactorRatiosInOrbit = []
        dRadianceFactorRatiosInOrbit = []
        latitudesInOrbit = []
        abcissaDataInOrbit = []

   
    # If the current image is to be taken into account, then add it to the list of this orbit.
    if phaseAngle <= phaseAngleLimit and numberOfPointInLatLonBox >= numberOfPointInLatitudeLongitudeBoxMinimum:
    
        # Find the index in the model phase curve  phaseCurve  (1˚ step) for this angle.
        iPhaseCurve = phaseAngle - int ( phaseCurve [0][0][0] )

        # Check that correct phase curve value is taken from the fitted phase curve.
#         print (phaseAngle, iPhaseCurve, phaseCurve [0][0][iPhaseCurve] )

        radianceFactorRatiosInOrbit.append ( VMCSelectedImages [0][16][iImage] / phaseCurve [0][1][iPhaseCurve] )
        
        # Take the "MaxMin RF (= maximum - minimum / 2 ) of the Radiance Factor from 1000 gaussian noise experiments"   of the phase curve as the uncertainty.    
        dPhaseCurve = phaseCurve [0][4][iPhaseCurve]
        
        # The uncertainty in the   RadianceFactorInLatLonBox / phaseCurve  is derived from the formula of propagating erros for a division.
        dRadianceFactorRatiosInOrbit.append ( 
            np.sqrt ( ( VMCSelectedImages [0][17][iImage] / phaseCurve [0][1][iPhaseCurve] ) ** 2 +
                      ( dPhaseCurve * VMCSelectedImages [0][16][iImage] / ( phaseCurve [0][1][iPhaseCurve] ) ** 2 ) ** 2 ) )
        

        latitudesInOrbit.append ( VMCSelectedImages [0][8][iImage] )
        abcissaDataInOrbit.append ( VMCSelectedImages [0][ abcissaList [0] ][iImage] )


    
# Add the values for the last orbit.
averageAndMedianValues = getAverageAndMedianRadianceFactorRatiosInOrbit (radianceFactorRatiosInOrbit, dRadianceFactorRatiosInOrbit)

radianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [0] )
dRadianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [1] )

radianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [2] )
dRadianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [3] )

latitudesPerOrbit.append ( DataTools.getMedianAndQuantilesPYtoCPP (latitudesInOrbit)[0] )

numberOfValuesPerOrbit.append ( len (radianceFactorRatiosInOrbit) )


if createPlots:        

    for iSubPlotRemove in range (iSubPlot + 1, numberOfPlotsOnPage):
    
        iRow = iSubPlotRemove // numberOfSubPlotColumns
        iColumn = iSubPlotRemove % numberOfSubPlotColumns
        
        subPlotAxis [iRow, iColumn].remove ()

    
    iSubPlotPage += 1
    savePlotPage (iSubPlotPage, iSubPlot + 1, abcissaList)
    plt.close (fig)


if createTable:

    # Safe all the results to the table file.
    RadianceFactorsRatiosPerOrbitFileName = 'RadianceFactorRatiosPerOrbit.dat'
    fileOpen = open ( os.path.join (VMCWorkBookDirectory, 'Step03', RadianceFactorsRatiosPerOrbitFileName), 'w')
    
    headerLines = [
    '',
    ' RFR = Radiance Factor Ratio',
    ' dRFR = uncertainty in the RFR',
    ' Latitude = median of the latitudes of the images in each orbit',
    '',
    ' Image data from VMC/Step01/{}'.format (VMCSelectedImagesFileName),
    ' Phase curve from VMC/Step02/{}'.format (phaseCurveFitFileName),
    '',
    ' Phase angle <= {:3d}˚'.format (phaseAngleLimit),
    '',
    ' Orbit     Latitude    RFR_Average  dRFR_Average    RFR_Median   dRFR_Median   #Images in Orbit',
    '              (˚)'
    ]

    headerString = HandyTools.getTableHeader (RadianceFactorsRatiosPerOrbitFileName, creationScript = 'CreateTableAndFigures_RadianceFactorRatio.py', headerLines = headerLines)    
    print (headerString, file = fileOpen)
    
    
    for iOrbit in range ( len (VMCOrbitIDsUnique) ): 
    
        print ( '  {}      {:6.2f}      {:6.2f}        {:6.3f}         {:6.2f}        {:6.3f}        {:4d}'.
                format ( VMCOrbitIDsUnique [iOrbit], 
                         latitudesPerOrbit [iOrbit],
                         radianceFactorRatiosAveragePerOrbit [iOrbit],
                         dRadianceFactorRatiosAveragePerOrbit [iOrbit],
                         radianceFactorRatiosMedianPerOrbit [iOrbit],
                         dRadianceFactorRatiosMedianPerOrbit [iOrbit],
                         numberOfValuesPerOrbit [iOrbit] ), file = fileOpen )
    
    
    fileOpen.close ()


