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
	table['timeRequested'] = table.timeRequested.apply(convertTime)
	return table[['timeRequested','timeCompleted', 'id', 'survey', 'value']]
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

def getEachIDCompletedTask(df):
	groupColumns = ['survey', 'timeCompleted']
	i = 0
	while i < len(df.id.unique()):
		yield df.pivot_table(index = 'id', columns = groupColumns, values = 'value').ix[i:i+1]#dropna(axis = 1)
		i += 1

def getEachIDRequested(df):
	groupColumns = ['survey', 'timeRequested']
	i = 0
	while i < len(df.id.unique()):
		yield df.pivot_table(index = 'id', columns = groupColumns, values = 'value').ix[i:i+1]#.dropna(axis = 1)
		i += 1

a = [x for x in getEachIDCompletedTask(start)][0]
b =[x for x in getEachIDRequested(start)][0]
c = pd.DataFrame(b.iloc[0]).reset_index()
d = pd.DataFrame(a.iloc[0]).reset_index()
print c.merge(d)[['survey', 'DUofMl', 'timeCompleted']].drop_duplicates()

