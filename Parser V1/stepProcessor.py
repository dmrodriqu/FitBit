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
class HDretrieve:
    # initializing values:
    # dataToRead is the stepFrame.csv file
    # qID is the ID to be queried
    def __init__(self, filepath, qID):

        self.ID = qID
        self.frame = self.readFrame(filepath)

    def readFrame(self, filepath , dataToRead = 'stepFrame'):
        # fpath -> pd.DataFrame
        # readFrame takes the stepframe CSV file
        # and sets the self.frame variable to the DataFrame
        # with selected conditions below
        # line below: reading CSV to variable "data"
        query = '%s' % (self.ID)
        cond = "ID == "
        retrieval = cond + query
        data = pd.read_hdf(filepath, dataToRead,  where = retrieval)
        #data = data['stepFrame']
        # creating a condition variable for indexing the resulting
        # pd.DateFrame. only selecting data for the ID to be queried
        #cond = data['ID'] == self.ID
        #col = ['ID', 'Date', 'Total']
        # setting variable self.frame to subset of dataframe
        return data

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
        new = HDretrieve('stepFrame.h5', self.ID)
        df = new.frame
        col = ['Date', 'Total']

        def getVals(series):
            return series.values

        if graphReady is False:
            return df[col]
        elif graphReady is True:
            if withTimeSeries is True:
                self.Timeseries = getVals(df['Timeseries'])
            else:
                pass
            self.date = getVals(df['Date'])
            self.Total = getVals(df['Total'])
        else:
            pass
