import pandas as pd
import re

filePathToJsonFile = '/Volumes/rubin-lab/FitBit/JSON Files/download.json'

class table:

	def __init__(self, filePath):
		self.path = filePath
		self.parsedTable = None
		self.getAllFrames(filePathToJsonFile)
		self.addFromBruteSearch()

	def openJsonFile(self, path):
	    jsonToParse = open(path).read()
	    return jsonToParse
	
	def parseJson(self, path):
		openedJsonFile = self.openJsonFile(path)
		return pd.read_json(openedJsonFile)
	
	def createDataFrame(self, series):
		return pd.DataFrame.from_dict (series)
	
	def parseDataColumn(self, dataToClean):
		return map(self.createDataFrame, dataToClean)
	
	def concatAndTransposeData(self, fpath):
		dfInit =self.parseJson(filePathToJsonFile).reset_index()['data']
		dataFrame = pd.concat(self.parseDataColumn(dfInit))
		return dataFrame.transpose()
	
	def parseNameSpace(self, regex, testString):
		matches = re.search(regex, testString)
		return (matches.group(1))

	def namespaceBruteSearch(self):
		regexHardList = ['Corporation', 'Study', 'Subject', 'namespace', 'DataPoint']
		dataToClean = self.concatAndTransposeData(filePathToJsonFile).loc[('namespace')]
		cleanedList = []
		addtoCleanedList = cleanedList.append
		i = 0
		while i < 4:
			s1 = regexHardList[i]
			s2 = regexHardList[i+1]
			regexStringFormats = r"(?<={0})(.+)(?=\W{1})".format(s1, s2)
			cleaned = pd.DataFrame([self.parseNameSpace(regexStringFormats, string) for string in dataToClean])
			addtoCleanedList(cleaned)
			i += 1
		return pd.concat(cleanedList, axis = 1)

	def getAllFrames(self, filePathToJsonFile):
		df = self.concatAndTransposeData(filePathToJsonFile)
		indices = df.index.values
		frames = map(pd.DataFrame,[df.loc[x] for x in indices])
		self.parsedTable = pd.concat(frames, axis = 1).reset_index()

	def addFromBruteSearch(self):
		cols = self.namespaceBruteSearch()
		self.parsedTable = pd.concat([self.parsedTable, cols], axis = 1)
	
def main():
	newTable = table(filePathToJsonFile)
	print newTable.parsedTable


if __name__ == '__main__':
	main()




