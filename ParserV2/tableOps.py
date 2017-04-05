from parser import Table
import time
import pandas as pd
fpath = '/Volumes/rubin-lab/FitBit/JSON Files/download.json'


def stringCleaning(stringToClean): 
	return stringToClean[2:-2]

def convertTime(unixTime):
	return time.strftime('%Y-%m-%d', time.localtime(unixTime/1000))

def newTable(fpath):
	table = Table(fpath)
	col = table.parsedTable.columns
	for x in col[:-3:-1]:
		table.parsedTable[x] = table.parsedTable[x].apply(stringCleaning)
	return table.parsedTable

def getStartDates(table):
	#regex string for Demo, get all dates
	table['value'] = table['value'].astype(int)
	table['timeCompleted'] = table.timeCompleted.apply(convertTime)
	return table[['timeCompleted', 'id', 'survey', 'value']]
'''	
def _createKeysFromSurveys(startDataFrame):
	return map(str, startDataFrame.survey.values)

def _createValuesFromValuesInTable(startDataFrame):
	return list(startDataFrame['value'].values)

def createHashTableOfSurveyValueList(startDataFrame):
	x = _createKeysFromSurveys(startDataFrame)
	y = _createValuesFromValuesInTable(startDataFrame)
	return zip(x,y)

def createDfFromHashTable(startDataFrame):
	return pd.DataFrame.from_records(createHashTableOfSurveyValueList(startDataFrame))
'''
df = newTable(fpath)
start =  getStartDates(df)
start = start.reset_index()
print start.pivot_table(index = 'id', columns = ['survey', 'timeCompleted'], values = 'value')