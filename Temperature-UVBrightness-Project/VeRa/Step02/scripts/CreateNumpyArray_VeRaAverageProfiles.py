# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20240616

# Read all the raw VeRa-profiles, filter each profile with the specific settings (= default setting at 1km vertical resolution) and keep the raw and filtered profiles
#  and some meta-data for each profile in a Python dictionary structure. At the end, save a NumPy binary file of the content of the dictionary for easy loading and acces later.

# Standard imports.
import sys
separatorCharacter = '\\' if sys.platform == 'win32' else '/'

import os
import numpy as np


# Custom imports.
from HandyTools import HandyTools
from VeRaTools import VeRaTools

# Import the analysis configuration settings.
sys.path.append ( os.path.abspath ('../../../') ) 
from analysisConfiguration import *


# Create the VeRa profiles dictionary.
def createVeRaProfilesDictionary (listOfVeRaProfileTABList, VeRaProfilesInformation, dictionaryFileName = ''):

    VeRaProfiles = {
     'OrbitID' : [],
     'ProfileID' : [],
     'LatitudeOneBar' : [],
     'LongitudeOneBar' : [],
     'DayOfYear' : [],
     'TimeOfDay' : [],
     'LocalSolarTime' : [],
     'FilteredProfiles' : [],
     'NumberOfFilteredLevels' : [],
     'OriginalProfiles' : [],
     'NumberOfOriginalLevels' : []
    }
    
    
    # Go through all the VeRa profiles in the list.
    for VeRaProfileTABFileName in listOfVeRaProfileTABList:

        
        # Determine the orbit ID from the file name, which is the name of the deepest subfolder minus the 'Orb' string.
        orbitID = VeRaProfileTABFileName.split (separatorCharacter) [-2].split ('Orb')[-1]
        # Determine which line in the information file corresponds to the orbit ID.
        iVeRaProfilesInformation = 0
        while VeRaProfilesInformation [0][iVeRaProfilesInformation] not in orbitID and iVeRaProfilesInformation < len (VeRaProfilesInformation [0]):
        
            iVeRaProfilesInformation += 1
 
        if iVeRaProfilesInformation < len (VeRaProfilesInformation [0]):

            # Store the profile ID.
            VeRaProfiles ['ProfileID'].append ( VeRaProfileTABFileName.split (separatorCharacter) [-1] )

            print ( ' Reading information for {} with orbit ID {}'.format (VeRaProfiles ['ProfileID'][-1], orbitID) )

            # Store the orbit ID.
            VeRaProfiles ['OrbitID'].append (orbitID)
            
        
            # Store the relevant values and profiles in the  VeRaProfiles  dictionary.
            VeRaProfiles ['LatitudeOneBar'].append ( VeRaProfilesInformation [6][iVeRaProfilesInformation] )
            VeRaProfiles ['LongitudeOneBar'].append ( VeRaProfilesInformation [7][iVeRaProfilesInformation] )
    
            VeRaProfiles ['DayOfYear'].append ( VeRaProfilesInformation [1][iVeRaProfilesInformation] )
            VeRaProfiles ['TimeOfDay'].append ( VeRaProfilesInformation [2][iVeRaProfilesInformation] )
            VeRaProfiles ['LocalSolarTime'].append ( VeRaProfilesInformation [3][iVeRaProfilesInformation] )
       
    
            # Read, filter and store the VeRa profile.
            VeRaFilteredProfile = VeRaTools.getFilteredVeRaProfile (VeRaProfileTABFileName)
    
            VeRaProfiles ['FilteredProfiles'].append ( VeRaFilteredProfile [0] )
            VeRaProfiles ['NumberOfFilteredLevels'].append ( VeRaFilteredProfile [1] )
            VeRaProfiles ['OriginalProfiles'].append ( VeRaFilteredProfile [2] )
            VeRaProfiles ['NumberOfOriginalLevels'].append ( VeRaFilteredProfile [3] )


    # Save the  VeRaProfiles  dictionary as a NumPy file with the extension '.profiles'.
    HandyTools.saveContentToNumpyWithCustomExtension ( VeRaProfiles, 
                                                       os.path.join (VeRaWorkBookDirectory, 'Step02', dictionaryFileName), 
                                                       extensionWithoutDot = 'profiles', 
                                                       overWrite = True )



# Create and save the dictionary for the "selected profiles" (i.e. not the South Polar Dynamics Campaign).
VeRaSelectedProfilesInformation = \
 VeRaTools.readValuesFromVeRaTable ( os.path.join (VeRaWorkBookDirectory, 'Step01', 'VeRa_LocalSolarTime_OneBarLevel_PerOrbit_SelectedProfiles.dat') )

# Note that  VeRaDataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
topDirectory = os.path.join (VeRaDataDirectory, 'VeRa_selected_profiles')
listOfVeRaProfileTABList = HandyTools.getFilesInDirectoryTree (topDirectory, extension = 'TAB')
listOfVeRaProfileTABList = sorted (listOfVeRaProfileTABList, key = lambda x : x.split ('/') [-2])

createVeRaProfilesDictionary (listOfVeRaProfileTABList, VeRaSelectedProfilesInformation, 'VeRaSelectedProfiles')


# Create and save the dictionary for the South Polar Dynamics Campaign.
VeRaSPoleProfilesInformation = \
 VeRaTools.readValuesFromVeRaTable ( os.path.join (VeRaWorkBookDirectory, 'Step01', 'VeRa_LocalSolarTime_OneBarLevel_PerOrbit_SPoleProfiles.dat') )

# Note that  VeRaDataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
topDirectory = os.path.join (VeRaDataDirectory, 'VeRa_Spole_2013') 
listOfVeRaProfileTABList = HandyTools.getFilesInDirectoryTree (topDirectory, extension = 'TAB')
listOfVeRaProfileTABList = sorted (listOfVeRaProfileTABList, key = lambda x : x.split ('/') [-2])


createVeRaProfilesDictionary (listOfVeRaProfileTABList, VeRaSPoleProfilesInformation, 'VeRaSouthPolarDynamicsCampaignProfiles')
