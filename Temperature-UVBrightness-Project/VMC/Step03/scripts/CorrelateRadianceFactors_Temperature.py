# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241022

# Extract the Radiance Factors and VeRa-derived temperatures from table file   VMCSelectedImages.dat  created in Step01 of the images of the selected orbits
# (VMCOrbitBoundaries) and normalise each Radiance Factor to the model phase curve from table file  PhaseCurveFit.dat  created in Step02: 
# this is called Radiance Factor Ratio (RFR). 
#
# The RFRs corresponds to the latitude-longitude wind advected boxes for each image. There is a large variation in the amount of individual pixels on the Venus
# disk that are in a box, due to variations in the time difference between the time of the image and the time of the VeRa-measurement and due to the observing 
# geometry. Most boxes have several hundreds of points, but some have less than 10. The minimum number of point can be set with  numberOfPointInLatitudeLongitudeBoxMinimum .
#
# Three plots can be created in each of three steps:
#  (1) all RFS of the selected orbits as a function of the VeRa-derived temperature;
#  (2) the average or median of the RFRs per orbit as a function of the VeRa-derived temperature;
#  (3) the temperature-binned average or median of the results in (2)
#
# In steps (2) and (3) calculate the least square linear fit to the results.
#
# The VeRa-derived temperatures can be corrected for the thermal tide, which is determined in Step04, by setting the  thermalTideCorrection  boolean.


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


# Extract the data of mission sections Extension 2, 3 and 4 + South Polar Dynamics Campaign (VMCOrbitID >= 1000).
VMCOrbitBoundaries = [1000, 2811]

# This is the minimum amount of points that need to be present in a latitude-longitude box for this data value to be included.
#  It is the  - #Points in box -  column in the  VMCSelectedImages.dat  file.
numberOfPointInLatitudeLongitudeBoxMinimum = 0

# Limit the phase angle of the data values to include.
phaseAngleLimit = 130

# Set here to either take the average of the median of the RFR values for each orbit.
radianceFactorRatiosStatistics = { 'Use average step2' : True, 
                                   'Use average step3' : False }

# Correct sub-string to create the plot file names and the plot titles.
statisticsStringStep2 = 'average'  if radianceFactorRatiosStatistics ['Use average step2'] else  'median'
statisticsStringStep3 = 'average'  if radianceFactorRatiosStatistics ['Use average step3'] else  'median'


# Temperature bin size for step 3.
temperatureBinSize = 2
# temperatureBinSize = 4
# temperatureBinSize = 8

# Boolean to control correction for thermal tide.
thermalTideCorrectionApply = False
thermalTideString = '_thermalTideCorrection'  if thermalTideCorrectionApply else  ''


# The first plot is all points, the second plot is the RFRs averaged (or median-ed) for each orbit, the third plot is with RFR-values per orbit binned in temperature bins.
plotParameters = { 'create plots' : [True, False, False],
                   'plot titles' : [ 'All points orbits {} - {}, \n # points in lat-lon box > {}, $\phi$ < {:3d}'.format ( VMCOrbitBoundaries [0], 
                                                                                                                           VMCOrbitBoundaries [1], 
                                                                                                                           numberOfPointInLatitudeLongitudeBoxMinimum, 
                                                                                                                           phaseAngleLimit ),
                                     '{} values per orbit (orbits {} - {})'.format ( statisticsStringStep2, 
                                                                                     VMCOrbitBoundaries [0], 
                                                                                     VMCOrbitBoundaries [1] ),
                                     'T-binned ({:3.1f}K wide), {} values (from {}) (orbits {} - {})'.format ( temperatureBinSize, 
                                                                                                               statisticsStringStep3, 
                                                                                                               statisticsStringStep2, 
                                                                                                               VMCOrbitBoundaries [0], 
                                                                                                               VMCOrbitBoundaries [1] ) ],
                   'plotFileName' : [ 'plots_phase_angle_lt_{:03d}_min-points-latlonbox_{}{}/RadianceFactorRatio_vs_Temperature_all_images.png'.
                                       format ( phaseAngleLimit, 
                                                numberOfPointInLatitudeLongitudeBoxMinimum,
                                                thermalTideString), 
                                      'plots_phase_angle_lt_{:03d}_min-points-latlonbox_{}{}/RadianceFactorRatio_vs_Temperature_orbits_{}.png'.
                                       format ( phaseAngleLimit, 
                                                numberOfPointInLatitudeLongitudeBoxMinimum, 
                                                thermalTideString,
                                                statisticsStringStep2 ),
                                      'plots_phase_angle_lt_{:03d}_min-points-latlonbox_{}{}/RadianceFactorRatio_vs_Temperature_binned_{}_from_{}_{}K.png'.
                                       format ( phaseAngleLimit, 
                                                numberOfPointInLatitudeLongitudeBoxMinimum,
                                                thermalTideString,
                                                statisticsStringStep3,
                                                statisticsStringStep2,
                                                temperatureBinSize ) ] }



