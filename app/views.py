"""
Definition of views.
"""
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
        """Renders the home page."""
        satellite = request.GET['satellite']
        time = request.GET['time']
        #
        referenceTime = (dt.datetime.utcnow() + dt.timedelta(days=-2)).timetuple()
        endTime = (dt.datetime.utcnow() + dt.timedelta(days=-1)).timetuple()
        currentYear = referenceTime[0]
        currentMonth = referenceTime[1]
        currentDay = referenceTime[2]
        currentHour = referenceTime[3]
        currentMinute = referenceTime[4]
        currentSecond = referenceTime[5]
        #
        filePath = os.getcwd() + '/app'
        command = "python3 {0}/getTLE.py".format(filePath)
        os.system(command)  
        tleFilePath = filePath + '/tle.txt'
        with open(tleFilePath, 'r') as fp:
            content = fp.readlines()
        content = [x.strip('\n') for x in content] 
    
        name = content[0]
        line1 = content[1]
        line2 = content[2]
        tle_rec = ephem.readtle(name, line1, line2)
        tle_rec.compute()
        data = {}
        data['satellite'] = satellite
        data['time'] = time
        data['lon'] = math.degrees(tle_rec.sublong)
        data['lat'] = math.degrees(tle_rec.sublat)
        #
        response = Response(data, status=status.HTTP_200_OK)
        return response


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
