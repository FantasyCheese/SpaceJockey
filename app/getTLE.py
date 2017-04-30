import os
import sys
import datetime as dt
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from skyfield.api import Topos, load

print("execute getTLE")
timestamp = sys.argv[1][:-5]
referenceTime = dt.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
print(referenceTime)
startTime = referenceTime.timetuple()
# referenceTime = (dt.datetime.utcnow() + dt.timedelta(days=-2)).timetuple()
endTime = (referenceTime + dt.timedelta(days=1)).timetuple()
currentYear = startTime[0]
currentMonth = startTime[1]
currentDay = startTime[2]
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