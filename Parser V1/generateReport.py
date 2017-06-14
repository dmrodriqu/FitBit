# $generateReport.py
# about
# -----
# $generateReport.py generates a report to allow the
# Clinical Staff to find out who has completed
# and not completed the tasks during the fitbit study

import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np

from os import listdir
from os.path import isfile, join
mypath = '/Volumes/rubin-lab/FitBit'
onlyfiles = [f for f in listdir(mypath) if isfile(
    join(mypath, f)) and '.h5' in f and 'TimeSeries' not in f]


dataArr = []

print onlyfiles
addToDataArr = dataArr.append
for file in onlyfiles:
    tablename = file[:-3]
    print tablename
    tableString = '%s.h5' % tablename
    data = pd.read_hdf(tableString, tablename)['ID'].unique()
    addToDataArr({tableString: data})

newFrames = []
addToNew = newFrames.append
for each in dataArr:
    addToNew(pd.DataFrame(each))

result = pd.concat(newFrames, axis=1)

print result
