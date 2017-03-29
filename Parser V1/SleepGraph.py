import pandas as pd
import matplotlib.pyplot as plt
import parser
import ast
import matplotlib
matplotlib.style.use('ggplot')

# to add
# comparison along uniform timeframe:

# Create a class for each graph
# create a 24 hour time frame from 0000 to 2359 as an array with 2400 values
# insert values
#

sleepFrame = pd.read_csv('sleepFrame')
dataToPlot = sleepFrame[sleepFrame['ID'] == 'BLqS60']
sleepDates = dataToPlot['DateOfSleep'].unique()

for date in sleepDates:
	dataForPlot = dataToPlot[dataToPlot['DateOfSleep'] == date]
	seriesToPlot = dataForPlot['MinuteData']
#print dataToPlot
# string representation of dictionary
# evaluate as literal to get dictionary from string
	recreateDictionaries = seriesToPlot.apply(ast.literal_eval)
# create columns for plotting
	timeSeries = recreateDictionaries.apply(pd.Series)
#print timeSeries

	timeSeries.plot.bar(x= 'Timestamp' , y ='Value')
	plt.show()