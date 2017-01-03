import pandas as pd
import numpy as np


#data = pd.read_csv('stepFrame.csv')

class stepFrame:

	def __init__(self, dataToRead):
		self.frame = None 
		self.uniqueID = None
		self.readFrame(dataToRead)
		self.findUniqueID()

	def readFrame(self, dataToRead):
		data = pd.read_csv(dataToRead)
		self.frame = data[['ID','Timeseries', 'Date', 'Total']]

	def findUniqueID(self):
		data = self.frame
		self.uniqueID = data['ID'].unique()


class Timeseries:

	def __init__(self, ID):
		self.Timeseries = None
		self.Total = None
		self.Date = None
		self.ID = ID

	def stepCountByID(self):
		#test ID 'BLqS60'
		queryID = self.ID
		new = stepFrame('stepFrame.csv')
		graphlist = []
		#print new.frame['ID']
		for eachID in new.frame[new.frame['ID'] == queryID]:
			#newGraph = Timeseries()
			self.Timeseries = new.frame['Timeseries'].values
			#self.ID = new.frame['ID'].values
			self.Date = new.frame['Date'].values
			self.Total = new.frame['Total'].values
			#graphlist.append(newGraph)

		#timeseries[0,1,2,3...n]- 1:1 with  date
		#date[0,1,2,3...n]-------1:1 with timeseries
		#id[0,1,2,3...n]
	
		#return graphlist[0].Total

