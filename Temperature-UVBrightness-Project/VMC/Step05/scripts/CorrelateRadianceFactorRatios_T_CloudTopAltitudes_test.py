# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240928

# Analysis of the cloud top temperatures vs radiance factor ratios.

# Chose the desired limitation in orbitIDVMC.

# Standard imports.
import os
import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import numpy as np
import matplotlib.pyplot as plt


# Custom imports.
from HandyTools import HandyTools
from DataTools import DataTools


# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *



tableContent = HandyTools.readTable ('../cloudTopTemperature_vs_RadianceFactorRatio.dat')
numberOfDataPoints = len ( tableContent[0][0] )

RFRRange = [0.7, 1.4]
RFRStep = 0.1
numberOfRFRSteps = int ( ( RFRRange [1] - RFRRange [0] ) / RFRStep + 0.5 )

temperatureRange = [200,240]
temperatureStep = 5
numberOfTemperatureCells = int (  ( temperatureRange [1] - temperatureRange [0] ) / temperatureStep + 0.5 )

contigencyTable = np.zeros ( (numberOfRFRSteps, numberOfTemperatureCells), dtype = int )

for iDataPoint in range (numberOfDataPoints):

    iRFR = int ( ( tableContent [0][5][iDataPoint] -  RFRRange [0] ) / RFRStep )
    iTemperature = int ( ( tableContent [0][0][iDataPoint] - temperatureRange [0] ) / temperatureStep )
    
#     print (tableContent [0][5][iDataPoint], iRFR)
#     print (tableContent [0][0][iDataPoint], iTemperature)
#     print ()
    contigencyTable [iRFR][iTemperature] += 1
    

p_rows = [ np.sum ( contigencyTable [iRow] ) / numberOfDataPoints   for iRow in range (numberOfRFRSteps) ]
p_columns = [ np.sum ( contigencyTable [:,iColumn] ) / numberOfDataPoints  for iColumn in range (numberOfTemperatureCells) ]


chi_square = 0
for iRow in range (numberOfRFRSteps):

    for iColumn in range (numberOfTemperatureCells):
    
        pProduct = p_rows [iRow] * p_columns [iColumn]
        term = (contigencyTable [iRow][iColumn] / numberOfDataPoints - pProduct)

        if pProduct:
                 
            chi_square += term ** 2 / pProduct 
        
chi_square *= numberOfDataPoints

print (' Degrees of freedom: (numberOfRFRSteps - 1) x (numberOfTemperatureCells - 1) = {:2d}'.format ( (numberOfRFRSteps - 1) * (numberOfTemperatureCells - 1) ) )
print (' chi_square = {:5.2f}'.format (chi_square) )

# https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test#Testing_for_statistical_independence
# https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm








