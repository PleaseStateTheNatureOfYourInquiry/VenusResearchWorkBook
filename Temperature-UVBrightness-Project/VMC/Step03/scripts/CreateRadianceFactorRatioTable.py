# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240917

# Extract the Radiance Factors  from table file   VMCSelectedImages.dat  created in Step01 of the images of the selected orbits
# (VMCOrbitBoundaries) and normalise each Radiance Factor to the model phase curve from table file  PhaseCurveFit.dat  created in Step02: 
# this is called Radiance Factor Ratio (RFR). 
#
# The RFRs corresponds to the latitude-longitude wind advected boxes for each image. There is a large variation in the amount of individual pixels on the Venus
# disk that are in a box, due to variations in the time difference between the time of the image and the time of the VeRa-measurement and due to the observing 
# geometry. Most boxes have several hundreds of points, but some have less than 10. The minimum number of point can be set with  numberOfPointInLatitudeLongitudeBoxMinimum .
#


# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np


# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools


#
def getAverageAndMedianRadianceFactorRatiosInOrbit (radianceFactorRatiosInOrbit, dRadianceFactorRatiosInOrbit):
    '''
    '''

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


# This is the minimum amount of points that need to be present in a latitude-longitude box for this data value to be included.
#  It is the  - #Points in box -  column in the  VMCSelectedImages.dat  file.
numberOfPointInLatitudeLongitudeBoxMinimum = 0

# Limit the phase angle of the data values to include.
phaseAngleLimit = 130

# Load the data from the table files.
VMCSelectedImages = HandyTools.readTable ('../../Step01/VMCSelectedImages.dat')
numberOfVMCImages = len ( VMCSelectedImages [0][0] )

phaseCurve =  HandyTools.readTable ('../../Step02/PhaseCurveFit.dat')


# Go through all the images in the  VMCSelectedImages.dat  table and collect all the valid data points from the selected images per orbit.
iImage = 0
VMCOrbitIDsUnique = [ VMCSelectedImages [1][0][iImage] ]

radianceFactorRatiosInOrbit = []
dradianceFactorRatiosInOrbit = []
latitudesInOrbit = []

radianceFactorRatiosAveragePerOrbit = []
dRadianceFactorRatiosAveragePerOrbit = []

radianceFactorRatiosMedianPerOrbit = []
dRadianceFactorRatiosMedianPerOrbit = []

latitudesPerOrbit = []

numberOfValuesPerOrbit = []

for iImage in range (numberOfVMCImages):

    VMCOrbitID = VMCSelectedImages [1][0][iImage]
    numberOfPointInLatLonBox = VMCSelectedImages [0][15][iImage]
    
    # The phase angle is binned in 1˚ bins, hence take the integer.
    phaseAngle = int ( VMCSelectedImages [0][14][iImage] )


    # Select the images based on the orbits IDs, the phase angle and the minimum number of points in the latitude-longitude boxes.  
    if VMCOrbitID != VMCOrbitIDsUnique [-1]:
    
        averageAndMedianValues = getAverageAndMedianRadianceFactorRatiosInOrbit (radianceFactorRatiosInOrbit, dradianceFactorRatiosInOrbit)
        
        radianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [0] )
        dRadianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [1] )
        
        radianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [2] )
        dRadianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [3] )
        
        latitudesPerOrbit.append ( DataTools.getMedianAndQuantilesPYtoCPP (latitudesInOrbit)[0] )
        
        numberOfValuesPerOrbit.append ( len (radianceFactorRatiosInOrbit) )

        # Reset for the next orbit    
        VMCOrbitIDsUnique.append (VMCOrbitID)
        radianceFactorRatiosInOrbit = []
        dradianceFactorRatiosInOrbit = []
        latitudesInOrbit = []

   
    # If the current image is to be taken into account, then add it to the list of this orbit.
    if phaseAngle <= phaseAngleLimit and numberOfPointInLatLonBox >= numberOfPointInLatitudeLongitudeBoxMinimum:
    
        # Find the index in the model phase curve  phaseCurve  (1˚ step) for this angle.
        iPhaseCurve = phaseAngle - int ( phaseCurve [0][0][0] )
        radianceFactorRatiosInOrbit.append ( VMCSelectedImages [0][16][iImage] / phaseCurve [0][1][iPhaseCurve] )
        
        # Take the "MaxMin RF = maximum - minimum of the Radiance Factor from 1000 gaussian noise experiments"   of the phase curve as the uncertainty.    
        dPhaseCurve = phaseCurve [0][4][iPhaseCurve]
        
        # The uncertainty in the   RadianceFactorInLatLonBox / phaseCurve  is derived from the formula of propagating erros for a division.
        dradianceFactorRatiosInOrbit.append ( 
            np.sqrt ( ( VMCSelectedImages [0][17][iImage] / phaseCurve [0][1][iPhaseCurve] ) ** 2 +
                      ( dPhaseCurve * VMCSelectedImages [0][16][iImage] / ( phaseCurve [0][1][iPhaseCurve] ) ** 2 ) ** 2 ) )
        

        latitudesInOrbit.append ( VMCSelectedImages [0][8][iImage] )


    
# Add the values for the last orbit.
averageAndMedianValues = getAverageAndMedianRadianceFactorRatiosInOrbit (radianceFactorRatiosInOrbit, dradianceFactorRatiosInOrbit)

radianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [0] )
dRadianceFactorRatiosAveragePerOrbit.append ( averageAndMedianValues [1] )

radianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [2] )
dRadianceFactorRatiosMedianPerOrbit.append ( averageAndMedianValues [3] )

latitudesPerOrbit.append ( DataTools.getMedianAndQuantilesPYtoCPP (latitudesInOrbit)[0] )

numberOfValuesPerOrbit.append ( len (radianceFactorRatiosInOrbit) )


# Safe all the results to the table file.
RadianceFactorsRatiosPerOrbitFileName = 'RadianceFactorRatiosPerOrbit.dat'
fileOpen = open ( os.path.join ('..', RadianceFactorsRatiosPerOrbitFileName), 'w')

print (' ', file = fileOpen)
print (' File: {}'.format (RadianceFactorsRatiosPerOrbitFileName), file = fileOpen)
print (' Created at {}'.format ( HandyTools.getDateAndTimeString () ), file = fileOpen)



print (' ', file = fileOpen)
print (' RFR = Radiance Factor Ratio', file = fileOpen)
print (' dRFR = uncertainty in the RFR', file = fileOpen)
print (' Latitude = median of the latitudes of the images in each orbit', file = fileOpen)

print (' ', file = fileOpen)
print (' Image data from VMC/Step01/VMCSelectedImages.dat', file = fileOpen)
print (' Phase curve from VMC/Step02/PhaseCurveFit.dat', file = fileOpen)

print ( '', file = fileOpen )
print ( ' Phase angle <= {:3d}˚'.format (phaseAngleLimit), file = fileOpen )


print (' ', file = fileOpen)
print (' Orbit     Latitude    RFR_Average  dRFR_Average    RFR_Median   dRFR_Median   #Images in Orbit', file = fileOpen)
print ('              (˚)', file = fileOpen)
print ('C_END', file = fileOpen)


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


