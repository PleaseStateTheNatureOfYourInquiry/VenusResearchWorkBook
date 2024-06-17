# Author: Maarten Roos-Serote
# ORCID author: 0000 0001 5001 1347

# Version: v202400609

# Standard imports.
import numpy as np
import matplotlib.pyplot as plt

# Custom imports.
from VMCTools import VMCTools
from planetaryimage import PDS3Image


# This is a short script to verify the correct transformation of the longitude values, as performed in the  readVMCImageAndGeoCube  function of VMCTools 
#  from the original -180˚ - +180˚ stored in the .GEO cubes, to (the more convenient) 0˚ - 360˚. 

imageGeoCubeFileName = '/Users/maarten/Science/Venus/Temperature-UV_Analysis_2024/Data/VEX/VMC/Orb2805/V2805_0032_UV2.GEO'


VMCGeoCube = PDS3Image.open (imageGeoCubeFileName)
VMCImage = VMCTools.readVMCImageAndGeoCube (imageGeoCubeFileName)

# This line approximates the +180˚ / -180˚ passage line in the first figure.
x1 = 317 + np.arange (344 - 317)
y1 = (123 - 267) / (317 - 344) * (x1 - 344) + 267


# This line approximates the 0˚ / +360˚ passage line in the second figure.
x2 = 344 + np.arange (400 - 344)
y2 = (425 - 267) / (400 - 344) * (x2 - 344) + 267


plt.clf ()
plt.figure (1, figsize = (10,5) )

# In this plot is displayed the original longitude values, running from -180˚ to +180˚. 
plt.subplot (121)
plt.imshow (VMCGeoCube.data [4], vmin = -180, vmax = 180)
plt.colorbar (location = 'right')
plt.title ('V2805_0032_UV2 \n GEO cube original longitude', fontsize = 8)
plt.text (400,470, '+0˚', c = 'white')
plt.text (250,90, '+180˚', c = 'white')
plt.text (320,90, '-180˚', c = 'white')
plt.plot (x1, y1, c = 'white')
plt.plot (x2, y2, c = 'white')


# In this plot are displayed the longitude values as transformed by  VMCTools.readVMCImageAndGeoCube, that go from 0˚ to +360˚.
plt.subplot (122)
plt.imshow (VMCImage [3][-1].reshape (512, 512), vmin = 0, vmax = 360)
plt.colorbar (location = 'right')
plt.title ('V2805_0032_UV2 \n VMCTools.readVMCImageAndGeoCube transformed longitude', fontsize = 8)
plt.text (360,470, '+0˚', c = 'white')
plt.text (300,90, '+180˚', c = 'white')
plt.text (410,470, '+360˚', c = 'white')
plt.plot (x1, y1, c = 'white')
plt.plot (x2, y2, c = 'white')

plt.savefig ('longitudeTransformationCheck.png')