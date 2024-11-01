# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240616


# Create the tables with the orbit IDs and information at the one-bar pressure level of the corresponding VeRa temperature profiles.
# The information is the Day Of Year, time of observation, Local Solar Time, Latitude, Longitude, and Solar Zenith Angle at the one-bar
#  pressure levels.


# Standard imports.
import os
import sys


# Custom imports.
from VeRaTools import VeRaTools
from HandyTools import HandyTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Note that  VeRaDataDirectory  is from the  analysisConfiguration  file.
VeRaTools.createVeRaProfilesTable ( '../VeRa_LocalSolarTime_OneBarLevel_PerOrbit_SelectedProfiles.dat', 
                                    os.path.join (VeRaDataDirectory, 'VeRa_selected_profiles') )        
VeRaTools.createVeRaProfilesTable ('../VeRa_LocalSolarTime_OneBarLevel_PerOrbit_SPoleProfiles.dat', 
                                    os.path.join (VeRaDataDirectory, 'VeRa_Spole_2013') )      




