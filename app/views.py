import ephem
import math
import datetime as dt
from datetime import datetime
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MyRESTView(APIView):
    #
    def get(self, request, *args, **kw):
        #
        satellite = request.GET['satellite']
        reqTime = request.GET['time']
        reqTime = dt.datetime.strptime(reqTime, '%Y-%m-%d')
        referenceTime = reqTime.strftime("%Y-%m-%dT%H:%M:%S")
        timeInterval = []
        for i in range(10):
            timeInterval.append((reqTime + dt.timedelta(seconds=30*i)).strftime("%Y/%m/%d %H:%M:%S"))
        #
        filePath = os.getcwd() + '/app'
        command = "python3 {0}/getTLE.py {1} {2}".format(filePath, referenceTime, satellite)
        os.system(command)  
        tleFilePath = filePath + '/tle.txt'
        with open(tleFilePath, 'r') as fp:
            content = fp.readlines()
        content = [x.strip('\n') for x in content] 
        #
        name = content[0]
        line1 = content[1]
        line2 = content[2]
        tle_rec = ephem.readtle(name, line1, line2)
        data = {}
        for i in range(len(timeInterval)):
            timetag = 't'+str(i+1)
            data['t'+str(i+1)] = {}
            tle_rec.compute(timeInterval[i])
            data[timetag]['satellite'] = satellite
            data[timetag]['time'] = timeInterval[i]
            data[timetag]['bottomLeftLon'] = math.degrees(tle_rec.sublong) - 0.6
            data[timetag]['bottomLeftLat'] = math.degrees(tle_rec.sublat) - 0.6
            data[timetag]['topRightLon'] = math.degrees(tle_rec.sublong) + 0.6
            data[timetag]['topLeftLat'] = math.degrees(tle_rec.sublat) + 0.6
        #
        response = Response(data, status=status.HTTP_200_OK)
        return response
