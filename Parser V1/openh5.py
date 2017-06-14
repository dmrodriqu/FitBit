import os
import pandas as pd

class openData:
	
	def __init__(self, tableToOpen):
		self.df = None
		self.search = tableToOpen

	def _determineDataFiles(self):
		files = [f for f in os.listdir('.') if os.path.isfile(f) and '.h5' in f]
		return files
	
	def findfile(self, searchFile):
		i = 0
		while i < len(self._determineDataFiles()):
			comparison = self._determineDataFiles()[i]
			if searchFile in comparison:
				return comparison
			i += 1
	
	def formatOpeningQuery(self):
		file = self.findfile(self.search)
		psqi = pd.HDFStore(file)
		psqi = psqi[file[:-3]]
		self.df = psqi