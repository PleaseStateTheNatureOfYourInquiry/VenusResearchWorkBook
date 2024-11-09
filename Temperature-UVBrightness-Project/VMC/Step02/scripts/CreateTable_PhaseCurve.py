# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241022

# Load all the (hand)-selected images (see VMCImagesEvaluate.py in Step01) and extract the phase angle, the average and median radiance factor of all the valid 
#  points in the image and write the results to a table, in order of increasing phase angle.
#  The points on the Venus visible disk are selected based on a maximum incidence angle (i) and emission angle (e): 
#  Lee et al. (2015, Long-term variations of the UV contrast on Venus observed by the Venus Monitoring Camera on board Venus Express, 
#   http://dx.doi.org/10.1016/j.icarus.2015.02.015) adopt values of i < 84˚ and e < 81˚. 

#  Also write to the table the Radiance Scaling Factor from the image meta data, that is used to calibrate the radiance values.


# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt


# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools

from VeRaTools import VeRaTools
from VMCTools import VMCTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Extract the average and median of the radiance factor for a given image.
def processImage ( VMCFileNameRoot,
                   incidenceAngleLimit = 89, 
                   emissionAngleLimit = 89,
                   iterativeOutlierRemoval = True,
                   sigmaLimit = 2.5, 
                   percentageLimit = 1,
                   createQQPlots = False ):

    # Load the .IMG and .GEO files information.   
    VMCImage, VMCImageFlattened, VMCGeoCube, VMCGeoArraysFlattened = VMCTools.readVMCImageAndGeoCube (VMCFileNameRoot + '.GEO')

    # Perform the photometry on the image.
    VMCImageCalibrated, VMCImageCalibratedFlattened, \
    incidenceAngleAverage, incidenceAngleSTD, \
    emissionAngleAverage, emissionAngleSTD, \
    phaseAngleAverage, phaseAngleSTD, radianceScalingFactor = \
     VMCTools.VMCPhotometry ( VMCImage, 
                              VMCImageFlattened, 
                              VMCGeoCube, 
                              VMCGeoArraysFlattened,
                              incidenceAngleLimit = incidenceAngleLimit,
                              emissionAngleLimit = emissionAngleLimit )        

    
    iOnDiskValid = np.where ( VMCImageCalibratedFlattened > 0) [0]
    radianceFactorsOnDisk = VMCImageCalibratedFlattened [iOnDiskValid]
    iValidRadianceFactors = np.arange ( len (radianceFactorsOnDisk) )

    print ( ' Number of inital valid points on disk {}'.format ( len (radianceFactorsOnDisk) ) )            

    # Iteratively remove outliers beyond a standard-deviation (sigma) limit given by the user, until the percentage change between the current 
    #  and the previous average value is less than the  percentageLimit  set by the user.
    removeOutliers = True
    iOutlierRemovalIteration = 0
    averageRadianceFactor = (0,0,0)
    while removeOutliers:
    
        previousAverage = averageRadianceFactor [0]

        averageRadianceFactor = DataTools.getAverageVarAndSDPYtoCPP ( radianceFactorsOnDisk [iValidRadianceFactors] )
    
        lowerLimit = averageRadianceFactor [0] - averageRadianceFactor [1] * sigmaLimit
        upperLimit = averageRadianceFactor [0] + averageRadianceFactor [1] * sigmaLimit

        # Create plots of the iterative averaging processes for the work book. The plots will be saved to the same scripts directory and need to be
        #  placed in the proper directory manually afterwards. 
        if createQQPlots:
        
            
            plotTitle = VMCFileNameRoot.split (separatorCharacter)[-1] + ' - iteration {:02d}'.format(iOutlierRemovalIteration) 
            DataTools.QQPlot ( radianceFactorsOnDisk [iValidRadianceFactors], 
                               QQTitleToPrint = plotTitle + ' - QQ',
                               HistTitleToPrint = plotTitle + ' - Histogram',
                               savePlots = True, 
                               plotBaseFileName = VMCFileNameRoot.split (separatorCharacter)[-1] + '_iteration_{:02d}'.format(iOutlierRemovalIteration) ) 
        
        
        numberOfValidRadianceFactorsCurrentRun = len (iValidRadianceFactors)
        
        # Select the new valid points based on the lower and upper limits defined by the current average, standard deviation and user defined  sigmaLimit .
        iValidRadianceFactors = np.where ( np.logical_and (radianceFactorsOnDisk > lowerLimit, radianceFactorsOnDisk < upperLimit) )[0]
        
        # Decide if the iteration process has finished or not.        
        if np.abs (averageRadianceFactor [0] - previousAverage) / averageRadianceFactor [0] <= (percentageLimit / 100) or not iterativeOutlierRemoval:
        
            removeOutliers = False
            
        else:
        
            iOutlierRemovalIteration += 1

        
    print ( ' iOutlierRemovalIteration = {}'.format (iOutlierRemovalIteration) )
    print ( ' Number of final valid points {}'.format (numberOfValidRadianceFactorsCurrentRun) )            
    
    
    # Calculate the median using the set with outliers removed.
    medianRadianceFactor = DataTools.getMedianAndQuantilesPYtoCPP ( radianceFactorsOnDisk [iValidRadianceFactors] )

        
    return averageRadianceFactor, medianRadianceFactor, phaseAngleAverage, iOutlierRemovalIteration, radianceScalingFactor, len (iValidRadianceFactors)
        

# Initialise the run.

# Note that  dataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
listOfVMCPNGFileNames = HandyTools.getFilesInDirectoryTree ( VMCDataDirectory, extension = 'png' )

