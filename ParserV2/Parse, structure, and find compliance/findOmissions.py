from parser import Table
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys, getopt


#additional PSQI class for aggregate scoring

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





class SubData:

	patientsToContact = []

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
					patientsToContact.append(self.participantID)
					i += 1
				else:
					pass
				#return ('%s + did not complete' % (self.participantID))
			return ('%s \n completed on following dates: %s \n completed after window on following dates (bug): %s \n and did not complete by %s \n' % 
				(self.participantID[0], completionDates , completionAfterDates, nonCompletionDates))

	def findLastVAS(self, question, timeInterval):
		convertedIntToTimeDelta = timeDelta(timeInterval)
		vasCompletionDates = self.getQuestionDate(question, requested = 'completed')
		if datetime.now - vasCompletionDates[:-1] > convertedIntToTimeDelta:
			patientsToContact.append(self.participantID)
		else:
			pass

	def findVASOmissions(self, question):
		listOfIdsToContact = []
		datesCompleted = []
		completionDates = []
		deltaDates = []
		addToDeltaDates = deltaDates.append
		addToCompletionDates = completionDates.append
		addTolistOfIdsToContact = listOfIdsToContact.append
		questionCompletionDate = self.getQuestionDate(question, requested = 'completed')
		if len(questionCompletionDate) > 0:
			questionCompletionDate = [datetime.strptime(x, '%Y-%m-%d') for x in questionCompletionDate[0]]
			addToCompletionDates(questionCompletionDate)
		differenceInDates = [x - questionCompletionDate[i - 1] for i, x in enumerate(questionCompletionDate)][1:]
		i = 0
		while i < len(differenceInDates):
			if differenceInDates[i] > timedelta(days = 3):
				addToDeltaDates(completionDates[0][i+1])
			else:
				pass
			i += 1
		try:
			if (datetime.now() - completionDates[0][-1]) >= timedelta(days = 2):
				return ('\n {0} \n last completion dates: {1} \n CONTACT PATIENT \n'.format (self.participantID[0], deltaDates))
			if (datetime.now() - completionDates[0][-1]) < timedelta(days = 2):
				return ('\n {0} \n last completion dates: {1} \n'.format (self.participantID[0], deltaDates))
		except:
			pass

	def getSurveySeries(self, surveyType):
		data = self.df
		data = data[data['survey'].str.contains(surveyType)]
		uniqueSurveys = data['timeRequested'].unique()
		surveys = []
		addToSurveys = surveys.append
		for survey in uniqueSurveys:
			addToSurveys(data[data['timeRequested']==survey])
		self.uniqueSurveys = surveys


	def scorePSQI(self, surveyToScore):
		if len(surveyToScore) < 17:
			pass
		else:
			i = 0
			qvals = []
			questionValueArray = surveyToScore['value'].values
			while i < 17:
				questionValues = questionValueArray[i]
				if 4 <= i < 17:
					qvals.append(questionValues - 1)
				if i == 1:
					valfor2 = (questionValues - 1)
					if valfor2 > 3:
						valfor2 = 3
						qvals.append(valfor2)
				if i == 3:
					qvals.append(questionValues + 1)
				if i == 0:
					if questionValues == 1:
						qvals.append(20.0)
					if questionValues == 2:
						qvals.append(20.5)
					if questionValues == 3:
						qvals.append(21.5)
					if questionValues == 4:
						qvals.append(22.5)
					if questionValues == 5:
						qvals.append(23.5)
					if questionValues == 6:
						qvals.append(0.5)
					if questionValues == 7:
						qvals.append(1.0)
				i += 1
			scores = Psqi(qvals)
			try:
				scores.scoreall()
				scores.globalPsqi()
				return scores.score
			except:
				pass


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

def main():

	data = MainData()
	data.createTraversal()
	for subject in data.getSubsetData():
		subject.getUniqueSurveys()
		print subject.participantID
		subject.getSurveySeries('PSQI')
		print map (subject.scorePSQI, subject.uniqueSurveys)

if __name__ == '__main__':
	main()


