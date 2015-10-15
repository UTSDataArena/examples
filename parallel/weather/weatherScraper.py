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
                    subset = row[1:5]
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
            try:
                datapoint['maxTemp'] = float(row[1] or 0)
                datapoint['minTemp'] = float(row[2] or 0)
                datapoint['rainFall'] = float(row[3] or 0)
            except ValueError:
                print 'Value Error occured: ' + str(row)
                continue
            dataset.append(datapoint)
    return dataset
            
locationDict = {
   'Canberra':'IDCJDW2801',
   'Tuggeranong':'IDCJDW2801',
   'Mount Ginini':'IDCJDW2804',
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
