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
		self.patientID = None
		#self.sleepPlaceholder = None
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
	
	#def initSleepClass(self):
	#	init sleepFrame Class
	#	self.sleepPlaceholder = sleepFrame()
	#	self.sleepPlaceholder.construct()


	#def getUniqueDateForID(self):
	#	for each ID in 
	#	self.initSleepClass()
	#	return self.sleepPlaceholder.uniqueID

	# only append one, use functions outside of class to add
	# information to data structure 

	def getEdgeTimes(self, sleepTimes):

		# get time of today
		today = Delorean(datetime = self.dateOfSleep)
		
		def getZeroHour(today):
			midnight = epoch(today).midnight
			d = Delorean(datetime = midnight)
			return d.epoch
		
		def getEndHour(today):
			tomorrowmid = epoch(today).next_day().midnight
			d = Delorean(datetime = tomorrowmid)
			return d.epoch
		
		return getZeroHour(),getEndHour()

		def preAppendTimes(today):
			preAppendArray = []
			AppendArray = []
			secAtMidnight = getZeroHour(today)
			secAtTomorrowMidnight = getEndHour(today)
			secondsFromMidnight = time - secAtMidnight
			secondsToMidnight = secAtTomorrowMidnight- time 
			secondsToPrepend = range(secondsFromMidnight - 1)
			secondsToAppend = range(secondsToAppend - 1)
			for num in secondsToPrepend:
				addToPreArr = today+num
				preAppendArray.append(addToPreArr)
			for num in secondsToAppend:
				addToAppendArray = today+num
				AppendArray.append(addToAppendArray)
			return preAppendArray, AppendArray

		def concatenationOfSuppTimes(sleepTimes):
			sleepTimes = map(lambda x : ast.literal_eval(x))
			sleepValues = []
			SleepKeys = []
			supplimentTimes = preAppendTimes()
			preArr = supplimentTimes[0]
			postArr = supplimentTimes[1]
			for x in preArr:
				sleepValues.append(0)
			for x in sleepTimes:
				sleepValues.append(x.values)
				SleepKeys.append(x.keys)
			for x in postArr:
				sleepValues.append(0)
			totalSleepArray = preArr + sleepTimes + postArr
			return sleepValues, totalSleepArray
			# get values of original, convert to arr,


		




