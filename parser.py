import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize





fpath = '/Users/Dylan/Dropbox/FitBit/UChicagoIBD_data.json'


class Table:

    def __init__(self):
        self.sleepFrame = []
        self.dataType = ''
        self.i = 0
        self.listOfExpandedFrames = []
        self.stepFramesToConcatenate = []
        self.heartFramesToConcatenate = []

    def parseJsonFile(self, path):
        json_to_parse = open(path).read()
        data = json.loads(json_to_parse)
        subjectIDs = data.keys()
        fullFrame = pd.read_json(json_to_parse, orient='index')
        fullFrame['ID'] = fullFrame.index
        return fullFrame.reset_index()


    def recursiveRows(self, dataFrame, dataType):
        if len(dataFrame) == 0:
            return pd.Series(self.sleepFrame)
        else:
            if len(dataFrame) == 1:
                row = dataFrame[:]
                litmus = row['Fitbit']
                self.sleepFrame.append(litmus.values[0][dataType])
                return self.recursiveRows(dataFrame[1:], dataType)
            else:
                row = dataFrame[:-(len(dataFrame)) + 1]
                litmus = row['Fitbit']
                self.sleepFrame.append(litmus.values[0][dataType])
                return self.recursiveRows(dataFrame[1:], dataType)

    def createSleepColumns(self, originalDataFrame, seriesToExpand):
        indexCount = 0
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
                        self.listOfExpandedFrames.append(totalSleepFrame)
                        columncount += 1
                indexCount += 1

        return pd.concat(self.listOfExpandedFrames).reset_index()

    def createStepOrHeartColumns(self, originalDataFrame, seriesToExpand, seriesName):
        indexCount = 0
        while indexCount < len(seriesToExpand):
            for x in seriesToExpand:
                if type(x) is list:
                    stepFrameToModify = pd.DataFrame.from_records(x)
                    stepFrameToModify['ID'] = originalDataFrame.ix[indexCount]['ID']
                    if seriesName == 'Steps':
                        self.stepFramesToConcatenate.append(stepFrameToModify)
                    if seriesName == 'Heart':
                        self.heartFramesToConcatenate.append(stepFrameToModify)
                else:
                    pass
                indexCount += 1
        if len(self.stepFramesToConcatenate)> 0:
            return pd.concat(self.stepFramesToConcatenate).reset_index()
        if len(self.heartFramesToConcatenate)>0:
            return pd.concat(self.heartFramesToConcatenate).reset_index()


new = Table()
table = new.parseJsonFile(fpath)
# Heart, Steps, Sleep
heartrows = new.recursiveRows(table, 'Heart')
print new.createStepOrHeartColumns(table, heartrows, 'Heart')
steprows = new.recursiveRows(table, 'Steps')
#print steprows
print new.createStepOrHeartColumns(table, steprows, 'Steps')

print len(new.stepFramesToConcatenate)