HandyTools.createPathToFile ( 
 fullPath = os.path.join (VMCWorkBookDirectory, 'Step03', 'plots_phase_angle_lt_{:03d}_min-points-latlonbox_{}{}'.format ( phaseAngleLimit, 
                                                                                                                           numberOfPointInLatitudeLongitudeBoxMinimum,
                                                                                                                           thermalTideString ) ) )



# # Settings to extract the data of orbit 2805 and plot the individual Radiance Factor Ratios.
# # VMCOrbitBoundaries = [1789, 1789]
# VMCOrbitBoundaries = [2811, 2811]
# numberOfPointInLatitudeLongitudeBoxMinimum = 0
# phaseAngleLimit = 130
# plotParameters = { 'create plots' : [True, False, False],
#                    'plot titles' :  [ 'Orbit {} - {}, \n # points in lat-lon box > {}, $\phi$ < {:3d}'.format ( VMCOrbitBoundaries [0], 
#                                                                                                                 VMCOrbitBoundaries [1], 
#                                                                                                                 numberOfPointInLatitudeLongitudeBoxMinimum,
#                                                                                                                 phaseAngleLimit ) ],
#                    'plotFileName' : [ 'plots_phase_angle_lt_{:03d}_min-points-latlonbox_{}/RadianceFactorRatio_vs_Temperature_images_orbit_{}-{}.png'.format ( phaseAngleLimit, 
#                                                                                                                                                                   numberOfPointInLatitudeLongitudeBoxMinimum, 
#                                                                                                                                                                   VMCOrbitBoundaries [0], 
#                                                                                                                                                                   VMCOrbitBoundaries [1] ) ] }
# 
# HandyTools.createPathToFile ( fullPath = 'plots_phase_angle_lt_{:03d}_min-points-latlonbox_{}'.format (phaseAngleLimit, numberOfPointInLatitudeLongitudeBoxMinimum) )




# Load the data from the table files.
VMCSelectedImages = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step01', 'VMCSelectedImages.dat') )
numberOfVMCImages = len ( VMCSelectedImages [0][0] )
phaseCurve =  HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step02', 'PhaseCurveFit_i<84_e<81.dat') )
thermalTideCorrection = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step04','ThermalTideCorrection.dat') )


# Set plot parameters.
temperatureRange = [215, 250]
RFRatioRange = [0.6,1.6]


