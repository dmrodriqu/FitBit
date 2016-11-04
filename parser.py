import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize


## note ##

# new method to extract updated data stream. Tested with sleep data
# abstraction upcomming



fpath = '/Users/Dylan/Dropbox/FitBit/UChicagoIBD_data.json'


def parseJsonFile(path):
    json_to_parse = open(path).read()
    data = json.loads(json_to_parse)
    subjectIDs = data.keys()

    fullFrame = pd.read_json(json_to_parse,
                             orient='index')
    return fullFrame

table = parseJsonFile(fpath)
table['ID'] = table.index
table = table.reset_index()
#print table

#print table['Fitbit']
i = 0
sleepSeries = []

sleepFrame = []


def recursiveRows (dataFrame, dataType):
    if len(dataFrame)==0:
        return pd.Series(sleepFrame)
    else:
        if len(dataFrame) == 1:
            row = dataFrame[:]
            litmus = row['Fitbit']
            sleepFrame.append(litmus.values[0][dataType])
            #sleepSeries.append(litmus[u'Sleep'])
            return recursiveRows(dataFrame[1:], dataType)
        else:
            row = dataFrame[:-(len(dataFrame))+1]
            litmus = row['Fitbit']
            sleepFrame.append(litmus.values[0][dataType])
            #sleepSeries.append(litmus[u'Sleep'])
            return recursiveRows(dataFrame[1:], dataType)

concatenatedSleepFrames = recursiveRows(table, 'Sleep')
concatenatedStepFrames = recursiveRows(table, 'Steps')

def createSleepColumns(originalDataFrame, seriesToExpand):
    indexCount = 0
    listOfExpandedFrames = []
    for row in seriesToExpand:
        if type(row) is None:
            print 'none'
            indexCount += 1
        else:
            tempframe = pd.DataFrame.from_dict(row)
            columncount = 1
            while columncount < len(list(tempframe.columns.values)):
                columnToParse = tempframe.ix[:, columncount]
                for jsonRow in columnToParse:
                    totalSleepFrame = pd.DataFrame.from_dict(jsonRow[0])
                    totalSleepFrame['ID'] = originalDataFrame.ix[indexCount]['ID']
                    listOfExpandedFrames.append(totalSleepFrame)
                    columncount += 1
            indexCount += 1

    return pd.concat(listOfExpandedFrames)


#works!
print createSleepColumns(table, concatenatedSleepFrames)




