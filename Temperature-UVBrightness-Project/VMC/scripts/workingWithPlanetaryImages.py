# Quick test script for working with the planetaryimage module.



from planetaryimage import PDS3Image

import matplotlib.pyplot as plt

VMCimage = PDS3Image.open ('V0260_0008_UV2.IMG')
VMCimageGEO = PDS3Image.open ('V0260_0008_UV2.GEO')


plt.figure (1)
plt.clf ()
plt.title ('V0260_0008_UV2.IMG')
plt.imshow (VMCimage.image)
plt.savefig ('../plots/V0260_0008_UV2.png')
plt.close ()

# datetime object
print ( "VMCimageGEO.label ['START_TIME']", VMCimageGEO.label ['START_TIME'] )
print ( 'day = {}, hour = {}'.format (VMCimageGEO.label ['START_TIME'].day, VMCimageGEO.label ['START_TIME'].hour))

plt.figure (2)
plt.clf ()
plt.title ('latitude plane index [3]')
plt.imshow (VMCimageGEO.data [3], vmin=-90, vmax=90)
plt.savefig ('../plots/V0260_0008_UV2_latitude.png')
plt.close ()