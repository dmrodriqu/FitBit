import pandas as pd
import parser 


#parsing data storing as csv
def main():


	fpath = '/Volumes/rubin-lab/UChicagoIBD_data.json'

	fullDataFrame = parser.parseJsonFile(fpath)

	psqiTable = parser.createSurveyTable(fullDataFrame, 'PSQI')
	
	sibdqTable = parser.createSurveyTable(fullDataFrame, 'SIBDQ')
	sibdqTable['TimeCompleted'] = map(lambda x: parser.convertToDate(x) , sibdqTable['TimeCompleted'])
	#print psqiTable[['index','ID']].drop_duplicates()
	
	steps = parser.Table()
	stepSeries = steps.recursiveRows(fullDataFrame, 'Fitbit', 'Steps')
	stepFrame = steps.createStepOrHeartColumns(fullDataFrame, stepSeries)
	
	sleep = parser.Table()
	sleepSeries = sleep.recursiveRows(fullDataFrame, 'Fitbit', 'Sleep')
	sleepFrame = sleep.createSleepColumns(fullDataFrame, sleepSeries)
	sleepFrame.to_csv('sleepFrame')

	#print sleepFrame[sleepFrame['ID'] == 'vB4y2r']
	
	heart = parser.Table()
	heartSeries = heart.recursiveRows(fullDataFrame, 'Fitbit', 'Heart')
	heartFrame = heart.createStepOrHeartColumns(fullDataFrame, heartSeries)


	Vas = parser.Table()
	globalVas = Vas.recursiveRows(fullDataFrame,'Litmus', "UChicagoIBD/SubjectGlobalAssessmentVAS")
	globalVasFrame = Vas.createStepOrHeartColumns(fullDataFrame, globalVas)
	globalVasFrame = parser.readableDate(globalVasFrame)

	globalVasFrame.to_csv('globalVas.csv')
	psqiTable.to_csv('psqiTable.csv')
	sibdqTable.to_csv('sibdqTable.csv')
	stepFrame.to_csv('stepFrame.csv')
	sleepFrame.to_csv('sleepFrame.csv')
 	heartFrame.to_csv('heartFrame.csv')
	
if __name__ == '__main__':
	main()
#print sibdqTable[sibdqTable['ID']== 'vZoyyc']