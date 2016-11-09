import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize
import string
import datetime

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

def defineQuestionStrings(Survey):
    # raise error if user tries to input anything other than PSQI or SIBDQ
    try:
        Survey == 'PSQI' or 'SIBDQ'
    except ValueError:
        print ("Survey Origin for function defineQuestionStrings must be PSQI or SIBDQ")
    finally:
        # set up initial arrays for questions
        arrayOfQuestions = []
        if Survey == 'PSQI':
            # set up array for sub question only if PSQI
            listOfSubQuestions = []
            questiondigits = map(lambda x: x + 1, (range(10)))
            # alpha suffix a-H reversed for insertion for Q5
            psqiSubQ5 = string.uppercase[:8]
            for char in psqiSubQ5:
                listOfSubQuestions.append("UChicagoIBD/%s/Q5%s" % (Survey, char))
        elif Survey == 'SIBDQ':
            # only need digits to append to end of Q
            questiondigits = map(lambda x: x + 1, (range(9)))
        for digit in questiondigits:
            questionString = "UChicagoIBD/%s/Q%s" % (Survey,digit)
            arrayOfQuestions.append(questionString)
        if Survey == 'PSQI':
            arrayOfQuestions[4:4] = listOfSubQuestions
            arrayOfQuestions.remove('UChicagoIBD/PSQI/Q5')
        return arrayOfQuestions



def createSurveyTable(originalDataFrame, surveyType):
    arrayOfQuestions = defineQuestionStrings(surveyType)
    arrayOfPsqiFrames = []
    i = 0
    while i < len(arrayOfQuestions):
        question = Table()
        psqirow = question.recursiveRows(originalDataFrame, 'Litmus', str(arrayOfQuestions[i]))
        expandedPsqi = question.createStepOrHeartColumns(originalDataFrame, psqirow)
        expandedPsqi[('%sQuestionID') % surveyType] = i
        arrayOfPsqiFrames.append(expandedPsqi)
        i += 1
    return pd.concat(arrayOfPsqiFrames).reset_index()



#parsing data

fullDataFrame = parseJsonFile(fpath)
psqiTable = createSurveyTable(fullDataFrame, 'PSQI')
sibdqTable = createSurveyTable(fullDataFrame, 'SIBDQ')

steps = Table()
stepSeries = steps.recursiveRows(fullDataFrame, 'Fitbit', 'Steps')
stepFrame = steps.createStepOrHeartColumns(fullDataFrame, stepSeries)

sleep = Table()
sleepSeries = sleep.recursiveRows(fullDataFrame, 'Fitbit', 'Sleep')
sleepFrame = sleep.createSleepColumns(fullDataFrame, sleepSeries)

heart = Table()
heartSeries = heart.recursiveRows(fullDataFrame, 'Fitbit', 'Heart')
heartFrame = heart.createStepOrHeartColumns(fullDataFrame, heartSeries)


# Available tables:
# psqiTable
# sibdqTable
# stepFrame
# sleepFrame
# heartFrame

def convertToDate(timeStamp):
    time =  datetime.datetime.fromtimestamp(timeStamp / 1e3)
    return time.date()

# get IDs
psqiTable['TimeCompleted'] = map(lambda x: convertToDate(x), psqiTable['TimeCompleted'])
print psqiTable['TimeCompleted'].unique()

# for each unique id get unique date values

# getting unique IDs
idToScore = psqiTable['ID'].unique()
for each in idToScore:
    # unique frame per ID
    uniqueIDFrame = psqiTable[psqiTable['ID'] == each]
    uniqueTimes = uniqueIDFrame['TimeCompleted'].unique()
    for uniqueTime in uniqueTimes:
        print uniqueIDFrame[uniqueIDFrame['TimeCompleted'] == uniqueTime][['PSQIQuestionID','Value', 'ID']]


