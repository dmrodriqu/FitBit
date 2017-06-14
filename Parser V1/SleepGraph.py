import pandas as pd
import matplotlib.pyplot as plt
import parser
import ast
import matplotlib
import unisleep
matplotlib.style.use('ggplot')

def sleepGraph():
	sleepData = unisleep.sleepFrame()
	sleepData.construct()
	idArray = sleepData.uniqueID
	constructors = []
	for idInArray in idArray:
		iSleep = unisleep.UniSleep()
		iSleep.patientID = idInArray
		idToIndex = idInArray
		# storing class var in function var
		data = sleepData.frame
		# selecting dataframe for only ID we want
		dataToIndex = data[data['ID'] == idToIndex]
		sleepDates = dataToIndex['DateOfSleep'].unique()
		# selecting dates specific to ID
		datearr = []
		timearr = []
		for date in sleepDates:
			# set date
			# set minute data
			# date1, date2, date3....dateN
			# minutedata1, minutedata2, minutedata3...minutedataN
			datearr.append(date)
			dataForPlot = dataToIndex[dataToIndex['DateOfSleep'] == date]
			seriesToPlot = dataForPlot['MinuteData'].values
			timearr.append(seriesToPlot)
		iSleep.dateOfSleep.append(datearr)
		iSleep.reportedsleep.append(timearr)
		constructors.append(iSleep)
	return constructors
#print sleepGraph()

def main():
	conarray = sleepGraph()
	patientID = []
	sleepDate = []
	sleeptimeseries = []
	for each in conarray:
		print each.patientID
		print each.dateOfSleep[0][0]
		return each.reportedsleep[0][0]

#	# to add
#	# comparison along uniform timeframe:
#	
#	# Create a class for each graph
#	# create a 24 hour time frame from 0000 to 2359 as an array with 2400 values
#	# insert values
#	#
#	
#	sleepFrame = pd.read_csv('sleepFrame')
#	dataToPlot = sleepFrame[sleepFrame['ID'] == 'BLqS60']
#	sleepDates = dataToPlot['DateOfSleep'].unique()
#	
#	for date in sleepDates:
#		dataForPlot = dataToP.lot[dataToPlot['DateOfSleep'] == date]
#		seriesToPlot = dataForPlot['MinuteData']
#	#print dataToPlot
#	# string representation of dictionary
#	# evaluate as literal to get dictionary from string
#		recreateDictionaries = seriesToPlot.apply(ast.literal_eval)
#	# create columns for plotting
#		timeSeries = recreateDictionaries.apply(pd.Series)
#	#print timeSeries
#	
#		timeSeries.plot.bar(x= 'Timestamp' , y ='Value')
#		plt.show()

if __name__ is "__main__":
	print main()