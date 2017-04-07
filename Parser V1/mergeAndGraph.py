import pandas as pd
import parser
import PSQImain

class PsqiVsSleep:

	def __init__(self):
		self.psqiOB = PSQImain.PsqiTable()
		self.sleep = None
		self.SharedIds = None #compare superclass ID functions
		self.openSleepFrame()

	def getPsqiIds(self):
		return self.psqiOB.ids

	def result(self, df):
		return self.dropDuplicateDates(self.merger(result, self.sleep))

	def getPsqiData(self):
		listOfIds = self.getPsqiIds()
		dfList = []
		addToDflist = dfList.append
		for each in listOfIds:
			singleIDPsqi = self.psqiOB.psqiParse(each)
			addToDflist(self.dropDuplicateDates(self.merger(singleIDPsqi, self.sleep)))
		return pd.concat(dfList)

	def openSleepFrame(self):
		sleepFrame = pd.HDFStore('sleepFrame.h5')
		self.sleep = sleepFrame['sleepFrame']
	
	def merger(self, x, y):
		mergedTables = pd.merge(x, y, on = 'ID')
		drops = parser.idsToDrop()
		mergedTables = mergedTables[~mergedTables['ID'].isin(drops)]
		return mergedTables
	
	def convertToDatetime(self, df, col):
		df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
		return df[col]
	
	def maskDates(self, mask1, mask2):
		datemask = (mask1 == mask2)
		return datemask
	
	def dropDuplicateDates(self, mergedDf):
		df = mergedDf
		datemask1 = self.convertToDatetime(df, 'DateOfSleep')
		datemask2 = self.convertToDatetime(df, 'Date')
		mask = (datemask1 == datemask2)
		return mergedDf[['Date','ID','Score','Efficiency']].loc[mask].drop_duplicates()


	
#print dropDuplicateDates(merger(psqiFrame, sleepFrame))

'''
psqiInstances=mergedframe['ID'].value_counts().reset_index()
psqiInstances1 = psqiInstances[psqiInstances['ID'] == 1]['index'].values
mergedframe = mergedframe[~mergedframe['ID'].isin(psqiInstances1)]
print mergedframe
groups = mergedframe.groupby(['ID'])
# plot
fig, ax = plt.subplots()
ax.margins(0.05)
for name, group in groups:
	ax.plot(group.Score, group.Efficiency, marker= 'o', linestyle = '', ms=12, label=name)
ax.set_title('Fitbit Defined Sleep Efficiency vs Calculated PSQI Score')
ax.set_xlabel('PSQI Score')
ax.set_ylabel('Sleep Efficiency')
plt.show()

#mergedframe[['ID', 'Date', 'Score']]
'''

# find all IDs in dataframes, pd.append, then get R for linear reg