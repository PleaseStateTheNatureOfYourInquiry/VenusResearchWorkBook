# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v20241020

# Load all images and create a figure of each image, showing the spot of the VeRa sounding and the wind advected area of that spot at the time of the
#  recording of the image.


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


# orbitIDLimit = '0000'
orbitIDLimit = '1188'

# With this function a list of VMC images is processed:
#  For each image the wind advected area (latitude-longitude box) of the VeRa sounding location is calculated using  the  getWindAdvectedBox  method of the 
#  VMCTools class, and the average radiance factor (a measure of the reflectance, determined using the  VMCPhotometry  method of the  VMCTools  class) 
#  is determined inside this area.
def processOrbit ( listOfImageFiles, 
                   VeRaSelectedProfilesInformation, 
                   VeRaSPoleProfilesInformation, 
                   targetAltitude = 70,
                   oneSigmaZonalWind = 20, 
                   oneSigmaMeridionalWind = 12):


    # This is the directory path of the orbit.
    orbitDirectory = os.path.dirname ( listOfImageFiles [0] )

    listWithSelectedImages = []
    # Get the image file names that are in the  UsedImages  subfolder of the orbit directory.
    #  These are the images that are manually selected to be part of the analysis.
    if os.path.isdir ( os.path.join (orbitDirectory , 'UsedImages') ):

        listWithSelectedImages = HandyTools.getFilesInDirectoryTree ( os.path.join (orbitDirectory , 'UsedImages'), extension = 'png' )

    # Make sure the  Images  subfolder exists in the orbit directory. 
    #  In this subfolder, the .png files of all images are stored (see end of this function).   
    allImagesDirectory = os.path.join (orbitDirectory , 'Images')
    if not os.path.isdir (allImagesDirectory):
    
        os.mkdir (allImagesDirectory)
    
    
    # Go through the list of images in the orbit.       
    for iImage in range ( len (listOfImageFiles) ):
    
        VMCImageFileName = listOfImageFiles [iImage]
    
        print ()
        print ('VMC image filename:', VMCImageFileName)
        
        # Check if the current image is part of the selected images as per the ones in the  UsedImages  subfolder.
        imageSelected = False
        VMCImageString = VMCImageFileName.split (separatorCharacter) [-1][:-4]
        for selectedImage in listWithSelectedImages:
        
            if VMCImageString in selectedImage:
            
                imageSelected = True

                
        VMCOrbitString = VMCImageFileName.split (separatorCharacter) [-2]  
              
        
        # Read the .IMG and .GEO files with the  readVMCImageAndGeoCube  method of the  VMCTools  class.
        VMCImage, VMCImageFlattened, VMCGeoCube, VMCGeoArraysFlattened = VMCTools.readVMCImageAndGeoCube (VMCImageFileName)


        # Perform the photometry on the image with the  VMCPhotometry  method of the  VMCTools  class.    
        VMCImageCalibrated, VMCImageCalibratedFlattened, \
        incidenceAngleAverage, incidenceAngleSTD, \
        emissionAngleAverage, emissionAngleSTD, \
        phaseAngleAverage, phaseAngleSTD, radianceFactor = VMCTools.VMCPhotometry (VMCImage, VMCImageFlattened, VMCGeoCube, VMCGeoArraysFlattened)
    
        # Extract the time of the acquisition of the image.
        VMCTime = VMCGeoCube.label ['IMAGE_TIME']
    
    
        # Find the VeRa profile information from the orbit ID.
    
        # The result of this search is that the the VeRa profile specs for corresponding orbit are stored in the  VeRaProfileSpecs  variable:
        #      VeRaProfileSpecs [0] = 'OrbitID'
        #      VeRaProfileSpecs [1] = 'ProfileID'
        #      VeRaProfileSpecs [2] = 'LatitudeOneBar'
        #      VeRaProfileSpecs [3] = 'LongitudeOneBar'
        #      VeRaProfileSpecs [4] = 'DayOfYear'
        #      VeRaProfileSpecs [5] = 'TimeOfDay'
        #      VeRaProfileSpecs [6] = 'LocalSolarTime'
        #      VeRaProfileSpecs [7] = 'FilteredProfiles'
        #      VeRaProfileSpecs [8] = 'NumberOfFilteredLevels'
        #      VeRaProfileSpecs [9] = 'OriginalProfiles'
        #      VeRaProfileSpecs [10] = 'NumberOfOriginalLevels'
    
        orbitFound = False
        iVeRaProfile = 0
        while not orbitFound and iVeRaProfile < len ( VeRaSelectedProfilesInformation ['OrbitID'] ):
        
            if VeRaSelectedProfilesInformation ['OrbitID'][iVeRaProfile].split ('_')[0] in VMCOrbitString:
            
                orbitFound = True
                VeRaProfileSpecs = [ VeRaSelectedProfilesInformation [key][iVeRaProfile]  for key in VeRaSelectedProfilesInformation.keys () ]            
                print ( ' VeRa profile specs (1bar):', VeRaProfileSpecs [0] )
                                    
                
            iVeRaProfile += 1
        
    
        orbitFound = False
        iVeRaProfile = 0
        while not orbitFound and iVeRaProfile < len ( VeRaSPoleProfilesInformation ['OrbitID'] ):
        
            if VeRaSPoleProfilesInformation ['OrbitID'][iVeRaProfile].split ('_')[0] in VMCOrbitString:
            
                orbitFound = True
                VeRaProfileSpecs = [ VeRaSPoleProfilesInformation [key][iVeRaProfile]  for key in VeRaSPoleProfilesInformation.keys () ]
                print (' VeRa profile specs (1bar):', VeRaProfileSpecs [0] ) 
                                    
                
            iVeRaProfile += 1
        
        
        VeRaOrbitID = VeRaProfileSpecs [0]
        VeRaDayOfYear = VeRaProfileSpecs [4]
        VeRaTimeOfDayHours = VeRaProfileSpecs [5]
    
    
    
        # Extract the latitude, longitude, temperature and pressure at the target altitude from the filtered VeRa profile.
        # Note that the  radiusOfVenus  is from the  analysisConfiguration  file.
        iCloudTopLevel = 0
        for iLevel in range (VeRaProfileSpecs [8]):
        
            if VeRaProfileSpecs [7][0][iLevel] - radiusOfVenus == targetAltitude:
            
                iCloudTopLevel = iLevel
                latitudeAtTargetAltitude = VeRaProfileSpecs [7][5][iCloudTopLevel]
                longitudeAtTargetAltitude = VeRaProfileSpecs [7][6][iCloudTopLevel]
                temperatureAtTargetAltitude = VeRaProfileSpecs [7][1][iCloudTopLevel]
                oneSigmaTemperateAtTargetAltitude = VeRaProfileSpecs [7][2][iCloudTopLevel]
                pressureAtTargetAltitude = VeRaProfileSpecs [7][3][iCloudTopLevel]
    
    
        print (' lat, lon, T, dT, p @ {:5.2f}km altitude: {:6.2f}˚, {:6.2f}˚, {:6.2f}K, {:6.2f}K, {:8.5f}bar'.format ( targetAltitude, 
                                                                                                                       latitudeAtTargetAltitude,
                                                                                                                       longitudeAtTargetAltitude,
                                                                                                                       temperatureAtTargetAltitude,
                                                                                                                       oneSigmaTemperateAtTargetAltitude,
                                                                                                                       pressureAtTargetAltitude ) )
        
        
        # Check if the VMC image is acquired at same day as the VeRa profile.
        if VeRaDayOfYear == '{:4d}-{:02d}-{:02d}'.format (VMCTime.year, VMCTime.month, VMCTime.day):
        
            timeDifferenceVMC_VeRa = (VMCTime.hour + VMCTime.minute / 60) - VeRaTimeOfDayHours
        
        
        # VMC image is taken on the previous day as compared to the VeRa profile.
        elif VeRaDayOfYear > '{:4d}-{:02d}-{:02d}'.format (VMCTime.year, VMCTime.month, VMCTime.day):
        
            timeDifferenceVMC_VeRa = ( (VMCTime.hour + VMCTime.minute / 60) - 24 ) - VeRaTimeOfDayHours
        
            
        # VMC image is taken on the next day as compared to the VeRa profile.
        else:
        
            timeDifferenceVMC_VeRa = (VMCTime.hour + VMCTime.minute / 60) + (24 - VeRaTimeOfDayHours)
            
        
            
        print (' Time difference VMC - VeRa (h)', timeDifferenceVMC_VeRa)

        # Calculate the wind advected area in the image that corresponds to the VeRa sounding location using the  getWindAdvectedBox  of the  VMCTools  class.
        latitudeCentre, latitudeLimits, longitudeCentre, longitudeLimits = \
         VMCTools.getWindAdvectedBox ( latitudeAtTargetAltitude, 
                                       longitudeAtTargetAltitude, 
                                       timeDifferenceVMC_VeRa, 
                                       oneSigmaZonalWind = oneSigmaZonalWind, 
                                       oneSigmaMeridionalWind = oneSigmaMeridionalWind )
    
        
        # Determine the indices in the flattened image array of the latitude-longitude box. 

        #  First find all the indices within the longitude limits.
        #  Note that for the longitude, the crossing of the 0˚ (or 360˚) line needs to be taken into account. Therefore the longitudeLimits is a list of two 
        #  lists. If the two sublists are the same, then there is no crossing. If they are different ( longitudeLimits [0] != longitudeLimits [1] ) then there is
        #  a crossing.
        iLongitudeBox = np.where ( np.logical_and ( VMCGeoArraysFlattened [4] >= longitudeLimits [0][0], VMCGeoArraysFlattened [4] <= longitudeLimits [0][1] ) ) [0]
        if longitudeLimits [0] != longitudeLimits [1]:
        
            iLongitudeBox2 = np.where ( np.logical_and ( VMCGeoArraysFlattened [4] >= longitudeLimits [1][0], VMCGeoArraysFlattened [4] <= longitudeLimits [1][1] ) ) [0]
            iLongitudeBox = np.asarray ( list ( set ( iLongitudeBox.tolist () + iLongitudeBox2.tolist () ) ) )
 
        #  Next find all the indices within the latitude limits.   
        iLatitudeBox = np.where ( np.logical_and ( VMCGeoArraysFlattened [3] >= latitudeLimits [0], VMCGeoArraysFlattened [3] <= latitudeLimits [1] ) ) [0]
    
    
        #  Finally, find the indices both with in the longitude and latitude sets and store in the  iInLatitudeLongitudeBox  list. 
        #  Also store the indices of points with valid radiance factors, i.e. VMCImageCalibratedFlattened > 0, in the  iValidValues  list.
        iInLatitudeLongitudeBox = []
        iValidValues = []
        for iLongitudeInBox in iLongitudeBox:
    
            if iLongitudeInBox in iLatitudeBox:
            
                iInLatitudeLongitudeBox.append (iLongitudeInBox)
                
                if VMCImageCalibratedFlattened [iLongitudeInBox] > 0:
                
                    iValidValues.append (iLongitudeInBox)
                
        
        # Calculate the average radiance factor of the valid points in the latitude-longitude box.
        averageRadianceFactor = (0,0,0)
        if len (iValidValues) > 1:
        
            print ( ' number of positive values in the latitude-longitude-box = {} ({})'.format ( len (iValidValues), len (iInLatitudeLongitudeBox) ) )
            averageRadianceFactor = DataTools.getAverageVarAndSDPYtoCPP ( VMCImageCalibratedFlattened [iValidValues] )
            print ( ' average radiance factor in box = {:6.4f} +/- {:7.5f}'.format ( averageRadianceFactor [0], averageRadianceFactor [1] ) )
            print ( ' average phase, emission and incidence angles: {}, {}, {}'.format (phaseAngleAverage, emissionAngleAverage, incidenceAngleAverage) )
    
    
        # Add the information of selected images to the selected images table, as well as to the  iValidPointsSelectedImages   Python dictionary.
        if imageSelected:
        
            print ( ' {}   {}   {}    {:5.2f}       {:5.2f}      {:6.2f}    {:6.2f}    {:7.2f}         {:6.2f}      {:6.2f}  {:6.2f}      {:7.2f}      {:6.2f}   {:7.2f}     {:7.2f}         {:6d}             {:6.3f}           {:6.3f}        {:6.2f}   {:6.3f}       {:5.2f}             {:6.2f}           {:6.2f} '.
                  format ( VeRaProfileSpecs [0].split ('_')[0],
                           VMCImageFileName.split (separatorCharacter)[-1][:-4],
                           VeRaProfileSpecs [4],
                           VeRaTimeOfDayHours,
                           (VMCTime.hour + VMCTime.minute / 60),
                           timeDifferenceVMC_VeRa,
                           latitudeAtTargetAltitude,
                           longitudeAtTargetAltitude,
                           latitudeCentre,
                           latitudeLimits [0], latitudeLimits [1],
                           longitudeCentre,
                           longitudeLimits [0][0], longitudeLimits [1][1],
                           phaseAngleAverage,
                           len (iValidValues),
                           averageRadianceFactor [0], 
                           averageRadianceFactor [1],               
                           temperatureAtTargetAltitude,
                           oneSigmaTemperateAtTargetAltitude,   
                           VeRaProfileSpecs [6],
                           emissionAngleAverage,
                           incidenceAngleAverage ), file = fileOpen )

        
            iValidPointsSelectedImages ['Image File Name'].append (VMCImageFileName)
            iValidPointsSelectedImages ['Indices Valid Points'].append (iValidValues)


        # Create a plot and save it.  
        
        # The opacity mask is the latitude-longitude box.  
        opacityMaskFlattened = np.zeros ( 512 * 512 ) - 1.
        opacityMaskFlattened [iInLatitudeLongitudeBox] = 0
        opacityMask = opacityMaskFlattened.reshape (512,512)

        # Determine the index of the point in the VMC image closest to the VeRa coordinates.
        deltaLongitude = np.abs ( VMCGeoArraysFlattened [4] - longitudeAtTargetAltitude )
        iClosestLongitudes = np.where ( deltaLongitude < 1 )[0]

        deltaLatitude = np.abs ( VMCGeoArraysFlattened [3] - latitudeAtTargetAltitude )                
        iClosestLatitudes = np.where ( deltaLatitude < 1 )[0]

        VeRaPositionInVMCImage = False
        VeRaClosestLatitudeAndLongitude = np.zeros ( 512 * 512 ) - 1.        
        for iClosestLongitude in iClosestLongitudes:
        
            if iClosestLongitude in iClosestLatitudes:
            
                VeRaPositionInVMCImage = True
                VeRaClosestLatitudeAndLongitude [iClosestLongitude] = 0
                
    
        VMCFigure, VMCFigureAxis = plt.subplots ( figsize = (10, 8), ncols = 1 )
    
        if not phaseAngleAverage:
        
            phaseAngleAverage = -1
            
            
        imageTitle = '{} | $\Delta$T = {:5.2f}h | {} = {:5.2f} +/- {:6.3f} | $\\alpha$ = {:02d}˚'.\
                      format ( VMCImageString, timeDifferenceVMC_VeRa, 'R$_{factor}$', averageRadianceFactor [0], averageRadianceFactor [1], int (phaseAngleAverage) )
        plt.title (imageTitle, fontsize = 12)
        plt.xlabel ( '(VMC)  {:4d}-{:02d}-{:02d} at {:02d}h:{:02d}m   |   (VeRa)  {:02d}h:{:02d}m  X @ (lat, lon) = ({:03d}˚, {:03d}˚E)'.
                     format ( VMCTime.year, VMCTime.month, VMCTime.day, VMCTime.hour, VMCTime.minute, 
                              int (VeRaTimeOfDayHours), int ( 60 * ( VeRaTimeOfDayHours - int (VeRaTimeOfDayHours) ) ),
                              int (latitudeAtTargetAltitude), int (longitudeAtTargetAltitude) ) )
    
        VMCFigureAxisPlot = VMCFigureAxis.imshow (VMCImageCalibrated, cmap = 'nipy_spectral', vmin = 0, vmax = 3.)
        plt.colorbar (VMCFigureAxisPlot, label = 'R$_{factor}$')
    
        VMCFigureAxis.imshow ( opacityMask, cmap = 'binary', vmin = 0, vmax = 1., alpha = 0.6 * (opacityMask == 0) )

        if VeRaPositionInVMCImage:

            opacityMaskVeRa = VeRaClosestLatitudeAndLongitude.reshape (512,512)
            VeRaXCoordinate = int ( np.median ( np.where (opacityMaskVeRa == 0)[1] ) )
            VeRaYCoordinate = int ( np.median ( np.where (opacityMaskVeRa == 0)[0] ) )
            plt.plot (VeRaXCoordinate, VeRaYCoordinate, marker = 'x', color = 'white')
    
        plt.savefig ( os.path.join ( allImagesDirectory, VMCImageString + '.png' ) )
        
        if imageSelected:
        
            plt.savefig ( os.path.join ( orbitDirectory, 'UsedImages', VMCImageString + '.png' ) )

        
        plt.close ()
        

        


