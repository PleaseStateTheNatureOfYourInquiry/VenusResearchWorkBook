from HandyTools import HandyTools as ht
import numpy as np

temperatureProfilesSpecs = ht.readTable ('/Users/maarten/Science/Venus/VEX/Analysis2024/VeRa_LocalSolarTime_OneBarLevel_PerOrbit.dat')

solarHours = list ( set ( [ int (solarLongitude) for solarLongitude in temperatureProfilesSpecs[1] ] ) )

for solarHour in solarHours:

    iProfilesInHour = np.where ( np.logical_and (temperatureProfilesSpecs[1] > solarHour, temperatureProfilesSpecs[1] < solarHour + 1) )[0]
    print (solarHour)
    print (*iProfilesInHour)
    
    