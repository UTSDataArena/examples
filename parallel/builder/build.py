#!/usr/bin/python

import csv
import json
from distutils import dir_util 
from subprocess import call
import random
from sys import argv
from sys import platform

csvName = 'Public.csv'
groupColumn = 'Institution'
ordinals = []
excludes = []

if len(argv)>2:
    csvName = argv[1]
    groupColumn = argv[2]
    excludes = argv[3:]
else:
    print "Usage: {} <csv file> <group Column name>".format(argv[0])
    print "Example: {} Public.csv 'Institution'".format(argv[0])
    exit(1)

print "Using {} file and '{}' as Group".format(csvName, groupColumn)

path = csvName[:-4]
# has to end with /
baseDir = path + "/"
dir_util.mkpath(baseDir) 
dir_util.copy_tree('./template', baseDir)
 
print "Copied files to folder {}..".format(path)
groups = []
firstRow = {}

with open(csvName) as csvfile:
    reader = csv.DictReader(csvfile)
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

print "Wrote new json file {}".format(baseDir+ 'file/data.js')

def replace(s1, s2, filename):
    command = 's|{}|{}|g'.format(s1, s2)
    replace = ['sed', '-i', command, filename]
    # differences in sed on linux vs osx (http://stackoverflow.com/a/2321958)
    if 'darwin' in platform:
        replace = ['sed', '-i', '', command, filename]
    call(replace)

# figure out ordinals (they are columns that can't be converted to a float
# note: relying on the fact that an int can be considered a float
for key, value in firstRow.iteritems():
    try:
        float(value)
        print "Numeric", key, value
    except ValueError:
        print "Ordinal", key, value
        ordinals.append(key)

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
replace('GROUP', groupColumn, baseDir + 'index.html')
replace('ORDINALS', json.dumps(ordinals), baseDir + 'files/parallel-coordinates.js')
replace('EXCLUDES', excludes, baseDir + 'files/parallel-coordinates.js')
replace('GROUP', groupColumn, baseDir + 'files/parallel-coordinates.js')

print "Saved to: " + baseDir
