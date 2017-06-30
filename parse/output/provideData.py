from findOmissions import MainData
import pandas as pd

class Results:

	def __init__(self, stringOfSurvey):
		self.IDs = []
		self.Dates = None
		self.Values = None
		self.survey = stringOfSurvey
		self._getData()


	def _getData(self):
		data = MainData()
		data.createTraversal()
		idsurvey = []
		surveyDates = {}
		surveyValues = {}
		for subject in data.getSubsetData():
			identifier = subject.participantID[0] #prints an ID for the current participant
			identifier = str(identifier)
			idsurvey.append(identifier)
			subject.getSurveySeries(self.survey)
			listofVals = []
			listofDate = []
			if len(subject.uniqueSurveys) > 0:
				i = 0
				while i < len(subject.uniqueSurveys):
					date = subject.uniqueSurveys[i]['timeCompleted'].drop_duplicates().values
					values = subject.uniqueSurveys[i]['value'].values
					listofDate.append(date)
					listofVals.append(values)
					i+=1
			else:
				surveyDates.update({identifier:None})
				surveyValues.update({identifier:None})
			surveyDates.update({identifier:listofDate})
			surveyValues.update({identifier:listofVals})
		self.Dates = surveyDates
		self.Values = surveyValues

	
	def output(self, date = True, values = False):
		a =  pd.DataFrame.from_dict(self.Values, orient = 'index')
		b = pd.DataFrame.from_dict(self.Dates,  orient = 'index')
		if values:
			return a
		else: 
			return b
		


result = Results('PSQI')
print result.output()
