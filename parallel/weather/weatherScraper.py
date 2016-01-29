import urllib2
import StringIO
import csv
import json
from os import listdir

def scrapeWeather(dates, locationDict):
    for date in dates:
        for location in locationDict.keys():
            url = 'http://www.bom.gov.au/climate/dwo/%s/text/%s.%s.csv' % (date,locationDict[location],date)
            data = urllib2.urlopen(url).read()

            # Remove comment lines
            data = data.split('\n')
            i = 1
            while len(data[i])>1: i+=1
            data = '\n'.join(data[i+2:])

            f = StringIO.StringIO(data)
            reader = csv.reader(f)

            with open(location+date+'.csv','w') as csvfile: 
                writer = csv.writer(csvfile)
                for row in reader:
                    subset = row[1:]
                    writer.writerow(subset)

def getCSVs():
    filenames = []
    files = listdir('.')
    for f in files:
        if f.endswith('.csv'):
           filenames.append(f)
    return filenames

def getData(filename):
    dataset = []
    with open(filename,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            datapoint = {}
            datapoint['location'] = filename[:-10]
            date = row[0].split('-')
            datapoint['year'] = int(date[0])
            datapoint['month'] = int(date[1])
            datapoint['day'] = int(date[2])
            # TODO better filtering of NULL values
            try:
                datapoint['minTemp'] = float(row[1] or 0)
                datapoint['maxTemp'] = float(row[2] or 0)
                datapoint['rainFall'] = float(row[3] or 0)
                datapoint['evaporation'] = float(row[4] or 0)
                datapoint['sunshine'] = float(row[5] or 0)
                datapoint['windDirection'] = row[6]
                datapoint['windSpeed'] = float(row[7] or 0)
                datapoint['windTime'] = row[8]
                datapoint['9amTemp'] = float(row[9] or 0)
                datapoint['9amHumid'] = float(row[10] or 0)
                datapoint['9amClouds'] = float(row[11] or 0)
                datapoint['9amWindDirection'] = row[12]
                datapoint['9amWindSpeed'] = float(row[13] or 0)
                datapoint['9amPressure'] = float(row[14] or 0)
                datapoint['3pmTemp'] = float(row[15] or 0)
                datapoint['3pmHumid'] = float(row[16] or 0)
                datapoint['3pmClouds'] = float(row[17])
                datapoint['3pmWindDirection'] = row[18]
                datapoint['3pmWindSpeed'] = float(row[19] or 0)
                datapoint['3pmPressure'] = float(row[20] or 0)
            except ValueError, e:
                print e
                continue
            dataset.append(datapoint)
    return dataset
            
locationDict = {
   'Canberra':'IDCJDW2801',
   'Sydney':'IDCJDW2124',
   'Brisbane':'IDCJDW4019',
   'Melbourne':'IDCJDW3050',
   'Adelaid':'IDCJDW5002',
   'Perth':'IDCJDW6111',
   'Hobart':'IDCJDW7021',
   'Darwin':'IDCJDW8014'
}
dates = ['201509','201508','201507','201506','201505','201504','201503','201502','201501','201412','201411','201410']

data = []

scrapeWeather(dates,locationDict)

for csvfile in getCSVs():
    data += getData(csvfile)
with open('weather.js','w') as f:
    jsonStr = json.JSONEncoder().encode(data)
    f.write('var weatherData= ' + jsonStr)
