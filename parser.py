import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize
import string
import datetime

fpath = '/Volumes/rubin-lab/UChicagoIBD_data.json'

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

#fullDataFrame = parseJsonFile(fpath)
#psqiTable = createSurveyTable(fullDataFrame, 'PSQI')
#sibdqTable = createSurveyTable(fullDataFrame, 'SIBDQ')

#steps = Table()
#stepSeries = steps.recursiveRows(fullDataFrame, 'Fitbit', 'Steps')
#stepFrame = steps.createStepOrHeartColumns(fullDataFrame, stepSeries)

#sleep = Table()
#sleepSeries = sleep.recursiveRows(fullDataFrame, 'Fitbit', 'Sleep')
#sleepFrame = sleep.createSleepColumns(fullDataFrame, sleepSeries)

#heart = Table()
#heartSeries = heart.recursiveRows(fullDataFrame, 'Fitbit', 'Heart')
#heartFrame = heart.createStepOrHeartColumns(fullDataFrame, heartSeries)


# Available tables:
# psqiTable
# sibdqTable
# stepFrame
# sleepFrame
# heartFrame

def convertToDate(timeStamp):
    time = datetime.datetime.fromtimestamp(timeStamp / 1e3)
    return time.date()

def readableDate(surveyFrame):
    # Set datetimes
    surveyFrame['TimeCompleted'] = map(lambda x: convertToDate(x), surveyFrame['TimeCompleted'])
    return surveyFrame

# for each unique date get ID
def getUniqueIds(SurveyFrame):
    # getting unique IDs
    idToScore = SurveyFrame['ID'].unique()
    scoringFrame = []
    for each in idToScore:
        # unique frame per ID
        uniqueIDFrame = SurveyFrame[SurveyFrame['ID'] == each]
        uniqueTimes = uniqueIDFrame['TimeCompleted'].unique()
        for uniqueTime in uniqueTimes:
            scoringFrame.append(uniqueIDFrame[uniqueIDFrame['TimeCompleted'] == uniqueTime]
                                [['PSQIQuestionID','Value', 'ID', 'TimeCompleted']])
    return scoringFrame

# begin scoring:
def questionSelector(dataFrame,numOFQuestion):
    questionCondition = dataFrame['PSQIQuestionID'] == numOFQuestion
    return dataFrame[questionCondition]['Value']

def scoreRaw(dataFrame):
    i=0
    questionValueArray = []
    while i<=17:
        questionValues = questionSelector(dataFrame, i)
        if 4 <= i < 17:
            questionValueArray.append(questionValues.values[0] - 1)
        if i == 1:
            valfor2 = (questionValues.values[0] - 1)
            if valfor2 > 3:
                valfor2 = 3
            questionValueArray.append(valfor2)
        if i == 3:
            questionValueArray.append(questionValues.values[0] + 1)
        if i == 0:
            if questionValues.values == 1:
                questionValueArray.append(20.0)
            if questionValues.values == 2:
                questionValueArray.append(20.5)
            if questionValues.values == 3:
                questionValueArray.append(21.5)
            if questionValues.values == 4:
                questionValueArray.append(22.5)
            if questionValues.values == 5:
                questionValueArray.append(23.5)
            if questionValues.values == 6:
                questionValueArray.append(0.5)
            if questionValues.values == 7:
                questionValueArray.append(1.0)
        i+=1
    return questionValueArray

class Psqi:
    def __init__(self, scoreArray):
        self.scoreArray = scoreArray
        self.comp1 = 0
        self.comp2 = 0
        self.comp3 = 0
        self.comp4 = 0
        self.comp5 = 0
        self.comp6 = 0
        self.comp7 = 0
        self.score = 0

    def scoreall(self):
        self._psqiComp1(self.scoreArray)
        self._psqiComp2(self.scoreArray)
        self._psqiComp3(self.scoreArray)
        self._psqiComp4(self.scoreArray)
        self._psqiComp5(self.scoreArray)
        self._psqiComp6(self.scoreArray)
        self._psqiComp7(self.scoreArray)

    def _psqiComp1(self, scoreArray):
        comp1 = scoreArray[13]
        self.comp1 = comp1
        return self.comp1

    def _psqiComp2(self, scoreArray):
        # comp2
        modscore = scoreArray[1] + scoreArray[4]
        if 1 <= modscore <= 2:
            modscore = 1
        elif 3<= modscore <= 4:
            modscore = 2
        elif modscore > 4:
            modscore = 3
        else:
            modscore = 0
        comp2 = modscore
        self.comp2 = comp2
        return self.comp2

    def _psqiComp3(self, scoreArray):
        if scoreArray[3] > 7:
            comp3 = 0
        elif 6 <= scoreArray[3] < 7:
            comp3 = 1
        elif 5 <= scoreArray[3] < 6:
            comp3 = 2
        elif scoreArray[3] < 5:
            comp3 = 3
        else:
            comp3 = 0
        self.comp3 = comp3
        return self.comp3

    def _psqiComp4(self, scoreArray):
        if (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 > 100:
            comp4 = 0
        elif 75 <= (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 <= 84:
            comp4 = 1
        elif 65 <= (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 <= 74:
            comp4 = 2
        elif (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 < 65:
            comp4 = 3
        self.comp4 = comp4
        return self.comp4

    def _psqiComp5(self, scoreArray):
        comp5 = sum(scoreArray[5:13])
        if 1 <= comp5 <= 9:
            comp5 = 1
        if 10 <= comp5 <= 18:
            comp5 = 2
        if 18 < comp5:
            comp5 = 3
        else:
            comp5 = 0
        self.comp5 = comp5
        return self.comp5

    def _psqiComp6(self, scoreArray):
        comp6 = scoreArray[14]
        self.comp6 = comp6
        return self.comp6

    def _psqiComp7(self, scoreArray):
        comp7 = sum(scoreArray[15:17])
        if 1 <= comp7 <= 2:
            comp7 = 1
        if 3 <= comp7 <= 4:
            comp7 = 2
        if 4 < comp7:
            comp7 = 3
        else:
            comp7 = 0
        self.comp7 = comp7
        return self.comp7

    def globalPsqi(self):
        self.score = self.comp1 + self.comp2 + self.comp3 + self.comp4 + self.comp5 + self.comp6 + self.comp7
        return self.score

#psqiTable = readableDate(psqiTable)
#i = 0
#while i < len(getUniqueIds(psqiTable)):
#    itemToScore = getUniqueIds(psqiTable)[i]
#    ptID = itemToScore['ID'].unique()[0]
#    newScore = Psqi(scoreRaw(itemToScore))
#    newScore.scoreall()
#    print newScore.globalPsqi(), ptID
#    i += 1

