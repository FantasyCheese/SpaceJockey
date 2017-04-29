import os
import datetime as dt
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from skyfield.api import Topos, load

print("execute getTLE")
referenceTime = (dt.datetime.utcnow() + dt.timedelta(days=-2)).timetuple()
endTime = (dt.datetime.utcnow() + dt.timedelta(days=-1)).timetuple()
currentYear = referenceTime[0]
currentMonth = referenceTime[1]
currentDay = referenceTime[2]
currentHour = referenceTime[3]
currentMinute = referenceTime[4]
currentSecond = referenceTime[5]
endYear = endTime[0]
endMonth = endTime[1]
endDay = endTime[2]
dateRange = op.inclusive_range(dt.date(currentYear, currentMonth, currentDay), dt.date(endYear, endMonth, endDay))
satellite = 'TERRA' # hardcode at moment, need to improve
satelliteID = 25994

st = SpaceTrackClient('tang.alf@gmail.com', 'P62-AER-sNJ-ubK')
lines = st.tle(iter_lines=True, epoch=dateRange, norad_cat_id=satelliteID, orderby='TLE_LINE1 ASC', format='tle')
filePath = os.getcwd() + '/app/tle.txt'
print(filePath)
with open(filePath, 'w') as fp:
    fp.write(satellite+'\n')
    for line in lines:
        print(line)
        fp.write(line+'\n')

# satTLE = load.tle(filePath)
# satellite = satTLE['TERRA']
# ts = load.timescale()
# t = ts.utc(currentYear, currentMonth, currentDay, currentHour, currentMinute, currentSecond)
# geocentric = satellite.at(t).position.km
# print(geocentric)