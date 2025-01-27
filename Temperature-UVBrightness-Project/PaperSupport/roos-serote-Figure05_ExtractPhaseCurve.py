# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20250120

# From the table created by  CreatePhaseCurveTable.py  in this same Step02 of the process, extract a binned phase curve. 
# The bin size can be set, default value is 1˚ (note, the PhaseCurve.dat table is ordered by increasing phase angle).
# 

# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt


# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools

from VMCTools import VMCTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('..') ) 
from analysisConfiguration import *


incidence_emission_angle_String = 'i<84_e<81'

phaseCurveFitFileName = os.path.join ( VMCWorkBookDirectory, 'Step02','PhaseCurve_{}.dat'.format (incidence_emission_angle_String) )


phaseCurveData = HandyTools.readTable (phaseCurveFitFileName)
numberOfPhaseCurvePoints = len (phaseCurveData [0][1])

# Set binsize and initialise the binned  phaseCurveBinned  list and the corresponding  phaseAnglesBinned  list.
binSize = 1 # ˚


# All the different settings to produce intermediate and final results for the phase curve.
selectionParameterSets =  [ 
    
    # Setting for the plots with all data not in bins.
    [ 'V1000', 130, '   Figure05a_PhaseCurveExtension2-4+SPDC_PhaseAngleLT130dgr.png', 'EXT2-4 + SPDC & phase angles < 130˚', False ],

    # Setting for the plots with binned data.
    [ 'V1000', 130, 'Figure05b_PhaseCurveBinnedExtension2-4+SPDC_PhaseAngleLT130dgr.png', 'EXT2-4 + SPDC & phase angles < 130˚ (binned {}˚)'.format (binSize), True ]
 
]



figure = plt.figure (1)
figure.set_figheight (6)
figure.set_figwidth (15)
figure.clf ()
figure.subplots_adjust (left = 0.05, right = 0.95)

axis1 = plt.subplot2grid ( shape = (1, 2), loc = (0, 0), colspan = 1 )
axis2 = plt.subplot2grid ( shape = (1, 2), loc = (0, 1), colspan = 1 )


