from parser import Table
import time
import pandas as pd
fpath = '/Volumes/rubin-lab/FitBit/JSON Files/3lbQgJIF.json'


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

df = newTable(fpath)
start =  getStartDates(df)
start = start.reset_index()
idList = start.id.unique()
print idList
surveyItems = [u'ImageChoiceDemo', u'PSQI/Q10', u'SIBDQ/Q10',
 u'SleepQualityVAS', u'SliderDemo', u'SubjectGlobalAssessmentVAS',
 u'SurveyDemo/Q1', u'SurveyDemo/Q2', u'WongBaker']
print surveyItems
def abstractedCompleteRequest(df, timepoint = 'timeCompleted'):
	i = 0
	while i < len(df.id.unique()):
		yield df.pivot_table(index = 'id', columns = ['survey', timepoint], values = 'value').ix[i:i+1]#dropna(axis = 1)
		i += 1

def transform(gen):
	return pd.DataFrame(gen.iloc[0]).reset_index()

def output(df):
	i = 0 
	a = [x for x in abstractedCompleteRequest(df)] # yield these
	#b = [x for x in abstractedCompleteRequest(df, timepoint = 'timeRequested')]
	while i < len(a):
		#c = transform(b[i]).dropna() # into these
		d = transform(a[i]).dropna()
		#print c
		#print d
		yield d
		#yield c.merge(d).drop_duplicates().dropna()
		i +=1
results = [x for x in output(start)]
#print results

for questions in surveyItems:
	i = 0
	concatenatedResponses = None
	responsesToConcat = []
	addToResponse = responsesToConcat.append
	while i < len(results):
		cond = results[i].survey == questions
		responses = results[i][cond]
		if len(responses) > 0:
			addToResponse(responses)
		concatenatedResponses = pd.concat(responsesToConcat)
		i +=1
	name = concatenatedResponses.survey.unique()
	concatenatedResponses.to_csv(str(name[0][0:4])+'.csv')
	#print concatenatedResponses[concatenatedResponses.timeRequested < concatenatedResponses.timeCompleted]

#[x.to_csv(str(x.columns[2])+".csv") for x in output(start)]