print ()
print ('- Step 1')
# Step 1
# Go through all the selected images in the  VMCSelectedImages.dat  table and collect all the valid data points from the selected images and orbits, normalise
#  them and plot.
radianceFactorRatiosInLatLonBox = []
dRadianceFactorRatiosInLatLonBox = []
VeRaTemperatures = []
dVeRaTemperatures = []
missionSectionColours = []
VMCOrbitIDs = []
for iImage in range (numberOfVMCImages):

    # The phase angle is binned in 1˚ bins, hence take the integer.
    phaseAngle = int ( VMCSelectedImages [0][14][iImage] )

    VMCOrbitID = VMCSelectedImages [0][0][iImage]
    numberOfPointInLatLonBox = VMCSelectedImages [0][15][iImage]

    # Select the images based on the orbits IDs, the phase angle and the minimum number of points in the latitude-longitude boxes.  
    if VMCOrbitID >= VMCOrbitBoundaries [0] and VMCOrbitID <= VMCOrbitBoundaries [1] and \
       phaseAngle <= phaseAngleLimit and \
       numberOfPointInLatLonBox >= numberOfPointInLatitudeLongitudeBoxMinimum:

        VMCOrbitIDs.append (VMCOrbitID)

        RadianceFactorInLatLonBox = VMCSelectedImages [0][16][iImage]
        dRadianceFactorInLatLonBox = VMCSelectedImages [0][17][iImage]
        
        # Find the index in the model phase curve  phaseCurve  (1˚ step) for this angle.
        iPhaseCurve = phaseAngle - int ( phaseCurve [0][0][0] )
        radianceFactorRatiosInLatLonBox.append ( RadianceFactorInLatLonBox / phaseCurve [0][1][iPhaseCurve] )
        
        # Take the "MaxMin RF = maximum - minimum of the Radiance Factor from 1000 gaussian noise experiments"   of the phase curve as the uncertainty.    
        dPhaseCurve = phaseCurve [0][4][iPhaseCurve]
        
        # The uncertainty in the   RadianceFactorInLatLonBox / phaseCurve  is derived from the formula of propagating erros for a division.
        dRadianceFactorRatiosInLatLonBox.append ( 
            np.sqrt ( ( dRadianceFactorInLatLonBox / phaseCurve [0][1][iPhaseCurve] ) ** 2 +
                      ( dPhaseCurve * RadianceFactorInLatLonBox / ( phaseCurve [0][1][iPhaseCurve] ) ** 2 ) ** 2 ) )
        

        # Determine the thermal tide amplitude, if the  thermalTideCorrection  boolean is True.
        thermalTideAmplitude = 0
        dThermalTideAmplitude = 0
        if thermalTideCorrectionApply:
                   
            iThermalTideCorrectionPerOrbit = 0     
            while iThermalTideCorrectionPerOrbit < len ( thermalTideCorrection [0][0] ) and \
                  thermalTideCorrection [0][0][iThermalTideCorrectionPerOrbit] != VMCOrbitID:
                  
                iThermalTideCorrectionPerOrbit += 1  
        
            thermalTideAmplitude = -thermalTideCorrection [0][5][iThermalTideCorrectionPerOrbit] 
            dThermalTideAmplitude = 0.1 #K (from Akiba et al. 2021)
#             print (VMCOrbitID, thermalTideAmplitude)
            
        
        VeRaTemperatures.append ( VMCSelectedImages [0][18][iImage] + thermalTideAmplitude )
        dVeRaTemperatures.append ( np.sqrt ( VMCSelectedImages [0][19][iImage]**2 + dThermalTideAmplitude**2 ) )
        missionSectionColours.append ( VMCTools.getColourForVEXMissionSection (VMCSelectedImages [1][0][iImage] ) )

        
        if VMCOrbitBoundaries [0] == VMCOrbitBoundaries [1]:
        
            print ('{:3d}˚: {:6.4f} / {:6.4f} = {:6.4f} +/- {:6.4f} (# points = {:3d})'.format ( phaseAngle, 
                                                                                                 RadianceFactorInLatLonBox, 
                                                                                                 phaseCurve [0][1][iPhaseCurve], 
                                                                                                 radianceFactorRatiosInLatLonBox [-1], 
                                                                                                 dRadianceFactorRatiosInLatLonBox [-1], 
                                                                                                 numberOfPointInLatLonBox ) )


