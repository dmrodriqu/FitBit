import surveyScoringTree
import pandas as pd

def results(data):
	results = []
	filterArr = ['2tcXat', 'GJbIM0', 'gRqhgp']
	addToResults = results.append
	tree = surveyScoringTree.ScoringTree(data, 'ID')
	tree.getSurveys()
	for surveyParticipant in tree.base:
		if surveyParticipant.id not in filterArr:
			surveyParticipant.populateScores()
			surveyParticipant.scoreSurveys()
			for each in surveyParticipant.scoredSurveys:
				if data == 'psqi':
					addToResults([each.id, each.scorePSQI(), each.date])
				elif data == 'sibdq':
					addToResults([each.id, each.scoreSIBDQ(), each.date])
				else:
					addToResults([each.id, each.scoreGlobalVas(), each.date])
	output = pd.DataFrame(results)
	describe = output[1].describe()
	print output
	if data == 'psqi':
		count = output[output[1] > 5][1].count()
		return describe ,count
	else:
		return describe

print results('sibdq')