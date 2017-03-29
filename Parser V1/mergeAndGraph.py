import pandas as pd
import parser
from datetime import timedelta
import PSQImain
import matplotlib.pyplot as plt

psqiFrame = PSQImain.psqiParse()
sleepFrame = pd.read_csv('sleepFrame.csv')


def merger(x, y):
	mergedTables = pd.merge(x, y, on = 'ID')
	drops = parser.idsToDrop()
	mergedTables = mergedTables[~mergedTables['ID'].isin(drops)]
	return mergedTables

mergedframe = merger(psqiFrame, sleepFrame)

#procedural non abstraction....
# later abstract to nC2

#parser.readableDate(mergedframe)
#mergedframe = mergedframe[mergedframe['DateOfSleep'] == mergedframe['TimeCompleted']]
#print mergedframe
mergedframe['Date'] = pd.to_datetime(mergedframe['Date'], infer_datetime_format=True)
mergedframe['DateOfSleep'] = pd.to_datetime(mergedframe['DateOfSleep'], infer_datetime_format=True)
#dateMask = (mergedframe['DateOfSleep'] > mergedframe['TimeCompleted'] - timedelta(days=14)) & (mergedframe['DateOfSleep'] < mergedframe['TimeCompleted'])
dateMask = (mergedframe['DateOfSleep'] == mergedframe['Date'])


#'Date','ID','Score','Efficiency', 'MinutesAsleep', 'RestlessDuration', 'RestlessCount', 'MinutesAwake', 'MinutesToFallAsleep'
mergedframe = mergedframe[['Date','ID','Score','Efficiency']].loc[dateMask].drop_duplicates()
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