# Only select the image file names from the  UsedImages  subfolders in each of the VMC orbit folders.
listOfUsedVMCPNGFileNames = [ listOfVMCPNGFileName for listOfVMCPNGFileName in listOfVMCPNGFileNames  if 'UsedImages' in listOfVMCPNGFileName ]

listOfUsedVMCPNGFileNames.sort ()

results = { 'images' : [],
            'phase angles' : [],
            'averages' : [],
            'medians' : [],
            'number of iterations' : [],
            'radiance scale factors' : [],
            'number of valid points' : [] }


sigmaLimit = 3
percentageLimit = 1
iterativeOutlierRemoval = True
orbits = []

# Based on section 3.2 of Lee et al. 2015 (Long-term variations of the UV contrast on Venus observed by the Venus Monitoring Camera on board Venus Express, 
#  http://dx.doi.org/10.1016/j.icarus.2015.02.015).

# incidenceAngleLimit = 84
# emissionAngleLimit = 81

incidenceAngleLimit = 89
emissionAngleLimit = 89

createTable = True

for VMCPNGFileName in listOfUsedVMCPNGFileNames:

# Use these four lines instead of the line above to only create the QQPlots of the iterative outlier removal for image  V0260_0047_UV2 as an example for the work book.
# for i in range (1,2,1):
# 
#     VMCPNGFileName = listOfUsedVMCPNGFileNames [i]   
#     createTable = False

    orbits.append ( VMCPNGFileName.split (separatorCharacter) [-3] )
      
    print ()
    print ('Processing image -', VMCPNGFileName)

    VMCImageFileNameRoot = os.path.join ( VMCPNGFileName.split ('UsedImages')[0], VMCPNGFileName.split (separatorCharacter)[-1][:-4] )
        
    
    createQQPlots = False
    if 'V0260_0047_UV2' in VMCPNGFileName:
    
        createQQPlots = True


     
    averageRadianceFactor, medianRadianceFactor, phaseAngle, numberOfIterations, radianceScalingFactor, numberOfValidPoints = \
     processImage ( VMCImageFileNameRoot, incidenceAngleLimit = incidenceAngleLimit, emissionAngleLimit = emissionAngleLimit,
                    iterativeOutlierRemoval = iterativeOutlierRemoval, sigmaLimit = sigmaLimit, percentageLimit = percentageLimit,
                    createQQPlots = createQQPlots )

    results ['images'].append ( os.path.basename (VMCPNGFileName)[:-4] )
    results ['phase angles'].append (phaseAngle)
    results ['averages'].append (averageRadianceFactor)
    results ['medians'].append (medianRadianceFactor)
    results ['number of iterations'].append (numberOfIterations)
    results ['radiance scale factors'].append (radianceScalingFactor)
    results ['number of valid points'].append (numberOfValidPoints)



# This  if  statement is to avoid creating a new table when only creating the QQPlots of image V0260_0047_UV2 example.
if createTable:
   
    # Open and create the header of the table file that will contain information about the selected images.
    phaseCurveFileName = 'PhaseCurve_i<{}_e<{}.dat'.format (incidenceAngleLimit, emissionAngleLimit)
    fileOpen = open ( os.path.join (VMCWorkBookDirectory, 'Step02', phaseCurveFileName), 'w')

    headerLines = [
    '',
    ' RF = Radiance Factor',
    ' dAverage RF = Standard deviation of average RF',
    '',
    ' Radiance Scaling Factor from image header label RADIANCE_SCALING_FACTOR',
    '',
    ' Incidence angle < {:2d}˚'.format (incidenceAngleLimit),
    ' Emission angle < {:2d}˚'.format (emissionAngleLimit),
    '',
    '[9] REPLACE WITH iterativeOutlierRemoval LOOP',
    '',
    ' {} orbits with a total of {} images'.format ( len ( list (set (orbits)) ), len (listOfUsedVMCPNGFileNames) ),
    '',
    '    Image          phase angle   Average RF  dAverage RF     Q1 RF  Median RF  Q3 RF   # iterations   Radiance Scaling Factor    # valid data points',
    '                       (˚)                                                                              W/m2/ster/micron/DN'
    ]
 
    if iterativeOutlierRemoval:
    
        headerLines [9] = ' Iterative removal of outliers at the {}-sigma level with a > {}% change in average value\n Note: median values are calculated after iterative outlier removal!'.format (sigmaLimit, percentageLimit)
        
    else:
    
        headerLines [9] = ' No iterative outlier removal has been applied'
 
   
    headerString = HandyTools.getTableHeader (phaseCurveFileName, creationScript = 'CreateTable_PhaseCurve.py', headerLines = headerLines)
    print (headerString, file = fileOpen)
            
    
    iPhaseAngles = np.argsort ( np.asarray ( results ['phase angles' ] ) )
    
    for iPhaseAngle in iPhaseAngles: 
    
        print ( ' {}      {:6.2f}        {:6.3f}     {:7.4f}       {:6.3f}   {:6.3f}   {:6.3f}       {:2d}               {:7.5f}                      {:6d}'.
                format ( results ['images'][iPhaseAngle], 
                         results ['phase angles'][iPhaseAngle],
                         results ['averages'][iPhaseAngle][0], 
                         results ['averages'][iPhaseAngle][1], 
                         results ['medians'][iPhaseAngle][1],
                         results ['medians'][iPhaseAngle][0],
                         results ['medians'][iPhaseAngle][2],
                         results ['number of iterations'][iPhaseAngle],
                         results ['radiance scale factors'][iPhaseAngle],
                         results ['number of valid points'][iPhaseAngle] ), file = fileOpen )
    
    
    fileOpen.close ()
       




