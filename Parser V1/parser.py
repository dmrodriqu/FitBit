# $Parser
# -------
# $parser is a framework for parsing the incoming Fitbit data from JSON to csv files.
# $parser identifies the correct record for each ID and places IDs in their records,
# along with the appropriate information.
#
# This is accomplished by separating tables by litmus or fitbit tables and walking through records,
# indexing by ID and then resetting the index of the table.
#
#
# Several other functions are included to assist in scoring the PSQI
#
#
# Input/Output Format
# ------------
#
# The JSON file is formatted thusly:
#
#
#  ID:{                                    -- each record key is a pt ID
#       Litmus:{
#           "UChicagoIBD/SURVEY/Q#":[
#            {"TimeCompleted": timestamp,  -- for each time completed, a new instance will appear
#             "TimeRequested": timestamp,  -- under the same question/survey ID
#              value: int
#            },
#            {"TimeCompleted": timestamp,
#             "TimeRequested": timestamp,
#              value: int
#            },
#          ],
#          "UchicagoIBD/SleepQualityVAS": [
#           {"TimeCompleted": timestamp,
#            "TimeRequested": timestamp,
#            value: int
#           },
#         ],
#          "UchicagoIBD/SubjectGlobalAssessmentVAS": [
#           {"TimeCompleted": timestamp,
#            "TimeRequested": timestamp,
#            value: int
#           },
#         ],
#          "UchicagoIBD/WongBaker": [
#           {"TimeCompleted": timestamp,
#            "TimeRequested": timestamp,
#            value: int
#           },
#         ],
#          "location": [
#              {"TimeCompleted": timestamp,
#               "TimeRequested": timestamp,
#                  "Value": {
#                  "Lat" : float64
#                  "Lon" : float64
#                  }
#              },
#          ],
#       },
#       "Fitbit" : {
#           "Sleep" : [
#             {
#               "date": datetime
#               "sleep": [
#                 {
#                   "AwakeCount": int,
#                   "AwakeDuration": int,
#                   "AwakeningsCount": int,
#                   "DateOfSleep": string of date, --- this is a string of a date
#                   "Duration": int64,             ---  must be converted (it is later)
#                   "Efficiency": int,
#                   "IsMainSleep": bool,
#                   "LogID": int64,
#                   "MinutesAfterWakeup": int,
#                   "MinutesAsleep": int,
#                   "MinutesAwake": int,
#                   "MinutesToFallAsleep": int,
#                   "RestlessCount": int,
#                   "RestlessDuration": int,
#                   "StartTime": timestamp,
#                   "TimeInBed": int,
#                   "MinuteData": [
#                      {
#                        "Timestamp": timestamp,
#                        "Value": int            --- range from [1, 3]
#                      },
#                   ],
#                   "summary": {
#                     "totalMinutesAsleep": int,
#                     "totalSleepRecords": int,
#                     "totalTimeInBed": int
#                   }
#               ]
#             }
#           ]
#           "Steps": [
#             {
#               "UserID": string,              --- this string is an arbitrary
#               "Date": string of datetime,    --- identifier and should not be used
#               "Total": int,
#               "Timeseries": [
#                 {
#                   "Timestamp": timestamp,
#                   "Value": int
#                 }
#               ],
#               "Interval" : int,             ---- number unit elapsed before measurement taken
#               "DatasetType": string         ---- DatasetType = minute
#             },
#           },
#           "Heart": [
#             {
#               "UserID": string,             --- this string is an arbitrary
#               "Date": string of datetime,   --- identifier and should not be used
#               "Zones": [
#                 {
#                   "CaloriesOut": float,
#                   "Max": int,
#                   "Min": int,
#                   "Minutes": int,
#                   "Name": string
#                 },
#               ],
#               "RestingHeartRate": int,
#               "Timeseries": [
#                 {
#                   "Timestamp": int64,
#                   "Value": int
#                 },
#               ],
#               "Interval": int,
#               "DatasetType": string
#             },
#       },
# },
#
#
#
# Reqiurements
# ------------
# pandas
# datetime
# string
# modules required:
# -----------------
#
#
# Usage
# -----
# Several functions and classes are present in this module
#
# parseJsonFile(path)
# >>> fpath = '/Volumes/rubin-lab/UChicagoIBD_data.json'
# >>> parseJsonFile(fpath)
# [FITBIT] [SLEEP HEART STEPS]
# [LITMUS] [SURVEY SURVEY SURVEY]
#
# Table() is the most prominent of the classes/functions
#
# parser.Table()
#     attributes:
#     -----------
#     recursiveRows(dataFrame, column, dataType)
#     dataFrame = pd.Dataframe
#
#     column = "Litmus" or "Fitbit",
#     dataType = if column is  "Litmus"
#                "SIBDQ"
#                "PSQI"
#                if column is "Fitbit"
#                "Sleep"
#                "Step"
#                "Heart"
#
#
#     createSleepColumns(originalDataFrame, seriesToExpand)
#     originalDataFrame = dataFrame from which json was parsed
#
#     seriesToExpand = sleepseries
#
#     the above is respective of the dataType of the dataType
#     in recursiveRows
#
#     createStepOrHeartColumns(originalDataFrame, seriesToExpand)
#
#     seriesToExpand = stepseries or heartseries
#
#     the above is respective of the dataType of the dataType
#     in recursiveRows
#
# >>> steps = Table()
# <new Table Object >
# >>> stepSeries = steps.recursiveRows(fullDataFrame, 'Fitbit', 'Steps')
#  ID  | AWAKEDURATION  AWAKECOUNT   DURATION DATE  ...   MINUTEDATA
#  ID1 |      int      |     int   |   datetime1   |     |     int
#  ID2 |      int      |     int   |   datetime1   |     |     int
#  ID2 |      int      |     int   |   datetime2   |     |     int
#  ID3 |      int      |     int   |   datetime1   |     |     int
# >>> stepFrame = steps.createStepOrHeartColumns(fullDataFrame, stepSeries)
# ID SLEEP
# Support
# -------
# for issues dylanmr@uchicago.edu