# Go through the different parameter sets.
for iSelectionParameters, selectionParameters in enumerate (selectionParameterSets):

    if iSelectionParameters == 0:
    
        axis = axis1
    
    elif iSelectionParameters == 1:
    
        axis = axis2


    binRadianceFactors = selectionParameters [-1]

    phaseCurveBinned = []
    phaseCurveBinnedStandardDeviation = []
    numberOfRadianceFactorsPerBin = []
    
    phaseAnglesBinned = [ int ( phaseCurveData [0][1][0] )  if binRadianceFactors else  phaseCurveData [0][1][0] ]
    radianceFactorsFactorsInBin = [ phaseCurveData [0][2][0] ]
    standardDeviationRadianceFactorsInBin = [ phaseCurveData [0][3][0] ]
    
    if not binRadianceFactors:
    
        coloursPerDataSection =  [ VMCTools.getColourForVEXMissionSection ( phaseCurveData [1][0][0] ) ]
        
    else:
    
        coloursPerDataSection = [ 'blue' ]



    iPhaseAngle = 1
    while iPhaseAngle < numberOfPhaseCurvePoints:
    
    
        if phaseCurveData [1][0][iPhaseAngle].split ('_')[0] >= selectionParameters [0]:
        
            phaseAngle = int ( phaseCurveData [0][1][iPhaseAngle] )  if binRadianceFactors else  phaseCurveData [0][1][iPhaseAngle]
            
            
            if phaseAngle <= selectionParameters [1]:
            
                # Collect the radiance values in the current phase angles bin.
                if binRadianceFactors and ( phaseAngle - phaseAnglesBinned [-1] ) < binSize:
                
                    radianceFactorsFactorsInBin.append ( phaseCurveData [0][2][iPhaseAngle] * 0.07738 / phaseCurveData [0][8][iPhaseAngle] )
                    standardDeviationRadianceFactorsInBin.append ( phaseCurveData [0][3][iPhaseAngle] )
                    
                    
                # New bin has been found, calculate the final value of the previous bin and reinitialise for the new bin.
                else:
                
                    numberOfRadianceFactorsPerBin.append ( len (radianceFactorsFactorsInBin) )
                    averageRadianceFactorInBin = DataTools.getAverageVarAndSDPYtoCPP (radianceFactorsFactorsInBin) 
            
                    phaseCurveBinned.append ( averageRadianceFactorInBin [0] )
                    
                    
                    #  First, the uncertainty can be assessed through: 
                    #   (sigma_x)^2 = (sigma_u)^2 * (dx / du)^2 + (sigma_v)^2 * (dx / dv)^2 + .... 
                    #   where x is the average of N values (u, v, ...), hence x = (u + v + ...) / N and thus dx / du = 1 / N 
                    # (see 3.14 in Data Reduction and Error Analysis for the Physical Science y P.R. Bevington and D.K. Robinson)
                    uncertaintyPhaseCurveValue = np.sqrt ( np.sum ( ( np.asarray (standardDeviationRadianceFactorsInBin) / numberOfRadianceFactorsPerBin [-1] ) ** 2 ) )

                    # The final uncertainty for each binned value is the maximum of the  uncertaintyPhaseCurveValue  and the standard deviation of the average.
                    phaseCurveBinnedStandardDeviation.append ( max ( uncertaintyPhaseCurveValue, averageRadianceFactorInBin [1] ) )


                    # Colours are coded per mission section for non-binned data.
                    if not binRadianceFactors:
                    
                        coloursPerDataSection.append (  VMCTools.getColourForVEXMissionSection ( phaseCurveData [1][0][iPhaseAngle] ) )

                    # Colours cannot be coded for binned data, as in each bin there are data points from different mission sections.                        
                    else:
                    
                        coloursPerDataSection.append ('blue')
                    
               
                    # Re-initialise.
                    phaseAnglesBinned.append ( phaseAngle )
#                     phaseAnglesBinned.append ( int ( phaseCurveData [0][1][iPhaseAngle] )  if binRadianceFactors else  phaseCurveData [0][1][iPhaseAngle] ) 
                    radianceFactorsFactorsInBin = [ phaseCurveData [0][2][iPhaseAngle] ]
                    standardDeviationRadianceFactorsInBin = [ phaseCurveData [0][3][iPhaseAngle] ]        
        
        
        iPhaseAngle += 1
    
    
    
    # Calculate the values for the final bin.
    numberOfRadianceFactorsPerBin.append ( numberOfRadianceFactorsPerBin [-1] )
    averageRadianceFactorInBin = DataTools.getAverageVarAndSDPYtoCPP (radianceFactorsFactorsInBin) 
    
    phaseCurveBinned.append ( averageRadianceFactorInBin [0] )
    numberOfPhaseCurveBinnedPoints = len (phaseCurveBinned)
    

    # Calculate the uncertainty in the value of each bin.
    uncertaintyPhaseCurveValue = np.sqrt ( np.sum ( ( np.asarray (standardDeviationRadianceFactorsInBin) / numberOfRadianceFactorsPerBin [-1] ) ** 2 ) )
    phaseCurveBinnedStandardDeviation.append ( max ( uncertaintyPhaseCurveValue, averageRadianceFactorInBin [1] ) )
    
    
    # Fit the phase curve with a quadratic polynomial.
    phaseAngleUpperLimit = selectionParameters [1]  if selectionParameters [1] < phaseAnglesBinned [-1] else  phaseAnglesBinned [-1]
    polynomialRegression = np.polynomial.polynomial.Polynomial.fit ( phaseAnglesBinned, phaseCurveBinned, 2, domain = [ phaseAnglesBinned [0], phaseAngleUpperLimit ] )

    # Array [a, b, c] of the  = a + bx * cx^2 (see NumPy manual)
    polynomialCoefficients = polynomialRegression.convert ().coef

    # Calculate the r-squared value, an indication for the goodness of the fit.
    phaseAngleRegression = polynomialRegression ( np.asarray (phaseAnglesBinned) )
    phaseAngleDataAverage = np.sum (phaseCurveBinned) / len (phaseCurveBinned)
    squaredSumRegression = np.sum ( ( phaseAngleRegression - phaseAngleDataAverage ) ** 2 )
    squaredSumTotal = np.sum ( ( phaseCurveBinned - phaseAngleDataAverage ) ** 2 )
    rSquared = squaredSumRegression / squaredSumTotal


    # Create and save the plot.
