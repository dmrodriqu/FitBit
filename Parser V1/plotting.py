import surveyScoringTree
import pandas as pd 
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from sklearn import preprocessing
import numpy as np
import seaborn as sns
sns.set(color_codes=True)

def acquireAndSort(dataframe, cond, columnToSort):
	return dataframe[cond].sort_values(columnToSort)

class ParticipantSurveys:

	def __init__(self, survey, surveyDate):
		self.df = survey
		self.date = surveyDate
		self.aggregate = []

	def _setAggreagate(self, vals):
		self.aggregate = vals

	def summary(self):
		self._setAggreagate([self.df['1_x'].mean(), 
			self.df['1_y'].mean(), self.df['2_y'].values[0]])

class pairwiseSurveyParticipant:

	def __init__(self, id, df):
		self.surveyPairs = df
		self.id = id
		self.surveys = []

	def _uniqueMatchedDates(self):
		return self.surveyPairs['2_y'].unique()

	def createSurveys(self):
		addToSurveys = self.surveys.append
		for dt in self._uniqueMatchedDates():
			ps = self.surveyPairs[self.surveyPairs['2_y'] == dt]
			addToSurveys(ParticipantSurveys(ps, dt))

class PairwiseSurveys:

	def __init__(self, data1, data2):
		self.df = None 
		self.surveyParticipants = []
		self.mergeData(data1, data2)

	def _setDataFrame(self, vals):
		self.df = vals

	def _getScores(self, table):
		results = []
		addToResults = results.append
		tree = surveyScoringTree.ScoringTree(table, 'ID')
		tree.getSurveys()
		for surveyParticipant in tree.base:
			surveyParticipant.populateScores()
			surveyParticipant.scoreSurveys()
			for each in surveyParticipant.scoredSurveys:
				if table == 'global':
					addToResults([each.id, each.scoreGlobalVas(), each.date])
				elif table == 'sibdq':
					addToResults([each.id, each.scoreSIBDQ(), each.date])
				elif table == 'psqi':
					addToResults([each.id, each.scorePSQI(), each.date])
		return results

	def _createDataframe(self,dataFromScores):
		return pd.DataFrame(self._getScores(dataFromScores))

	def _convertToDateTime(self, strDateTime):
		return pd.to_datetime((strDateTime[2]))

	def mergeData(self, data1, data2):
		datalist = [data1, data2]
		datalist = map(self._createDataframe, datalist)
		for each in datalist:
			each[2] = self._convertToDateTime(each)
		merged = datalist[0].merge(datalist[1], on = 0)
		self._setDataFrame(merged[(merged['2_y'] <= merged['2_x'] + datetime.timedelta(days=14)) & 
		(merged['2_y'] >= merged['2_x'])]) 

	def createPairwiseParticipants(self):
		ids = self.df[0].unique()
		cond = ((self.df['2_y'] <= self.df['2_x'] + datetime.timedelta(days=14)) & 
			(self.df['2_y'] >= self.df['2_x']))
		addToSurveyParticipants = self.surveyParticipants.append
		for x in ids:
			tempdf = self.df[self.df[0] == x]
			addToSurveyParticipants(pairwiseSurveyParticipant(x, tempdf))

def createPlot(df1, df2):
	dfAlias1xAxis = df1
	dfAlias2yAxis = df2
	surveys = PairwiseSurveys(dfAlias2yAxis, dfAlias1xAxis)
	surveys.createPairwiseParticipants()
	newFrame = []
	filterarr = ['2tcXat', 'GJbIM0', 'gRqhgp']
	addTonewFrame = newFrame.append
	for each in surveys.surveyParticipants: 
		if each.id not in filterarr:
			each.createSurveys()
	for each in surveys.surveyParticipants:
		print each.id
		for ob in each.surveys:
			ob.summary()
			print ob.aggregate
			addTonewFrame(ob.aggregate)
	results = pd.DataFrame(newFrame)
	print results
	results.rename(columns={0: dfAlias2yAxis , 1 : dfAlias1xAxis, 2: 'Date'}, inplace=True)
	sns.jointplot(x=dfAlias1xAxis, y=dfAlias2yAxis, data=results, ci= False, kind = 'reg', robust=True ) # yes, the axes look reversed, aggregates data
	plt.show()

#createPlot('psqi', 'sibdq')
#createPlot('psqi', 'global')
#createPlot('sibdq', 'global')

def findTimes():
	surveys.createPairwiseParticipants()