import os
import pandas as pd
import datetime
import math
from pandas.io.json import json_normalize
import string
import datetime


def idsToDrop():
    listOfIDsToDrop = ['1diMEc', 'PeLZ9Z', 'GpvQSU', 'gRqhgp',
                       '46ZXoP', '2tcXat', 'KLZzPC', 'K1SEV1', 'GJbIM0', '5ieK0V']
    return listOfIDsToDrop
#fullDataFrame = parseJsonFile(fpath)
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

    def recursiveRows(self, dataFrame, column, dataType):
        # type: (DataFrame) -> (Series)
        if self.recursiveCount == 0:
            self.dframeLen = len(dataFrame)
            self.recursiveCount += 1
            return self.recursiveRows(dataFrame, column, dataType)
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
                        totalSleepFrame['ID'] = originalDataFrame.ix[
                            indexCount]['ID']
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
                    stepFrameToModify['ID'] = originalDataFrame.ix[
                        indexCount]['ID']
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
        print("Survey Origin for function defineQuestionStrings must be PSQI or SIBDQ")
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
                listOfSubQuestions.append(
                    "UChicagoIBD/%s/Q5%s" % (Survey, char))
        elif Survey == 'SIBDQ':
            # only need digits to append to end of Q
            questiondigits = map(lambda x: x + 1, (range(9)))
        for digit in questiondigits:
            questionString = "UChicagoIBD/%s/Q%s" % (Survey, digit)
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
        psqirow = question.recursiveRows(
            originalDataFrame, 'Litmus', str(arrayOfQuestions[i]))
        expandedPsqi = question.createStepOrHeartColumns(
            originalDataFrame, psqirow)
        expandedPsqi[('%sQuestionID') % surveyType] = i
        arrayOfPsqiFrames.append(expandedPsqi)
        i += 1
    return pd.concat(arrayOfPsqiFrames).reset_index()


def convertToDate(timeStamp):
    time = datetime.datetime.fromtimestamp(timeStamp / 1e3)
    return time.date()


def readableDate(surveyFrame):
    # Set datetimes
    surveyFrame['TimeCompleted'] = map(
        lambda x: convertToDate(x), surveyFrame['TimeCompleted'])
    return surveyFrame


def fitbitreadableDate(fitbitPassiveFrame):
    # Set datetimes
    fitbitPassiveFrame['Timestamp'] = map(
        lambda x: convertToDate(x), fitbitPassiveFrame['Timestamp'])
    return fitbitPassiveFrame


def sleepdates(sleepFrameDate):
    # Set datetimes
    sleepFrameDate['StartTime'] = map(
        lambda x: convertToDate(x), sleepFrameDate['StartTime'])
    return sleepFrameDate

# for each unique date get ID


def getUniqueIds(SurveyFrame):
    # Dataframe -> [Dataframe[id1] dataframe[id2]... dataframe[idN]]
    # gets unique times per ID
    # getting unique IDs
    idToScore = SurveyFrame['ID'].unique()
    scoringFrame = []
    for each in idToScore:
        # unique frame per ID
        uniqueIDFrame = SurveyFrame[SurveyFrame['ID'] == each]
        # get unique time per ID
        uniqueTimes = uniqueIDFrame['TimeCompleted'].unique()
        # get psqiquestions and values per unique time completed
        for uniqueTime in uniqueTimes:
            conditionForFrame = uniqueIDFrame['TimeCompleted'] == uniqueTime
            listOfCols = ['PSQIQuestionID', 'Value', 'ID', 'TimeCompleted']
            scoringFrame.append(uniqueIDFrame[conditionForFrame][listOfCols])
    return scoringFrame


