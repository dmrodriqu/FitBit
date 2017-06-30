import time
from parser import Table
from os import listdir
from os.path import isfile, join

def getFiles(path):
	return [f for f in listdir(path) if isfile(join(path, f))]

def main():
	truncPath = '/Volumes/rubin-lab/FitBit/ParserV2'
	fpath = '/Volumes/rubin-lab/FitBit/JSON Files/download.json'
	newTable = Table(fpath)
	curDate = time.strftime("%d%m%Y")
	filesPresent = 'rawData{0}.csv'.format(curDate)
	if filesPresent not in getFiles(truncPath):
		return newTable.parsedTable.to_csv(filesPresent)
	else:
		print 'WARNING: This file already exists!' 
	


if __name__ == '__main__':
	main()
