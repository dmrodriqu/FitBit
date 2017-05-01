import openh5
import time
import pandas as pd
import numpy as np


# globals

def _flatten(vals):
	i = 0
	listOfVals = [] 
	addTolistOfVals = listOfVals.append
	while i < len(vals): 			# naieve! 
		addTolistOfVals(vals[i][0])
		i +=1
	return listOfVals

def _getUniqueVals(dataframe, column):
	return dataframe[column].value_counts().reset_index().ix[:,:-1].values

def _getUniqueValuesAndFlatten(dataframe, column):
	return _flatten(_getUniqueVals(dataframe, column))

def _acquireAndSort(dataframe, columnToAcquire, equivalency, columnToSort):
	return dataframe[dataframe[columnToAcquire] == equivalency].sort_values(columnToSort)


class ParticipantSurvey: # the bottom of the class. contains all necessary scores and aggregate functions

	def __init__(self, surveyID, surveyDate, surveyScores):
		self.id = surveyID
		self.date = surveyDate
		self.score = surveyScores

	def _setScore(self, value):
		self.score = value

	def scoreSIBDQ(self):
		return np.sum(self.score)/9.0

	def scoreGlobalVas(self):
		return self.score[0]


# for each id in SibdqScoringTree, create SibdqParticipant

class Participant:

	def __init__(self, subjectID):
		self.id = subjectID
		self.surveys = [] # surveys for self.id
		self.surveysToScore = [] # raw data, in case per questions needed
		self.scoredSurveys = [] # all scored surveys via participantsurvey objects

	def _setSurveys(self, value):
		self.surveysToScore = value

	def populateScores(self):
		totalSurveys = []
		for eachSurvey in self.surveys:
			uniqueIndex = _getUniqueValuesAndFlatten(eachSurvey, 'index')
			surveys = []
			addToSurveys = surveys.append
			for eachIndex in uniqueIndex:
				uniqueSurvey = _acquireAndSort(eachSurvey, 'index', eachIndex, 'TimeCompleted')
				addToSurveys(uniqueSurvey)
			totalSurveys = totalSurveys + surveys
		self._setSurveys(totalSurveys)

	def scoreSurveys(self):
		addToScoredSurveys = self.scoredSurveys.append
		for survey in self.surveysToScore:
			surveyID = survey['ID'].values[0]
			surveyDate = survey['TimeRequested'].values[0]
			surveyScores = survey['Value']
			createParticipantSurvey = ParticipantSurvey(surveyID, surveyDate, surveyScores.values)
			addToScoredSurveys(createParticipantSurvey)





class ScoringTree: # put entire database here, root to query
	
	
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
	
	def getFlattenedUniqueVals(self, dataframe, destination, column):
		vals = _getUniqueValuesAndFlatten(dataframe, column)
		if destination == 'ids':
			self._setUniqueIDs(vals)
		elif destination == 'dates':
			self._setUniqueDate(vals)

	def getSurveys(self):
		for eachID in self.uniqueIDs:
			subject = Participant(eachID)
			df2 = _acquireAndSort(self.df, 'ID', subject.id, 'TimeCompleted')
			self.getFlattenedUniqueVals(df2, 'dates', 'TimeRequested')
			surveyPerTime = []
			addToSurveyPerTime = surveyPerTime.append
			for eachTime in self.uniqueDate:
				df3 = _acquireAndSort(df2, 'TimeRequested', eachTime,'TimeCompleted')
				addToSurveyPerTime(df3)
			subject.surveys = surveyPerTime
			self.base.append(subject)

#def main():
#	results = []
#	addToResults = results.append
#	tree = ScoringTree('global', 'ID')
#	tree.getSurveys()
#	for surveyParticipant in tree.base:
#		surveyParticipant.populateScores()
#		surveyParticipant.scoreSurveys()
#		for each in surveyParticipant.scoredSurveys:
#			addToResults([each.id, each.scoreGlobalVas(), each.date])
#	return results
#
#if __name__ == "__main__":
#	print main()