# Create the plot for this step.
xLabelString = 'VeRa-derived temperature at 70km (K) with thermal tide correction'  if thermalTideCorrectionApply else   'VeRa-derived temperature at 70km (K)'
yLabelString = 'Radiance Factor Ratio'
if plotParameters ['create plots'][0]:
    
    plt.figure (1)
    plt.clf ()
    plt.scatter (VeRaTemperatures, radianceFactorRatiosInLatLonBox, s = 5, c = missionSectionColours)
    plt.xlim ( temperatureRange[0], temperatureRange [1] )
    plt.ylim ( RFRatioRange [0], RFRatioRange [1] )
    plt.xlabel (xLabelString)
    plt.ylabel (yLabelString)
    plt.title ( plotParameters ['plot titles'][0] )

    xStart = 216
    yStart = 1.55
    yJump = 0.05
    plt.text ( xStart, yStart, 'V1188 - V1522 (Extention 2)', c = 'purple', fontsize = 8 )
    plt.text ( xStart + 12, yStart, 'V1748 - V2301 (Extention 3)', c = 'black', fontsize = 8 )
    plt.text ( xStart, yStart - yJump, 'V2452 - V2639 (Extention 4)', c = 'grey', fontsize = 8 )
    plt.text ( xStart + 12, yStart -  yJump, 'V2776 - V2811 (South Polar Dynamics Campaign)', c = 'red', fontsize = 8 )

    plt.savefig ( os.path.join ( VMCWorkBookDirectory, 'Step03', plotParameters ['plotFileName'][0] ) )
    plt.close (1)

            

