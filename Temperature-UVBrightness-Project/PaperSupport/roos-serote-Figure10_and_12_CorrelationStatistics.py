# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20250121

# Create the figures of Pearson and Spearman Correlation Coefficients for RFR vs Temperature (z), as a function of the altitude z.

# Standard imports.
import os
import sys

import matplotlib.pyplot as plt

# Custom imports.
from HandyTools import HandyTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('..') ) 
from analysisConfiguration import *


ST_TableFiles = [
[ 'S_Correlation_All_Latitudes.dat',
  'S_Correlation_Latitudes_0_-40.dat',
  'S_Correlation_Latitudes_-40_-60.dat',
  'S_Correlation_Latitudes_-60_-90.dat' ],
[ 'T_Correlation_All_Latitudes.dat',
  'T_Correlation_Latitudes_0_-40_uncorrected.dat',
  'T_Correlation_Latitudes_-40_-60_uncorrected.dat',
  'T_Correlation_Latitudes_-60_-90_uncorrected.dat' ],
[ 'T_Correlation_All_Latitudes_normalised.dat',
  'T_Correlation_Latitudes_0_-40_normalised.dat',
  'T_Correlation_Latitudes_-40_-60_normalised.dat',
  'T_Correlation_Latitudes_-60_-90_normalised.dat' ],


]

plotFileNames = ['Figure12ab_S_Correction', 'Figure10a_T_correlation_uncorrected', 'Figure10b_T_correlation_normalised']

labels = [ '(0˚, -90˚) - 56 data points', '(0˚,-40˚) - 9 data points', '(-40˚,-60˚) - 30 data points', '(-60˚, -90˚) - 17 data points' ]
xyLabels = [ 'Altitude km)', 'Pearson Correlation Coefficient', 'Spearman Correlation Coefficient' ]
titles = [ 'UV-Brightness vs VeRa Static Stabiity', '(a) UV-Brightness vs VeRa Temperature', '(b) UV-Brightness vs VeRa Temperature (normalised)' ]

colours = ['blue', 'green', 'red', 'black']

# The Pearson or Spearman correlation coefficient has values between -1 and +1. Moderate correlation is when the coefficient has values < -0.5 or > 0.5.
moderateCorrelationLevel = 0.5


plt.figure (2)

# figure = plt.figure (1)
# figure.set_figheight (6)
# figure.set_figwidth (15)
# figure.clf ()
# figure.subplots_adjust (left = 0.05, right = 0.95)
# 
# axis1 = plt.subplot2grid ( shape = (1, 2), loc = (0, 0) )
# axis2 = plt.subplot2grid ( shape = (1, 2), loc = (0, 1) )


for iST_TableFile in range (3):

#     plt.figure (1)
#     axis1.clear ()
#     axis1.set_xlabel ( xyLabels [0] )
#     axis1.set_ylim (-1,1)
#     
    xmin, xmax = 50, 80
#     
#     axis1.hlines (xmin = xmin, xmax = xmax, y = moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
#     axis1.fill_between ( x = [xmin, xmax], y1 = moderateCorrelationLevel, y2 = 1.0 , color = 'green', alpha = 0.1 )
#     
#     axis1.hlines (xmin = xmin, xmax = xmax, y = -moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
#     axis1.fill_between ( x = [xmin, xmax], y1 = -moderateCorrelationLevel, y2 = -1.0 , color = 'green', alpha = 0.1 )
    
    
    
#     plt.figure (2)
    plt.clf ()
    plt.xlabel ( xyLabels [0] )
    plt.ylim (-1,1)
    
    plt.hlines (xmin = xmin, xmax = xmax, y = moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
    plt.fill_between ( x = [xmin, xmax], y1 = moderateCorrelationLevel, y2 = 1.0 , color = 'green', alpha = 0.1 )
    
    plt.hlines (xmin = xmin, xmax = xmax, y = -moderateCorrelationLevel, color = 'green', linewidths = 1, alpha = 0.5)
    plt.fill_between ( x = [xmin, xmax], y1 = -moderateCorrelationLevel, y2 = -1.0 , color = 'green', alpha = 0.1 )
    
    
    for iTableFile in range (1,4):
    
        tableFile = ST_TableFiles [iST_TableFile][iTableFile] 
      
        tableContent = HandyTools.readTable ( os.path.join (VMCWorkBookDirectory, 'Step06', tableFile) )
        
#         plt.figure (1)
#         axis1.scatter ( tableContent [0][0], tableContent [0][1], c = colours [iTableFile], label = labels [iTableFile] )
#         axis1.plot ( tableContent [0][0], tableContent [0][1], c = colours [iTableFile] )
#         HandyTools.plotErrorBars ( tableContent [0][0], tableContent [0][1], yErrors = tableContent [0][2], colours = colours [iTableFile], alpha = 0.5, axis = axis1 )
        
#         plt.figure (2)
        plt.scatter ( tableContent [0][0], tableContent [0][3], c = colours [iTableFile], label = labels [iTableFile] )
        plt.plot ( tableContent [0][0], tableContent [0][3], c = colours [iTableFile] )
        HandyTools.plotErrorBars ( tableContent [0][0], tableContent [0][3], yErrors = tableContent [0][4], colours = colours [iTableFile], alpha = 0.5 )
    
    
    
# #     plt.figure (1)
#     axis1.set_ylabel ( xyLabels [1] )
#     axis1.set_title ( titles [iST_TableFile] )
#     axis1.legend ()
# #     plt.savefig (  '{}_Pearson.png'.format ( plotFileNames [iST_TableFile] ) )
    
#     plt.close ()
    
#     plt.figure (2)
    plt.ylabel ( xyLabels [2] )
    plt.title ( titles [iST_TableFile] )
    plt.legend ()

    plt.savefig ( 'roos-serote-{}.png'.format ( plotFileNames [iST_TableFile] ), dpi = 300 )
    
#     plt.close ()







