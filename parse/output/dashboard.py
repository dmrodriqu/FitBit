from findOmissions import MainData
import pandas as pd
import datetime

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

	def insertDateGaps(self, dates):
		for k, v in dates.iteritems():
			i = 0
			while i < len(v) - 1:
				print v
				try:
					dateDiff = datetime.datetime.strptime(v[i+1][0] , "%Y-%m-%d") - datetime.datetime.strptime(v[i][0], "%Y-%m-%d")
					print dateDiff
				except:
					i+=1
				if dateDiff > datetime.timedelta(days = 1):
					repeat = 0
					while repeat < int(dateDiff.days - 1):
						v.insert(i+1, 'SKIPPED')
						repeat += 1
					i += int(dateDiff.days) 
				else:
					i+=1
		return dates
	
	def output(self, date = True, values = False):
		a =  pd.DataFrame.from_dict(self.Values, orient = 'index')
		b = pd.DataFrame.from_dict(self.insertDateGaps(self.Dates),  orient = 'index')
		print b

		if values:
			return a.to_csv('{}.csv'.format(self.survey))
		else: 
			return b.to_csv('{}.csv')
		

#usage 
result = Results('WongBaker')
print result.output(values = False)
