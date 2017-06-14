import openh5

def getData(tableToSearch): # puts df in the scoring tree
	table = openh5.openData(tableToSearch)
	table.formatOpeningQuery()
	table.convertTime()
	return table.df

