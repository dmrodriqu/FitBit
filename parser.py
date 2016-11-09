import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize
import string

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
        self.recursiveCount = 0
        self.dframeLen = 0

    def recursiveRows(self, dataFrame, column,  dataType):
        # type: (DataFrame) -> (Series)

        if self.recursiveCount == 0:
            self.dframeLen = len(dataFrame)
            self.recursiveCount += 1
            return self.recursiveRows(dataFrame, column,  dataType)
        if self.recursiveCount > 0:
            if self.recursiveCount > self.dframeLen:
                a = []
                b = 0
                self.recursiveCount = b
                self.sleepFrame = a
                return self.recursiveRows(dataFrame, column, dataType)
            if len(dataFrame) == 0:
                return pd.Series(self.sleepFrame)
            else:
                if len(dataFrame) == 1:
                    row = dataFrame[:]
                    litmus = row[column]
                    self.sleepFrame.append(litmus.values[0][dataType])
                    return self.recursiveRows(dataFrame[1:], column, dataType)
                else:
                    row = dataFrame[:-(len(dataFrame)) + 1]
                    litmus = row[column]
                    self.sleepFrame.append(litmus.values[0][dataType])
                    return self.recursiveRows(dataFrame[1:], column, dataType)

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




def createPsqiTable(originalDataFrame):
    arrayOfQuestions = []
    arrayOfPsqiFrames = []
    listOfSubQuestions = []
    psqiSubQ5 = string.uppercase[7::-1]
    i = 0
    questiondigits = map(lambda x: x+1, (range(10)))
    for digit in questiondigits:
        questionString = "UChicagoIBD/PSQI/Q%s" % digit
        arrayOfQuestions.append(questionString)
    for char in psqiSubQ5:
        listOfSubQuestions.append("UChicagoIBD/PSQI/Q5%s" % char)
    for q in listOfSubQuestions:
        arrayOfQuestions.insert(4, q)
    arrayOfQuestions.remove('UChicagoIBD/PSQI/Q5')
    while i < len(arrayOfQuestions):
        question = Table()
        psqirow = question.recursiveRows(originalDataFrame, 'Litmus', str(arrayOfQuestions[i]))
        expandedPsqi = question.createStepOrHeartColumns(originalDataFrame, psqirow)
        expandedPsqi['PsqiQuestionID'] = i
        print expandedPsqi
        arrayOfPsqiFrames.append(expandedPsqi)
        i += 1
    return pd.concat(arrayOfPsqiFrames, axis = 1)

fullDataFrame = parseJsonFile(fpath)
#psqiTable = createPsqiTable(fullDataFrame)
#print psqiTable


def createSibdqTable(originalDataFrame):
    arrayOfQuestions = []
    arrayOfPsqiFrames = []
    i = 0
    # create array of digits, one for each question
    questiondigits = map(lambda x: x+1, (range(9)))
    # create question strings
    for digit in questiondigits:
        questionString = "UChicagoIBD/SIBDQ/Q%s" % digit
        arrayOfQuestions.append(questionString)
    while i < len(arrayOfQuestions):
        question = Table()
        psqirow = question.recursiveRows(originalDataFrame, 'Litmus', str(arrayOfQuestions[i]))
        expandedPsqi = question.createStepOrHeartColumns(originalDataFrame, psqirow)
        expandedPsqi['SibdqQuestionID'] = i
        print expandedPsqi
        arrayOfPsqiFrames.append(expandedPsqi)
        i += 1
    return pd.concat(arrayOfPsqiFrames, axis = 1)

sibdqTable = createSibdqTable(fullDataFrame)
print sibdqTable
