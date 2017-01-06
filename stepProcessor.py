# About
# -------
# stepProcessor.py is a module that takes the csv files parsed from JSON
# and extracts intraday step counts, total steps per day, and date of
# measure taken for a specific ID.
#
# The objective of this script is not to parse, but to create a **graph ready**
# data structure of parsed records
#
#
# Input Format
# ------------
#
# data are input in the following manner:
# | ID  |       Timeseries    |   Date   | Total
# | ID1 |  {timestamp, value} |  Date1   | totalDate1
# | ID1 |  {timestamp, value} |  Date2   | totalDate2
# | ID2 |  {timestamp, value} |  Date1   | totalDate1
# | ID2 |  {timestamp, value} |  Date2   | totalDate2
# | ID3 |  {timestamp, value} |  Date1   | totalDate1
# | ID4 |  {timestamp, value} |  Date1   | totalDate1
#
# Reqiurements
# ------------
# packages required: pandas
# from terminal "pip install pandas"
#
# Usage
# -----
# create new object timeseries and init with desired ID.
#
# desiredID = "replace_with_desired_pt_ID_include_quotes"
# newStepFrameObject = Timeseries(ID)
#
# newStepFrameObject.stepCountByID()
#   options: withTimeSeries = False, True
#   False default value
#   includes timeseries
#
# this will define:
# newStepFrameObject.TimeSeries (if withTimeSeries = True)
# newStepFrameObject.Total
# newStepFrameObject.Date
#
# Support
# -------
# for issues dylanmr@uchicago.edu


import pandas as pd


# data = pd.read_csv('stepFrame.csv')

# child class of Timeseries
class stepFrame:
    # initializing values:
    # dataToRead is the stepFrame.csv file
    # qID is the ID to be queried
    def __init__(self, dataToRead, qID):
        self.frame = None
        self.uniqueID = None
        self.ID = qID
        self.readFrame(dataToRead)
        self.findUniqueID()

    def readFrame(self, dataToRead):
        # fpath -> pd.DataFrame
        # readFrame takes the stepframe CSV file
        # and sets the self.frame variable to the DataFrame
        # with selected conditions below
        # line below: reading CSV to variable "data"
        data = pd.read_csv(dataToRead)
        # creating a condition variable for indexing the resulting
        # pd.DateFrame. only selecting data for the ID to be queried
        cond = data['ID'] == self.ID
        # setting variable self.frame to subset of dataframe
        self.frame = data[cond][['ID', 'Timeseries', 'Date', 'Total']]

    # deprecated
    def findUniqueID(self):
        data = self.frame
        self.uniqueID = data['ID'].unique()

# main class


class Timeseries:

    # initializing Timeseries with var ID: the ID to be queried
    # initializing other vars to be used later with None Type
    def __init__(self, ID):
        self.Timeseries = None
        self.Total = None
        self.Date = None
        self.ID = ID

    def stepCountByID(self, withTimeSeries=False, graphReady=False):
        # self -> pd.Series
        # returns no value, takes an option
        # withTimeSeries = False is the default option,
        # if True, self.Timeseries is set to timeseries values
        # test case ID 'BLqS60'
        # setting queryID to self.ID
        queryID = self.ID
        # creating new stepframe object and initializing with 'stepframe.csv'
        # and queryID
        new = stepFrame('stepFrame.csv', queryID)
        if graphReady is False:
            return new.frame[['Date', 'Total']]
        elif graphReady is True:
            if withTimeSeries is True:
                self.Timeseries = new.frame['Timeseries'].values
            else:
                pass
            self.date = new.frame['Date'].values
            self.Total = new.frame['Total'].values
        else:
            pass
        # print new.frame['ID']

        # for eachID in new.frame[new.frame['ID'] == queryID]:
        #    # newGraph = Timeseries()
        #    if withTimeSeries is True:
        #        self.Timeseries = new.frame['Timeseries'].values
        #    else:
        #        pass
        #    # self.ID = new.frame['ID'].values
        #    self.Date = new.frame['Date'].values
        #    self.Total = new.frame['Total'].values
        #    # graphlist.append(newGraph)

        # timeseries[0,1,2,3...n]- 1:1 with  date
        # date[0,1,2,3...n]-------1:1 with timeseries
        # id[0,1,2,3...n]

        # return graphlist[0].Total
