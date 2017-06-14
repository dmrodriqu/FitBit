import mergeAndGraph
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.stats import pearsonr
import scipy

class RegressAndPlot:

	def __init__(self, metric):
		self.data = None
		self.regr = linear_model.LinearRegression()
		self.column = metric
		self.x = None
		self.y = None
		self.r = None
		self.createTable()

	def createTable(self):
		new = mergeAndGraph.PsqiVsSleep(self.column)
		self.data = new.getPsqiData()
	
	def getxAndyVals(self, df):
		self.y = df.ix[:, -2:-1].values
		self.x = df.ix[:, -1:].values


	def regression(self):
		x = self.x
		y = self.y
		self.regr.fit(x, y)
		self.r = pearsonr(x, y)[0][0]
		print('Variance score: %.2f' % self.regr.score(x, y))


	def plot(self):
		x = self.x
		y = self.y
		plt.scatter(x, y,  color='black')
		plt.plot(x, self.regr.predict(x), color='blue',
	         linewidth=3)
		plt.ylabel('PSQI Score')
		plt.xlabel('Restless Duration')
		plt.title('PSQI Vs. Restless Duration')
		plt.text(50, 7.5, r'R = {0}'.format(round(self.r,3)))
		plt.show()


new = RegressAndPlot('Efficiency')
new.getxAndyVals(new.data)
#new.regression()
#new.plot()
new2 = RegressAndPlot('RestlessDuration')
newData = new2.data.groupby(['ID', 'Date']).mean()
new2.getxAndyVals(newData)
new2.regression()
new2.plot()