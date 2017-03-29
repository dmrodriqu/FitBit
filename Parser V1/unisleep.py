import pandas as pd
import matplotlib.pyplot as plt
import parser
import ast
import matplotlib
from datetime import datetime
from delorean import epoch
from delorean import Delorean

matplotlib.style.use('ggplot')

# the object here is to create two classes:

# the first is to organize all sleep data into one class:
# -- sleep data frame
# -- unique IDs
# -- Unique Dates

# the second class is to create a class to provide a data structure
# for graphing. The data structure will provide the following:
# -- the previous class to derive the following data for each individual
# -- A pre structured 24 hour array in increments of one minute (24*60)
# -- The array for which an individual sleeps incremented by one minute intervals
# -- The date of sleep
# -- ID
# -- Values will be replaced at times that an individuals sleep, creating a standardized
# -- timeline.

# create class to store all data. don't keep referencing csv...
class sleepFrame:

	def __init__(self):
		self.frame = None 
		self.uniqueID = None
		self.sleepDates = None

	def readFrame(self):
		data = pd.read_csv('sleepFrame.csv')
		self.frame = data[['ID','MinuteData', 'DateOfSleep']]

	def findUniqueID(self):
		data = self.frame
		self.uniqueID = data['ID'].unique()

	def construct(self):
		self.readFrame()
		self.findUniqueID()


class UniSleep(): 

	def __init__ (self):
		# 24 hours * 60 minutes per hour -> gives prestruct array
		self.sleeparr = range(24*60)
		# get actual sleep structures for unique sleep
		self.reportedsleep = []
		# date of slep
		self.dateOfSleep = []
		self.sleepPlaceholder = None
		#placeholder holds sleepclass


	# call new instance of sleepFrame Class

	def instSleep(self):
		new = sleepFrame()
		# we now have a dedicated sleep dataframe
		new.readFrame()
		# with uniqueIDs
		new.findUniqueID()
		# finding unique dates per ID
		new.sleepDates()

	# for each ID, get the unique dates for that ID
	
	def initSleepClass(self):
		# init sleepFrame Class
		self.sleepPlaceholder = sleepFrame()
		self.sleepPlaceholder.construct()


	def getUniqueDateForID(self):
		# for each ID in 
		self.initSleepClass()
		return self.sleepPlaceholder.uniqueID

	# only append one, use functions outside of class to add
	# information to data structure 
	
	def getDataByID(self):
		# getting ID from expressed variable
		idArray = []
		for each in self.sleepPlaceholder.uniqueID:
			idArray.append(each)
		# on^2
		for idInArray in idArray:
			idToIndex = idInArray
			# storing class var in function var
			data = self.sleepPlaceholder.frame
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
			self.dateOfSleep.append(datearr)
			self.reportedsleep.append(timearr)
		
	def getZeroHour(self):
		today = 1467336420
		midnight = epoch(today).midnight
		d = Delorean(datetime = midnight)
		print d.epoch

	def getEndHour(self):
		today = 1467336420
		tomorrowmid = epoch(today).next_day().midnight
		d = Delorean(datetime = tomorrowmid)
		print d.epoch
		


new = UniSleep()
print new.getUniqueDateForID()
new.getDataByID()
print new.dateOfSleep[0]
print new.reportedsleep[0][0]
print new.getZeroHour()
print new.getEndHour()

# for tomorrow, get unique IDs, 
# for ID in list of Unique IDs, get data[data['id'] == 'id' ][minutedata]
# however, need to index id to equivalent


