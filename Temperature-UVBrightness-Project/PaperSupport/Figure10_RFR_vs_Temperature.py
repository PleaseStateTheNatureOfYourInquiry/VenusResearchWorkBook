# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241112

# Create the figures of Pearson and Spearman Correlation Coefficients for RFR vs Temperature (z), as a function of the altitude z.

# Standard imports.
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('..') ) 
from analysisConfiguration import *


correctionType = 'uncorrected'
# correctionType = 'normalised'


RFRvsT = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_TVeRa50-80kmAltitude.dat') )
RFRvsS = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'RadianceFactorRatio_vs_SVeRa50-80kmAltitude.dat') )


latitudesRFRvsT = [ HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'T_Correlation_Latitudes_0_-40_{}.dat'.format (correctionType) ) ) ]
latitudesRFRvsT.append ( HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'T_Correlation_Latitudes_-40_-60_{}.dat'.format (correctionType) ) ) )
latitudesRFRvsT.append ( HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'T_Correlation_Latitudes_-60_-90_{}.dat'.format (correctionType) ) ) )


latitudeDependence = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'TVeRa_vs_latitude_statistics_50-80kmAltitude.dat') )


latitudesRFRvsS = [ HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'S_Correlation_Latitudes_0_-40.dat') ) ]
latitudesRFRvsS.append ( HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'S_Correlation_Latitudes_-40_-60.dat') ) )
latitudesRFRvsS.append ( HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', 'S_Correlation_Latitudes_-60_-90.dat') ) )


iLatitudes = []
colours = ['green', 'red', 'black']
labels = ['   0˚ / -40˚', '-40˚ / -60˚', '-60˚ / -90˚']

iValidOrbits = np.where ( RFRvsT [0][0] > 1188 )[0]

iLatitude = np.where ( np.logical_and ( RFRvsT [0][4][iValidOrbits] <= 0, RFRvsT [0][4][iValidOrbits] > -40 ) )[0]
iLatitudes.append (iValidOrbits [iLatitude])

iLatitude = np.where ( np.logical_and ( RFRvsT [0][4][iValidOrbits] <= -40, RFRvsT [0][4][iValidOrbits] > -60 ) )[0]
iLatitudes.append (iValidOrbits [iLatitude])

iLatitude = np.where ( np.logical_and ( RFRvsT [0][4][iValidOrbits] <= -60, RFRvsT [0][4][iValidOrbits] > -90 ) )[0]
iLatitudes.append (iValidOrbits [iLatitude])


altitudes = [67, 71, 79]

for altitude in altitudes:

    iColumn = 5 + (altitude - 50) * 2
        
    plt.figure (1)
    plt.clf ()
    
    for iLatitudeSet in range (3):
        
        VeRaTemperatures = RFRvsT [0][iColumn][ iLatitudes [iLatitudeSet] ]
        dVeRaTemperatures = RFRvsT [0][iColumn + 1][ iLatitudes[iLatitudeSet] ]

        spearmanCC = latitudesRFRvsT [iLatitudeSet][0][3][altitude - 50]
        dSpearmanCC = latitudesRFRvsT [iLatitudeSet][0][4][altitude - 50]
     
     
        if correctionType == 'normalised':

            denominator = latitudeDependence [0][1][altitude - 50] * RFRvsT [0][4][ iLatitudes [iLatitudeSet] ] + latitudeDependence [0][3][altitude - 50]
            VeRaTemperatures = RFRvsT [0][iColumn][ iLatitudes [iLatitudeSet] ] / denominator

            dVeRaTemperatures = \
             np.sqrt ( (dVeRaTemperatures / denominator) ** 2 + 
                       (latitudeDependence [0][2][altitude - 50] * RFRvsT [0][iColumn][ iLatitudes [iLatitudeSet] ] * RFRvsT [0][iColumn][ iLatitudes [iLatitudeSet] ] / denominator ** 2) ** 2 +
                       (latitudeDependence [0][4][altitude - 50] * RFRvsT [0][iColumn][ iLatitudes [iLatitudeSet] ] / denominator ** 2) ** 2 )
        

        if correctionType == 'subtracted': 
                 
            VeRaTemperatures = RFRvsT [0][iColumn][ iLatitudes [iLatitudeSet] ] - \
             ( latitudeDependence [0][1][altitude - 50] * RFRvsT [0][4][ iLatitudes [iLatitudeSet] ] + latitudeDependence [0][3][altitude - 50] )

            dVeRaTemperatures = np.sqrt ( dVeRaTemperatures ** 2 + 
                                          ( latitudeDependence [0][2][altitude - 50] * RFRvsT [0][4][ iLatitudes [iLatitudeSet] ] ) ** 2 +
                                            latitudeDependence [0][4][altitude - 50] ** 2 )

        
        plt.scatter ( VeRaTemperatures, RFRvsT [0][1][ iLatitudes [iLatitudeSet] ], color = colours [iLatitudeSet], 
                      label = labels [iLatitudeSet] + ': Spearman CC = {:5.2f} ± {:5.3f}'.format (spearmanCC, dSpearmanCC) )

        HandyTools.plotErrorBars ( VeRaTemperatures, RFRvsT [0][1][ iLatitudes [iLatitudeSet] ], 
                                   yErrors = RFRvsT [0][2][ iLatitudes [iLatitudeSet] ], colours = colours [iLatitudeSet], alpha = 0.1 )

        HandyTools.plotErrorBars ( VeRaTemperatures, RFRvsT [0][1][ iLatitudes [iLatitudeSet] ], 
                                   xErrors = dVeRaTemperatures, 
                                   yErrors = RFRvsT [0][2][ iLatitudes [iLatitudeSet] ], colours = colours [iLatitudeSet], alpha = 0.1 )
    
    plt.legend (fontsize = 8)

    plt.ylabel ('Radiance Ratio Factor')
    
    
    if correctionType == 'normalised':

        plt.xlabel ('Normalised Temperature')
 
        plt.title ( '(10b) RFR versus Normalised Temperature at {}km'.format (altitude) )
        plt.savefig ('Figure10_RFR_vs_T_{}km_normalised.png'.format (altitude))
 
 
    elif correctionType == 'uncorrected':

        plt.xlabel ('Temperature (K)')

        plt.title ( '(10a) RFR versus Temperature at {}km'.format (altitude) )
        plt.savefig ('Figure10_RFR_vs_T_{}km_uncorrected.png'.format (altitude))
    
    
    plt.close ()





