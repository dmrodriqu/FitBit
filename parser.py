import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize

fpath = '/Users/Dylan/Dropbox/FitBit/UChicagoIBD_data.json'

def parseJsonFile(path):
    # type: (String) -> (DataFrame)
    json_to_parse = open(path).read()
    fullFrame = pd.read_json(json_to_parse, orient='index')
    fullFrame['ID'] = fullFrame.index
    return fullFrame.reset_index()


class Table:

    def __init__(self):
        self.sleepFrame = []
        self.listOfExpandedFrames = []
        self.FramesToConcatenate = []

    def recursiveRows(self, dataFrame, column,  dataType):
        # type: (DataFrame) -> (Series)
        if len(dataFrame) == 0:
            return pd.Series(self.sleepFrame)
        else:
            if len(dataFrame) == 1:
                row = dataFrame[:]
                litmus = row[column]
                self.sleepFrame.append(litmus.values[0][dataType])
                return self.recursiveRows(dataFrame[1:], dataType)
            else:
                row = dataFrame[:-(len(dataFrame)) + 1]
                litmus = row[column]
                self.sleepFrame.append(litmus.values[0][dataType])
                return self.recursiveRows(dataFrame[1:], dataType)

    def createSleepColumns(self, originalDataFrame, seriesToExpand):
        # type: (Series) -> (DataFrame)
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

    def createStepOrHeartColumns(self, originalDataFrame, seriesToExpand):
        # type: (Series) -> (DataFrame)
        indexCount = 0
        while indexCount < len(seriesToExpand):
            for x in seriesToExpand:
                if type(x) is list:
                    stepFrameToModify = pd.DataFrame.from_records(x)
                    stepFrameToModify['ID'] = originalDataFrame.ix[indexCount]['ID']
                    self.FramesToConcatenate.append(stepFrameToModify)
                else:
                    pass
                indexCount += 1
        return pd.concat(self.FramesToConcatenate).reset_index()


def concatStepHeartSleep(fileToJson):
    parsedJson = parseJsonFile(fileToJson)
    # Heart
    heartTable = Table()
    heartRows = heartTable.recursiveRows(parsedJson, 'Fitbit', 'Heart')
    heartDataFrame = heartTable.createStepOrHeartColumns(parsedJson, heartRows)
    # Steps
    sleepTable = Table()
    sleepRows = sleepTable.recursiveRows(parsedJson, 'Fitbit', 'Sleep')
    sleepDataFrame = sleepTable.createSleepColumns(parsedJson, sleepRows)
    # Sleep
    stepTable = Table()
    stepsRows = stepTable.recursiveRows(parsedJson, 'Fitbit', 'Steps')
    stepDataFrame = sleepTable.createStepOrHeartColumns(parsedJson, stepsRows)

    frame1 = pd.merge(heartDataFrame,sleepDataFrame, on = 'ID')
    return frame1



