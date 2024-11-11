# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241104

# Create the figures of Pearson and Spearman Correlation Coefficients for RFR vs Temperature (z), as a function of the altitude z.

# Standard imports.
import os
import sys

import matplotlib.pyplot as plt

# Custom imports.
from HandyTools import HandyTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


ST_TableFiles = [ [
 'S_Correlation_All_Latitudes.dat',
 'S_Correlation_Latitudes_-39.69_-14.97.dat',
 'S_Correlation_Latitudes_-59.14_-43.12.dat',
 'S_Correlation_Latitudes_-83.8_-62.06.dat'
],
[
'T_Correlation_All_Latitudes.dat',
'T_Correlation_Latitudes_-39.69_-14.97.dat',
'T_Correlation_Latitudes_-59.14_-43.12.dat',
'T_Correlation_Latitudes_-83.8_-62.06.dat'
] ]

plotFileNames = ['S_Correction', 'T_correlation']

labels = [ '(-90˚, 0˚)', '(-39˚,-15˚)', '(-59˚,-43˚)', '(-84˚, -62˚)' ]
xyLabels = [ 'Altitude km)', 'Pearson Correlation Coefficient', 'Spearman Correlation Coefficient' ]
titles = [ 'UV-Brightness vs VeRa Static Stabiity at Altitude', 'UV-Brightness vs VeRa Temperature at Altitude' ]

colours = ['blue', 'green', 'red', 'black']

# The Pearson or Spearman correlation coefficient has values between -1 and +1. Moderate correlation is when the coefficient has values < -0.5 or > 0.5.
moderateCorrelationLevel = 0.5

for iST_TableFile in range (2):

    plt.figure (1)
    plt.clf ()
    plt.xlabel ( xyLabels [0] )
    plt.ylim (-1,1)
    
    xmin, xmax = 50, 80
    
    plt.hlines (xmin = xmin, xmax = xmax, y = moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
    plt.fill_between ( x = [xmin, xmax], y1 = moderateCorrelationLevel, y2 = 1.0 , color = 'green', alpha = 0.1 )
    
    plt.hlines (xmin = xmin, xmax = xmax, y = -moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
    plt.fill_between ( x = [xmin, xmax], y1 = -moderateCorrelationLevel, y2 = -1.0 , color = 'green', alpha = 0.1 )
    
    
    
    plt.figure (2)
    plt.clf ()
    plt.xlabel ( xyLabels [0] )
    plt.ylim (-1,1)
    
    plt.hlines (xmin = xmin, xmax = xmax, y = moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
    plt.fill_between ( x = [xmin, xmax], y1 = moderateCorrelationLevel, y2 = 1.0 , color = 'green', alpha = 0.1 )
    
    plt.hlines (xmin = xmin, xmax = xmax, y = -moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
    plt.fill_between ( x = [xmin, xmax], y1 = -moderateCorrelationLevel, y2 = -1.0 , color = 'green', alpha = 0.1 )
    
    
    for iTableFile in range (0,4):
    
        tableFile = ST_TableFiles [iST_TableFile][iTableFile] 
      
        tableContent = HandyTools.readTable ( os.path.join ('..', tableFile) )
        
        plt.figure (1)
        plt.scatter ( tableContent [0][0], tableContent [0][1], c = colours [iTableFile], label = labels [iTableFile] )
        plt.plot ( tableContent [0][0], tableContent [0][1], c = colours [iTableFile] )
        HandyTools.plotErrorBars ( tableContent [0][0], tableContent [0][1], yErrors = tableContent [0][2], colours = colours [iTableFile] )
        
        plt.figure (2)
        plt.scatter ( tableContent [0][0], tableContent [0][3], c = colours [iTableFile], label = labels [iTableFile] )
        plt.plot ( tableContent [0][0], tableContent [0][3], c = colours [iTableFile] )
        HandyTools.plotErrorBars ( tableContent [0][0], tableContent [0][3], yErrors = tableContent [0][4], colours = colours [iTableFile] )
    
    
    
    plt.figure (1)
    plt.ylabel ( xyLabels [1] )
    plt.title ( titles [iST_TableFile] )
    plt.legend ()
    plt.savefig ( os.path.join ( VMCWorkBookDirectory, 'Step06', '{}_Pearson.png'.format ( plotFileNames [iST_TableFile] ) ) )
    
    plt.figure (2)
    plt.ylabel ( xyLabels [2] )
    plt.title ( titles [iST_TableFile] )
    plt.legend ()
    plt.savefig ( os.path.join ( VMCWorkBookDirectory, 'Step06', '{}_Spearman.png'.format ( plotFileNames [iST_TableFile] ) ) )
    
    plt.close ()