# Read the NumPy arrays containing all the necessary VeRa profiles information.
VeRaSelectedProfilesInformation = np.load ('../../../VeRa/Step02/VeRaSelectedProfiles.profiles', allow_pickle = True).tolist ()
VeRaSPoleProfilesInformation = np.load ('../../../VeRa/Step02/VeRaSouthPolarDynamicsCampaignProfiles.profiles', allow_pickle = True).tolist ()


# Set the parameters for this run.
targetAltitude = 70 #km - the altitude at which the latitude, longitude and temperature of the VeRa sounding will be extracted from the filtered VeRa profiles.
oneSigmaZonalWind = 20 #m/s - the uncertainty in the zonal wind.
oneSigmaMeridionalWind = 12 #m/s - the uncertainty in the meridional wind.


# Open and create the header of the table file that will contain information about the selected images.

if orbitIDLimit == '0000':

    VMCSelectedImagesFileName = 'VMCSelectedImages.dat'

else:

    VMCSelectedImagesFileName = 'VMCSelectedImages_orbits_later_than_{}.dat'.format (orbitIDLimit)


fileOpen = open ( os.path.join ('..', VMCSelectedImagesFileName), 'w' )

print (' ', file = fileOpen)
print (' File: {}'.format (VMCSelectedImagesFileName), file = fileOpen)
print (' Created at {}'.format ( HandyTools.getDateAndTimeString () ), file = fileOpen)

