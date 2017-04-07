import mergeAndGraph
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.stats import pearsonr
import scipy

class RegressAndPlot:

	def __init__(self):
		self.data = None
		self.regr = linear_model.LinearRegression()
		self.x = None
		self.y = None
		self.r = None
		self.createTable()
		self.getxAndyVals()

	def createTable(self):
		new = mergeAndGraph.PsqiVsSleep()
		self.data = new.getPsqiData()
	
	def getxAndyVals(self):
		self.y = self.data.ix[:, -2:-1].values
		self.x = self.data.ix[:, -1:].values


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
		plt.xlabel('Sleep Efficiency')
		plt.title('PSQI Vs. Sleep Efficiency')
		plt.text(88, 7.5, r'R = {0}'.format(round(self.r,3)))
		plt.show()


new = RegressAndPlot()
new.regression()
new.plot()