def dataframePerID(surveyFrame, ID):
    # Dataframe, ID -> [dataframe[ID]]
    # get dataframe for specific ID
    data = surveyFrame[surveyFrame['ID'] == ID]
    # get unique times within dataframe
    data = data.drop_duplicates('TimeCompleted')
    return data


# begin scoring:


def questionSelector(dataFrame, numOFQuestion):
    questionCondition = dataFrame['PSQIQuestionID'] == numOFQuestion
    return dataFrame[questionCondition]['Value']


def scoreRaw(dataFrame):
    i = 0
    questionValueArray = []
    while i <= 17:
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
            if questionValues.values[0] == 1:
                questionValueArray.append(20.0)
            if questionValues.values[0] == 2:
                questionValueArray.append(20.5)
            if questionValues.values[0] == 3:
                questionValueArray.append(21.5)
            if questionValues.values[0] == 4:
                questionValueArray.append(22.5)
            if questionValues.values[0] == 5:
                questionValueArray.append(23.5)
            if questionValues.values[0] == 6:
                questionValueArray.append(0.5)
            if questionValues.values[0] == 7:
                questionValueArray.append(1.0)
        i += 1
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

    def _setScore(self, vals):
        self.score = vals

    def _setcomp1(self, vals):
        self.comp1 = vals

    def _setcomp2(self, vals):
        self.comp2 = vals

    def _setcomp3(self, vals):
        self.comp3 = vals

    def _setcomp4(self, vals):
        self.comp4 = vals

    def _setcomp5(self, vals):
        self.comp5 = vals

    def _setcomp6(self, vals):
        self.comp6 = vals

    def _setcomp7(self, vals):
        self.comp7 = vals

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
        self._setcomp1(comp1)


    def _psqiComp2(self, scoreArray):
        # comp2
        modscore = scoreArray[1] + scoreArray[4]
        if 1 <= modscore <= 2:
            modscore = 1
        elif 3 <= modscore <= 4:
            modscore = 2
        elif modscore > 4:
            modscore = 3
        else:
            modscore = 0
        comp2 = modscore
        self._setcomp2(comp2)


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
        self._setcomp3(comp3)


    def _psqiComp4(self, scoreArray):
        if (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 > 100:
            comp4 = 0
        elif 75 <= (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 <= 84:
            comp4 = 1
        elif 65 <= (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 <= 74:
            comp4 = 2
        elif (scoreArray[2] / (scoreArray[0] - scoreArray[2])) * 100 < 65:
            comp4 = 3
        self._setcomp4(comp4)


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
        self._setcomp5(comp5)

    def _psqiComp6(self, scoreArray):
        comp6 = scoreArray[14]
        self._setcomp6(comp6)


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
        self._setcomp7(comp7)


    def globalPsqi(self):
        self.score = self.comp1 + self.comp2 + self.comp3 + \
            self.comp4 + self.comp5 + self.comp6 + self.comp7
        self._setScore(self.score) #updated

# examples for use

# parsing data
#psqiTable = createSurveyTable(fullDataFrame, 'PSQI')
#sibdqTable = createSurveyTable(fullDataFrame, 'SIBDQ')
# print psqiTable[['index','ID']].drop_duplicates()


#steps = Table()
#stepSeries = steps.recursiveRows(fullDataFrame, 'Fitbit', 'Steps')
#stepFrame = steps.createStepOrHeartColumns(fullDataFrame, stepSeries)

#sleep = Table()
#sleepSeries = sleep.recursiveRows(fullDataFrame, 'Fitbit', 'Sleep')
#sleepFrame = sleep.createSleepColumns(fullDataFrame, sleepSeries)
# print sleepFrame[sleepFrame['ID'] == 'vB4y2r']


#heart = Table()
#heartSeries = heart.recursiveRows(fullDataFrame, 'Fitbit', 'Heart')
#heartFrame = heart.createStepOrHeartColumns(fullDataFrame, heartSeries)


#sibdqTable['TimeCompleted'] = map(lambda x: convertToDate(x) , sibdqTable['TimeCompleted'])
# print sibdqTable[sibdqTable['ID']== 'vZoyyc']

# Available tables:
# psqiTable
# sibdqTable
# stepFrame
# sleepFrame
# heartFrame