print (' ', file = fileOpen)
print ('  Target altitude (cloud tops) = {}km (Lat_VeRa, Lon_VeRa, T, dT)'.format (targetAltitude), file = fileOpen)
print ('  Standard deviation zonal wind = {}m/s'.format (oneSigmaZonalWind), file = fileOpen)
print ('  Standard deviation meridional wind = {}m/s'.format (oneSigmaMeridionalWind), file = fileOpen)

print (' ', file = fileOpen)
print ('  # point in box are all the points in the latitude-longitude box on the Venus disk', file = fileOpen)
print ('  Radiance factor is the average of the points in the latitude-longitude box with values > 0 and incidence angles < 89˚', file = fileOpen)
print ('  dRadiance factor is the standard deviation of the radiance factor', file = fileOpen)

print (' ', file = fileOpen)
print (' Orbit       Image          DOY      VeRa Time    VMC Time   Time diff  Lat_VeRa   Lon_VeRa   lat_centre_VMC   Lat_range_VMC   Lon_centre_VMC   Lon_range_VMC      Phase Angle   #Points in box   Radiance factor  dRadiance factor     T       dT     Local Solar Time   Emission Angle   Incidence Angle', file = fileOpen)
print ('                         yyyy-mm-dd     (h)         (h)         (h)       (˚)        (˚)            (˚)             (˚)              (˚)             (˚)               (˚)                                                             (K)      (K)          (h)                (˚)              (˚)', file = fileOpen)
print ('C_END', file = fileOpen)



