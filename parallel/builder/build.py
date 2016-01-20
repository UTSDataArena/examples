#!/usr/bin/python2

import csv
import json
from distutils import dir_util 
from subprocess import call
import random
from sys import argv
            
csvName = 'Public.csv'
groupColumn = 'Institution'
if len(argv)>2:
    csvName = argv[1]
    groupColumn = argv[2]

path = csvName[:-4]
# has to end with /
baseDir = path + "/"
dir_util.mkpath(baseDir) 
dir_util.copy_tree('./template', baseDir)
 
groups = []
firstRow = {} 
with open(csvName) as csvfile:
    reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    with open(baseDir + 'files/data.js','w') as jsonfile:
        jsonfile.write('var dataJSON = [')
        for row in reader:
            if len(firstRow) == 0: firstRow = row
            # collect all values of group column
            if row[groupColumn] not in groups:
                groups.append(row[groupColumn])

            json.dump(row, jsonfile)
            jsonfile.write(',\n')
        jsonfile.write(']')

def replace(s1, s2, filename):
    command = 's/{}/{}/g'.format(s1, s2)
    replace = ['sed', '-i', command, filename]
    call(replace)

# exclude string columns from diagram
strColumn = ''
for key, value in firstRow.iteritems():
    if isinstance(value, basestring):
        strColumn += 'd != "{}" \&\& '.format(key)

# generate colors for all group values
colors = {}
for i in groups:
    colors[i] = '#%06x' % random.randint(0, 0xFFFFFF)

# puts colours in with no quotes if groups have no quotes
if not isinstance(groups[0], basestring):
    replace('COLORS', str(colors)  + ';', baseDir + 'index.html')
else:
    replace('COLORS', json.dumps(colors)  + ';', baseDir + 'index.html')

replace('TITLE', path.split('/')[-1], baseDir + 'index.html')
replace('GROUPS', json.dumps(groups) + ';', baseDir + 'index.html')
replace('EXCLUDE', strColumn, baseDir + 'files/parallel-coordinates.js')
replace('GROUP', groupColumn, baseDir + 'files/parallel-coordinates.js')

print "Saved to: " + baseDir
