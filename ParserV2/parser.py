import pandas as pd
import re


class Table:

	def __init__(self, filePath):
		self.path = filePath
		self.parsedTable = None
		self.getAllFrames()
		self.addFromBruteSearch()
		self.renameCol()

	def openJsonFile(self):
	    jsonToParse = open(self.path).read()
	    return jsonToParse
	
	def parseJson(self):
		openedJsonFile = self.openJsonFile()
		return pd.read_json(openedJsonFile)
	
	def createDataFrame(self, series):
		return pd.DataFrame.from_dict (series)
	
	def parseDataColumn(self, dataToClean):
		return map(self.createDataFrame, dataToClean)
	
	def concatAndTransposeData(self):
		dfInit =self.parseJson().reset_index()['data']
		dataFrame = pd.concat(self.parseDataColumn(dfInit))
		return dataFrame.transpose()
	
	def parseNameSpace(self, regex, testString):
		matches = re.search(regex, testString)
		return (matches.group(1))

	def namespaceBruteSearch(self):
		regexHardList = ['Corporation', 'Study', 'Subject', 'namespace', 'DataPoint']
		dataToClean = self.concatAndTransposeData().loc[('namespace')]
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

	def getAllFrames(self):
		df = self.concatAndTransposeData()
		indices = df.index.values
		frames = map(pd.DataFrame,[df.loc[x] for x in indices])
		self.parsedTable = pd.concat(frames, axis = 1).reset_index()

	def addFromBruteSearch(self):
		cols = self.namespaceBruteSearch()
		self.parsedTable = pd.concat([self.parsedTable, cols], axis = 1)
	
	def renameCol(self):
		self.parsedTable.columns = ['index', 'namespace',
		 'timeCompleted', 'timeRequested',
		  'value', 'corp', 'study', 'id', 'survey']
	