# Create the Python dictionary that will contain the image file names + paths and the lists of indices of the valid points in the latitude-longitude boxes of the 
#  wind advected VeRa sounding locations for that image. Note that the indices refer to the flattened image arrays!!
iValidPointsSelectedImages = { 'Image File Name' : [],
                               'Indices Valid Points' : [] }



# # ----- For testing of this script
# # Note that  VMCDataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
# listOfImageFiles = HandyTools.getFilesInDirectoryTree ( os.path.join ( VMCDataDirectory, 'Orb0260' ), extension = 'GEO' )
# processOrbit ( listOfImageFiles, 
#                VeRaSelectedProfilesInformation, 
#                VeRaSPoleProfilesInformation, 
#                targetAltitude = targetAltitude,
#                oneSigmaZonalWind = oneSigmaZonalWind, 
#                oneSigmaMeridionalWind = oneSigmaMeridionalWind )
# # ------


# Go through each VeRa profile and process the images of the corresponding orbit.
for orbitID in VeRaSelectedProfilesInformation ['OrbitID']:

    if orbitID >= orbitIDLimit:

        # Get the list of existing images in the orbit directory.
        # Note that  VMCDataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
        listOfImageFiles = HandyTools.getFilesInDirectoryTree ( os.path.join ( VMCDataDirectory, 'Orb' + str (orbitID).split ('_')[0] ), extension = 'GEO' )
        
        if listOfImageFiles:
    
            # Process the images with the  processOrbit  function.
            processOrbit ( listOfImageFiles, 
                           VeRaSelectedProfilesInformation, 
                           VeRaSPoleProfilesInformation, 
                           targetAltitude = targetAltitude,
                           oneSigmaZonalWind = oneSigmaZonalWind, 
                           oneSigmaMeridionalWind = oneSigmaMeridionalWind )



