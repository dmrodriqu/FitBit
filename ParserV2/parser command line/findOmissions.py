from parser import Table
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys, getopt

class SubData:

	def __init__ (self, participantID, subsetOfOriginalDataframe):
		self.participantID = participantID
		self.df = subsetOfOriginalDataframe
		self.uniqueSurveys = []
		self.enrollmentDate = []
		self.datesToCompleteSurveys = []
		self.contactPatient = False

	def _getData(self):
		return self.df

	def _setUniqueSurveys(self, values):
		self.uniqueSurveys = values

	def getUniqueSurveys(self):
		return self._setUniqueSurveys(self.df.survey.unique())

	def _getsurveys(self):
		return self.uniqueSurveys

	def _setEnrollmentDate(self, values):
		self.enrollmentDate = values

	def _getEnrollmentDate(self):
		return self.enrollmentDate

	def _setCompletionDates(self, values):
		self.datesToCompleteSurveys = values

	def _getCompletionDates(self):
		return self.datesToCompleteSurveys

	def _setContactPatient(self):
		self.contactPatient = True

	def _getContactPatient(self):
		return self.contactPatient

	def getQuestionDate(self, question, requested = 'requested'):
		if requested == 'requested':
			valuesToSearch = 'timeRequested'
		else:
			valuesToSearch ='timeCompleted'
		self.getUniqueSurveys()
		df = self._getData()
		questionQueries = [df[df.survey == a] for a in [b for b in self._getsurveys() if question in b]]
		questionQueries = [x[valuesToSearch].unique() for x in questionQueries]
		if len(questionQueries) < 1:
			return questionQueries
			#print 'check enrollment date of ID %s' % (self.participantID[0])
		else:
			return(questionQueries)

	def calculateCompletionDates(self):
		dateOfEnrollment = self._getEnrollmentDate()
		#print dateOfEnrollment[0]
		daysToAdd = [1, 16, 31]
		if len(dateOfEnrollment) > 0:
			datetime_object = datetime.strptime(str(dateOfEnrollment[0][0]), '%Y-%m-%d')
			self._setCompletionDates([(datetime_object + timedelta(days=x)) for x in daysToAdd])
		else:
			print 'calculate date of surveys %s' % (self.participantID[0])

	def calculateDateRanges(self):
		datesOfCompletion = self._getCompletionDates()
		addWindow = [(x + timedelta(days=4)) for x in datesOfCompletion]
		return zip(datesOfCompletion, addWindow)

	def findOmissions(self, question):
		dateRanges = self.calculateDateRanges()
		questionCompletionDate = self.getQuestionDate(question, requested = 'completed')
		if len(questionCompletionDate) > 0:
			questionCompletionDate = [datetime.strptime(x, '%Y-%m-%d') for x in questionCompletionDate[0]]
		else:
			pass
		i = 0
		completionDates = []
		completionAfterDates = []
		nonCompletionDates = []
		addToCompletionDates = completionDates.append
		addToCompletionAfterDates = completionAfterDates.append
		addToNonCompletionDates = nonCompletionDates.append
		while i < len(dateRanges):
			try:
				#print dateRanges[i]
				if (dateRanges[i][0] <= questionCompletionDate[i] <= dateRanges[i][1]):
					addToCompletionDates(questionCompletionDate)
					i += 1
				elif (dateRanges[i][1] < questionCompletionDate[i]):
					addToCompletionAfterDates(questionCompletionDate)
					i += 1
					#return ('%s + completed after request date' % (self.participantID))
			except: # questionCompletionDate == []:
				if dateRanges[i+1][0] < datetime.now():
					addToNonCompletionDates(dateRanges[i+1][0])
					self._setContactPatient()
					i += 1
				else:
					pass
				#return ('%s + did not complete' % (self.participantID))
			return ('%s \n completed on following dates: %s \n completed after window on following dates (bug): %s \n and did not complete by %s ' % 
				(self.participantID[0], completionDates , completionAfterDates, nonCompletionDates))

class MainData: # this superclass sets up the main dataframe, another b-tree
	
	def __init__(self): #this py file will be where the json file is downloaded.
		self.df = None
		self.surveyParticipants = [] # we need to find the unique IDs
		self.arrayOfSubsetObjects = [] # set up an array for the subclass here for traversing the tree
		self.patientsToContact = []

	def _setDf(self, value):
		self.df = value

	def _getDf(self):
		return self.df

	def _setSurveyIds(self, value):
		self.surveyParticipants = value

	def _getSurveyIds(self):
		return self.surveyParticipants

	def getSubsetData(self):
		return self.arrayOfSubsetObjects

	def _addPatientToContactList(self, value):
		self.patientsToContact.append(value)

	def _getPatientContactList(self):
		return self.patientsToContact

	def _getJsonPath(self):
		import os
		dir_path = os.path.dirname(os.path.realpath(__file__))
		for file in os.listdir(dir_path):
			if file.endswith(".json"):
				return(os.path.join(dir_path, file))
	
	def _stringCleaning(self, stringToClean): 
		return stringToClean[2:-2]

	def _convertTime(self, unixTime):
		return time.strftime('%Y-%m-%d', time.localtime(unixTime/1000))

	def _newTable(self):
		table = Table(self._getJsonPath())
		#print table.parsedTable.id.unique() # uncomment to debug and see IDs parsed
		col = table.parsedTable.columns
		for x in col[:-3:-1]:
			table.parsedTable[x] = table.parsedTable[x].apply(self._stringCleaning)
		return table.parsedTable

	def _getStartDates(self, table):
		#regex string for Demo, get all dates
		table['value'] = table['value'].astype(int)
		table['timeCompleted'] = table.timeCompleted.apply(self._convertTime)
		table['timeRequested'] = table.timeRequested.apply(self._convertTime)
		return table[['timeRequested','timeCompleted', 'id', 'survey', 'value']]

	def _construct(self):
		self._setDf(self._getStartDates(self._newTable()))
		self._setSurveyIds(self._getDf().id.unique())

	def _getCondition(self, values):
		return values

	def createTraversal(self):
		self._construct()
		data = self.df
		addToSubset = self.arrayOfSubsetObjects.append
		for uniqueID in self.surveyParticipants:
			condition = data.id == uniqueID
			subsetOfOriginalDataframe = data[condition]
			participantID = subsetOfOriginalDataframe.id.unique()
			initializeSubDataClass = SubData(participantID, subsetOfOriginalDataframe)
			addToSubset(initializeSubDataClass)




