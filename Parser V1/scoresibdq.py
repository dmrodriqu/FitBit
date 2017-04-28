import openh5
import time
import pandas as pd
sibdq = openh5.openData('sibdq')
sibdq.formatOpeningQuery()


# basic date formatting before the tree gets constructed.

def convertTime():
	times = ['TimeCompleted', 'TimeRequested']
	df = sibdq.df
	timeConversion = [(df[x]*1000000).apply(pd.to_datetime) for x in times] # pythonic!
	i = 0
	while i < len(timeConversion):
		df[times[i]] = timeConversion[i]
		i+=1
	df['TimeRequested'] = df['TimeRequested'].dt.strftime('%Y-%m-%d')
	return df

tempTable = convertTime()

def getIDs(table):
	ids = table.ID.value_counts().reset_index().ix[:,:-1].values
	i = 0
	listOfIDs = [] 
	addToListOfIDs = listOfIDs.append
	while i < len(ids): 			# naieve! 
		addToListOfIDs(ids[i][0])
		i +=1
	return listOfIDs

tempids =  getIDs(tempTable)

tempTable = tempTable[tempTable.ID == tempids[0]].sort_values('TimeCompleted')

tempTimes =  tempTable.TimeRequested.value_counts().reset_index().ix[:,:-1].values

def getUniqueVals(table, column):
	return table[column].value_counts().reset_index().ix[:,:-1].values

def flatten(vals):
	i = 0
	listOfVals = [] 
	addTolistOfVals = listOfVals.append
	while i < len(vals): 			# naieve! 
		addTolistOfVals(vals[i][0])
		i +=1
	return listOfVals

def getFlattenedUniqueVals(table, column):
	vals = getUniqueVals(table, column)
	return flatten(vals)

#print tempTable
#print getFlattenedUniqueVals(tempTable, 'TimeRequested')

# getIDs, sort, getDates
# function, sort, function

# for each date in SibdqParticipant, create SibdqParticipantSurvey

class SibdqParticipantSurvey: # the bottom of the class. contains all necessary scores

	def __init__(self):
		self.id = None
		self.date = None
		self.score = None


# for each id in SibdqScoringTree, create SibdqParticipant

class SibdqParticipant:

	def __init__(self, subjectID):
		self.id = subjectID
		self.surveys = [] # the dates for the SIBDQ go here
		self.surveyScores = []

	def _getUniqueVals(self, dataframe, column):
		return dataframe[column].value_counts().reset_index().ix[:,:-1].values
	

class SibdqScoringTree: # put entire database here, root to query
	
	
	def __init__(self, tableToSearch, column):
		self.uniqueIDs = None # IDs
		self.uniqueDate = None
		self.df = None # base dataframe
		self.base = []
		self.getdata(tableToSearch)
		self.getFlattenedUniqueVals(self.df, 'ids', column)

	def _setUniqueIDs(self, vals):
		self.uniqueIDs = vals

	def _setUniqueDate(self, vals):
		self.uniqueDate = vals

	def _convertTime(self, table): # convert unix epochs of the scoring tree
		times = ['TimeCompleted', 'TimeRequested'] # next time find cols with datatype as datetime -> reindex columns to be continuous -> use same timeConversion function.
		df = table                                 # always keep one with extended time information for sorting purposes.
		timeConversion = [(df[x]*1000000).apply(pd.to_datetime) for x in times] # pythonic!
		i = 0
		while i < len(timeConversion):
			df[times[i]] = timeConversion[i]
			i+=1
		df['TimeRequested'] = df['TimeRequested'].dt.strftime('%Y-%m-%d')
		return df

	def getdata(self, tableToSearch): # puts df in the scoring tree
		sibdq = openh5.openData(tableToSearch)
		sibdq.formatOpeningQuery()
		convertedDataFrame = self._convertTime(sibdq.df)
		self.df = convertedDataFrame


	def _getUniqueVals(self, dataframe, column):
		return dataframe[column].value_counts().reset_index().ix[:,:-1].values

	def _flatten(self, vals):
		i = 0
		listOfVals = [] 
		addTolistOfVals = listOfVals.append
		while i < len(vals): 			# naieve! 
			addTolistOfVals(vals[i][0])
			i +=1
		return listOfVals
	
	def getFlattenedUniqueVals(self, dataframe, destination, column):
		vals = self._getUniqueVals(dataframe, column)
		self._flatten(vals)
		if destination == 'ids':
			self._setUniqueIDs(self._flatten(vals))
		elif destination == 'dates':
			self._setUniqueDate(self._flatten(vals))

	def _acquireAndSort(self, dataframe, columnToAcquire, equivalency, columnToSort):
		return dataframe[dataframe[columnToAcquire] == equivalency].sort_values(columnToSort)

	def getSurveys(self):
		for eachID in self.uniqueIDs:
			subject = SibdqParticipant(eachID)
			df2 = self._acquireAndSort(self.df, 'ID', subject.id, 'TimeCompleted')
			self.getFlattenedUniqueVals(df2, 'dates', 'TimeRequested')
			surveyPerTime = []
			addToSurveyPerTime = surveyPerTime.append
			for eachTime in self.uniqueDate:
				df3 = self._acquireAndSort(df2, 'TimeRequested', eachTime,'TimeCompleted')
				addToSurveyPerTime(df3)
			subject.surveys = surveyPerTime
			self.base.append(subject)



tree = SibdqScoringTree('sibdq', 'ID')
print tree
print tree.uniqueIDs
tree.getSurveys()
for each in tree.base:
	print each.surveys

## for tomorrow:

'''
id > date > group surveys by date

'''






