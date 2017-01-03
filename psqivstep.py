## import statements
# import class for PSQI reading
# import class for Step Counting
import stepProcessor
import PSQImain


# goal is to take one ID and to return a graph of PSQI vs Step Count(two week prior)
# testID 'BLqS60'
def returnStepsPerID(ID):
	newSeries = stepProcessor.Timeseries(ID)
	newSeries.stepCountByID()
	print newSeries.Total
	print newSeries.Date

# 

def returnPsqiPerID(ID):
	newFrame = PSQImain.psqiParse(ID)
	return newFrame
returnStepsPerID('BLqS60')
print returnPsqiPerID('BLqS60')