for orbitID in VeRaSPoleProfilesInformation ['OrbitID']:

    if orbitID >= orbitIDLimit:
    
        # Get the list of existing images in the orbit directory.
        # Note that  VMCDataDirectory  is from the  analysisConfiguration  file (import at the top of this script).
        listOfImageFiles = HandyTools.getFilesInDirectoryTree ( os.path.join ( VMCDataDirectory, 'Orb' + str (orbitID).split ('_')[0] ), extension = 'GEO' )
    
        if listOfImageFiles:
        
            # Process the images with the  processOrbit  function.
            processOrbit ( listOfImageFiles, 
                           VeRaSelectedProfilesInformation, 
                           VeRaSPoleProfilesInformation, 
                           targetAltitude = targetAltitude,
                           oneSigmaZonalWind = oneSigmaZonalWind, 
                           oneSigmaMeridionalWind = oneSigmaMeridionalWind )

 
 
# Save the Python dictionary with the lists of indices (of the flattened image arrays!) of valid points to a NumPy file.
HandyTools.saveContentToNumpyWithCustomExtension ( iValidPointsSelectedImages, 
                                                   os.path.join ('..' , 'VMCSelectedImages'),
                                                   extensionWithoutDot = 'iValidPoints', 
                                                   overWrite = True )
   
    
# Once all images have been process, close the table file. 
fileOpen.close ()


# Determine the number of orbits and images and add this information to the header of the table file.
tableTextContent = HandyTools.getTextFileContent ( os.path.join ('..', VMCSelectedImagesFileName) )
tableContent = HandyTools.readTable ( os.path.join ('..', VMCSelectedImagesFileName) )

numberOfImages = len ( tableContent [0][0] )
numberOfOrbits = len ( list ( set ( tableContent [0][0] ) ) )

fileOpen = open ( os.path.join ('..', VMCSelectedImagesFileName), 'w')

for textLine in tableTextContent:
        
    print (textLine, file = fileOpen)

    if 'dRadiance factor is the standard deviation of the radiance factor' in textLine:

        print ( '', file = fileOpen )    
        print ( ' {} orbits with a total of {} images'.format (numberOfOrbits, numberOfImages), file = fileOpen )
        print ( '', file = fileOpen )

    
fileOpen.close ()