print ()
print ('- Step 2')
# Step 2
# Take all the images / data points from each orbit as collected in the first step and take the average value or the median  (controlled by the  
#  radianceFactorRatiosStatistics  boolean) of each orbit for a plot and for linear fitting.
if plotParameters ['create plots'][1]:


    VMCOrbitIDsUnique = list ( set (VMCOrbitIDs) )
    radianceFactorRatiosInLatLonBoxUnique = []
    dRadianceFactorRatiosInLatLonBoxUnique = []
    VeRaTemperaturesUnique = []
    dVeRaTemperaturesUnique = []
    missionSectionColoursUnique = []
    for iVMCOrbitIDsUnique, VMCOrbitIDUnique in enumerate (VMCOrbitIDsUnique):
    
        radianceFactorRatiosInOrbit = []
        dRadianceFactorRatiosInOrbit = []
        
        dRadianceFactorRatiosSquareSum = 0
        numberOfRadianceFactorRatios = 0
        for iVMCOrbitID, VMCOrbitID in enumerate (VMCOrbitIDs):
        
            if VMCOrbitID == VMCOrbitIDUnique:
                
                VeRaTemperatureAtOrbit = VeRaTemperatures [iVMCOrbitID]
                dVeRaTemperatureAtOrbit = dVeRaTemperatures [iVMCOrbitID]
                radianceFactorRatiosInOrbit.append ( radianceFactorRatiosInLatLonBox [iVMCOrbitID] )
                dRadianceFactorRatiosInOrbit.append ( dRadianceFactorRatiosInLatLonBox  [iVMCOrbitID] )
                dRadianceFactorRatiosSquareSum += dRadianceFactorRatiosInOrbit [-1] ** 2
                numberOfRadianceFactorRatios += 1 
 
    
        if numberOfRadianceFactorRatios:
            
            VeRaTemperaturesUnique.append (VeRaTemperatureAtOrbit)
            dVeRaTemperaturesUnique.append (dVeRaTemperatureAtOrbit)
            
            if radianceFactorRatiosStatistics ['Use average step2']:
            
                radianceFactorRatiosAverage = DataTools.getAverageVarAndSDPYtoCPP (radianceFactorRatiosInOrbit)
                
                radianceFactorRatiosInLatLonBoxUnique.append ( radianceFactorRatiosAverage [0] )   
                dRadianceFactorRatiosInLatLonBoxUnique.append ( max ( radianceFactorRatiosAverage [1], 
                                                                      np.sqrt (dRadianceFactorRatiosSquareSum) / numberOfRadianceFactorRatios ) )
            

            else:
            

                # Call the  getMedianAndQuantilesPYtoCPP  function of DataTools, with the uncertainties for each point and a 1000 random experiments:
                #  the presence of the uncertainties list triggers the estimation of the uncertainty in the median. 
                radianceFactorRatiosMedian = DataTools.getMedianAndQuantilesPYtoCPP ( radianceFactorRatiosInOrbit, 33, 67, 
                                                                                      uncertainties = dRadianceFactorRatiosInOrbit, 
                                                                                      numberOfUncertaintyExperiments = 1000 )
    
                radianceFactorRatiosInLatLonBoxUnique.append ( radianceFactorRatiosMedian [0] )
                dRadianceFactorRatiosInLatLonBoxUnique.append ( max ( ( radianceFactorRatiosMedian [2] - radianceFactorRatiosMedian [1] ) / 2,
                                                                      radianceFactorRatiosMedian [3] ) )
           

            missionSectionColoursUnique.append ( VMCTools.getColourForVEXMissionSection (VMCOrbitIDUnique) )
    
    
    
    radianceFactorRatiosInLatLonBoxUnique = np.asarray (radianceFactorRatiosInLatLonBoxUnique)
    dRadianceFactorRatiosInLatLonBoxUnique = np.asarray (dRadianceFactorRatiosInLatLonBoxUnique)
    VeRaTemperaturesUnique = np.asarray (VeRaTemperaturesUnique)
    dVeRaTemperaturesUnique = np.asarray (dVeRaTemperaturesUnique)


    # Create the plot.
    plt.figure (2)
    plt.clf ()

    plt.scatter (VeRaTemperaturesUnique, radianceFactorRatiosInLatLonBoxUnique, c = missionSectionColoursUnique)
    HandyTools.plotErrorBars ( xValues = VeRaTemperaturesUnique, 
                               xErrors = dVeRaTemperaturesUnique, 
                               yValues = radianceFactorRatiosInLatLonBoxUnique, 
                               yErrors = dRadianceFactorRatiosInLatLonBoxUnique, 
                               colours = missionSectionColoursUnique )

    plt.xlim ( temperatureRange[0], temperatureRange [1] )
    plt.ylim ( RFRatioRange [0], RFRatioRange [1] )

    plt.xlabel (xLabelString)
    plt.ylabel (yLabelString)
    plt.title ( plotParameters ['plot titles'][1] )

    
    fit = DataTools.linearLeastSquare (VeRaTemperaturesUnique, radianceFactorRatiosInLatLonBoxUnique)
    x = 220 + np.arange (2) * 25
    y = fit [0] * x + fit [1]
    print ('average / median  - fit:', fit)
    plt.plot (x, y, label = 'RF = {:7.5f} ($\pm$ {:7.5f}) T + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f}'.format ( fit [0], fit [2], fit [1], fit [3], fit [4] ))
    plt.legend ( loc = 'upper left', fontsize = 9 )

    xStart = 216
    yStart = 1.45
    yJump = 0.05
    plt.text ( xStart, yStart, 'V1188 - V1522 (Extention 2)', c = 'purple', fontsize = 8 )
    plt.text ( xStart + 12, yStart, 'V1748 - V2301 (Extention 3)', c = 'black', fontsize = 8 )
    plt.text ( xStart, yStart - yJump, 'V2452 - V2639 (Extention 4)', c = 'grey', fontsize = 8 )
    plt.text ( xStart + 12, yStart -  yJump, 'V2776 - V2811 (South Polar Dynamics Campaign)', c = 'red', fontsize = 8 )

    plt.savefig ( os.path.join ( VMCWorkBookDirectory, 'Step03', plotParameters ['plotFileName'][1] ) )
    plt.close (2)


        