#     plt.figure (iSelectionParameters + 1)
#     plt.clf ()
    
    
    # In order to assess the uncertainty in the fitted curve, add gaussian noise, with a standard deviation as determined from the individual values per bin,
    #  to the values of each phase angle bins and fit a new quadratic curve.

    # All phase angles in the range without jumps.
    phaseAnglesBinnedFullRange = phaseAnglesBinned [0] + np.arange ( phaseAnglesBinned [-1] - phaseAnglesBinned [0] + 1 )

    # Perform 1000 noise adding experiments.
    polynomialRegressionPerIteration = []
    regressionPhaseCurves = []
    for iRandomGaussianNoiseExperiment in range (1000):
    
        # Create a new phase curve, adding gaussian noise to the values in each of the phase angle bins,  
        phaseCurveBinnedRandomised = [ np.random.normal( phaseCurveBinned [iPhaseAngleBin], phaseCurveBinnedStandardDeviation [iPhaseAngleBin], 1)[0]  
                                       for iPhaseAngleBin in range (numberOfPhaseCurveBinnedPoints) ]
    
        # Store the resulting fit for each experiment
        polynomialRegressionPerIteration.append ( 
         np.polynomial.polynomial.Polynomial.fit ( phaseAnglesBinned, phaseCurveBinnedRandomised, 2, domain = [ phaseAnglesBinned [0], phaseAngleUpperLimit ] ) )
        regressionPhaseCurves.append ( polynomialRegressionPerIteration [-1] ( phaseAnglesBinnedFullRange ) )
    
        # Plot each new curve in transparent grey.
        axis.plot ( phaseAnglesBinnedFullRange, regressionPhaseCurves [-1], color = 'grey', alpha = 0.05 )
        
        
    axis.scatter (phaseAnglesBinned, phaseCurveBinned, s = 10, color = coloursPerDataSection)    
    axis.plot (phaseAnglesBinned, polynomialRegression ( np.asarray (phaseAnglesBinned) ), color = 'orange')
    axis.set_xlim (0,150)
    axis.set_ylim (0,2.5)

    axis.set_xlabel ('Phase Angle $\phi$ (˚)')
    axis.set_ylabel ('Radiance Factor')

    axis.legend ( [ 'RF = {:8.6f}$\phi^2$ + {:7.4f}$\phi$ + {:7.3f}  |  $r^2$ = {:5.3f}'.format ( 
                   polynomialCoefficients [2], polynomialCoefficients [1], polynomialCoefficients [0], rSquared ) ], loc = 'upper left' )


    # When plotting not-binned data, add the colour coding text to the plot.  
    if not binRadianceFactors:
        
        xStart = 10
        yStart = 2.
        yJump = 0.14
        axis.text ( xStart, yStart, 'V1188 - V1522 (Extention 2)', c = 'purple' )
        axis.text ( xStart, yStart - yJump, 'V1748 - V2301 (Extention 3)', c = 'black' )
        axis.text ( xStart, yStart - 2 * yJump, 'V2452 - V2639 (Extention 4)', c = 'grey' )
        axis.text ( xStart, yStart - 3 * yJump, 'V2776 - V2811 (South Polar Dynamics Campaign)', c = 'red' )
            
    
    axis.set_title ( selectionParameters [3] )
    
    
        
plt.savefig ( 'roos-serote-Figure5ab_PhaseCurveExtension2-4+SPDC_PhaseAngleLT130dgr.png', dpi = 300 )
    



