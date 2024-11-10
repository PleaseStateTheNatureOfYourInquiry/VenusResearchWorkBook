# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v202400610

# The CSV file comes from the Zenodo repository at doi.org/10.5281/zenodo.5159027, as part of the article by Akiba, M. et al. (2021). 
#   "Thermal tides in the upper cloud layer of Venus as deduced from the emission angle dependence of the brightness temperature by Akatsuki/ LIR."
#   Journal of Geophysical Research: Planets, 126, e2020JE006808. doi.org/10.1029/2020JE006808Abika

# Standard imports.
import os

import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'


# Custom imports.
from HandyTools import HandyTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Note that  AkatsukiDataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
csvFileName = os.path.join (AkatsukiDataDirectory, 'Akiba_etal_2021v4/Figure_data_csv/Figure5/temp_devi_contour_lt_to_lat_distributions_at_constant_altitude_each_value_whole_wider_period.csv') 

content = HandyTools.getTextFileContent (csvFileName)

tableFileName = os.path.abspath ( os.path.join (VMCWorkBookDirectory, 'Step04', 'temp_devi_contour_lt_to_lat_distributions_at_constant_altitude_each_value_whole_wider_period.dat') ) 
fileOpen = open (tableFileName, 'w')

headerLines = [
'',
' Original file {}'.format (csvFileName),
'  from Zenodo repository at doi.org/10.5281/zenodo.5159027 (figure5)',
'  Figure 5a from Akiba, M. et al. (2021). "Thermal tides in the upper cloud layer of Venus as deduced from the emission angle dependence of the brightness temperature by Akatsuki/ LIR."',
'   Journal of Geophysical Research: Planets, 126, e2020JE006808. https:// doi.org/10.1029/2020JE006808',
'',
' LST = Local Solar Time ',
' Values are the temperature amplitudes of the combined (diurnal and semi-diurnal) thermal tides.',
'',
' Latitude  LST:  00h       01h       02h       03h       04h       05h       06h       07h       08h       09h       10h       11h       12h       13h       14h       15h       16h       17h       18h       19h       20h       21h       22h       23h',
'   (˚)           (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)       (K)',
]

headerString = HandyTools.getTableHeader (tableFileName, creationScript = 'CreateTable_ThermalTide_Akiba2021_Figure5.py', headerLines = headerLines)
print (headerString, file = fileOpen)


for iLine in range ( 1, len (content) ):

    elements = content [iLine].split (',')
    
    lineString = ' {:5.1f}      '.format ( float ( elements [0] ) )
    for iElement in range (1, len (elements) ):
    
        lineString += '  {:8.5f}'.format ( float ( elements [iElement] ) )

    print (lineString, file = fileOpen)
    

fileOpen.close ()    
    






