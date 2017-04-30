import requests
import pandas as pd

url = 'https://www.celestrak.com/NORAD/elements/science.txt'
response = requests.get(url)
page = response.text

names = []
satelliteID = []
lines = page.split('\r\n')
for i in range(len(lines)-1):
    if i%3 == 0:
        names.append(lines[i].replace(" ", ""))
    if i%3 == 1:
        satelliteID.append(lines[i][2:7])

satelliteMappingTable = pd.DataFrame(
    {'name': names,
     'id': satelliteID
    })

satelliteMappingTable.to_csv('satelliteMappingTable.csv')