print ()
print ('- Step 3')
# Step 3
# 
if plotParameters ['create plots'][2]:

    temperatureLowerLimit = 220
    temperatureUpperLimit = 250
    numberOfBins = 2 * int ( ( temperatureUpperLimit - temperatureLowerLimit ) / temperatureBinSize )
    VeRaTemperaturesBins = temperatureLowerLimit + np.arange (numberOfBins) * temperatureBinSize 
    
    VeRaTemperaturesBinned = []
    radianceFactorRatiosInLatLonBoxBinned = []
    dRadianceFactorRatiosInLatLonBoxBinned = []
    for VeRaTemperatureBin in VeRaTemperaturesBins:
    
        binLowerBorder = VeRaTemperatureBin - temperatureBinSize / 2
        binUpperBorder = VeRaTemperatureBin + temperatureBinSize / 2
        iInBin = np.where ( np.logical_and ( VeRaTemperaturesUnique >= binLowerBorder, VeRaTemperaturesUnique < binUpperBorder) )[0]
    
        if len (iInBin):
        
            print ( '  # points bin between {}K and {}K = {}'.format (binLowerBorder, binUpperBorder, len (iInBin) ) )
        
            if radianceFactorRatiosStatistics ['Use average step3']:

                radianceFactorRatioInLatLonBoxBinned = DataTools.getAverageVarAndSDPYtoCPP ( radianceFactorRatiosInLatLonBoxUnique [iInBin] )
                dRadianceFactorRatioInLatLonBoxBinned = \
                 max ( np.sqrt ( np.sum ( dRadianceFactorRatiosInLatLonBoxUnique [iInBin] ** 2 ) ) / len (iInBin), 
                       radianceFactorRatioInLatLonBoxBinned [1] ) 


            else:

                radianceFactorRatioInLatLonBoxBinned = \
                 DataTools.getMedianAndQuantilesPYtoCPP ( radianceFactorRatiosInLatLonBoxUnique [iInBin], 33, 67,
                                                          uncertainties = dRadianceFactorRatiosInLatLonBoxUnique  [iInBin], numberOfUncertaintyExperiments = 1000 )

                dRadianceFactorRatioInLatLonBoxBinned = \
                 max ( ( radianceFactorRatioInLatLonBoxBinned [2] - radianceFactorRatioInLatLonBoxBinned [1] ) / 2,
                        radianceFactorRatioInLatLonBoxBinned [3] )
        
        
            # Add weights to bins based on the number of values in each bin. 
            for iAdd in iInBin:
    
                VeRaTemperaturesBinned.append (VeRaTemperatureBin)
                radianceFactorRatiosInLatLonBoxBinned.append ( radianceFactorRatioInLatLonBoxBinned [0] )
                dRadianceFactorRatiosInLatLonBoxBinned.append ( dRadianceFactorRatioInLatLonBoxBinned )
            

    # Create the plot.    
    plt.figure (3)
    plt.clf ()
    plt.scatter (VeRaTemperaturesBinned, radianceFactorRatiosInLatLonBoxBinned)
    HandyTools.plotErrorBars (VeRaTemperaturesBinned, radianceFactorRatiosInLatLonBoxBinned, yErrors = dRadianceFactorRatiosInLatLonBoxBinned, colours = 'darkblue')
    plt.xlim ( temperatureRange[0], temperatureRange [1] )
    plt.ylim ( RFRatioRange [0], RFRatioRange [1] )
    plt.xlabel (xLabelString)
    plt.ylabel ( 'Radiance Factor Ratio (T-binned {:3.1f}K wide)'.format (temperatureBinSize) )
    plt.title ( plotParameters ['plot titles'][2], fontsize = 10 )

    
    fit = DataTools.linearLeastSquare(VeRaTemperaturesBinned, radianceFactorRatiosInLatLonBoxBinned)
    x = 220 + np.arange (2) * 25
    y = fit [0] * x + fit [1]
    print ()
    print ('binned - fit:', fit)
    plt.plot (x, y, label = 'RF = {:7.5f} ($\pm$ {:7.5f}) T + {:7.5f} ($\pm$ {:7.5f}) | $r^2$ = {:5.3f} '.format ( fit [0], fit [2], fit [1], fit [3], fit [4] ))
    plt.legend ( loc = 'upper left', fontsize = 9 )

    plt.savefig ( plotParameters ['plotFileName'][2] )
    plt.close (3)
 