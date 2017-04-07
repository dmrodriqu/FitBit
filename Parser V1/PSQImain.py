from parser import readableDate, scoreRaw, Psqi
import pandas as pd



class PsqiTable:

    def __init__(self):
        self.psqiTable = None
        self.ids = None
        self.openPsqiTable()
        self.psqiIDs()

    def openPsqiTable(self):
        psqi = pd.HDFStore('psqiTable.h5')
        psqi = psqi['psqiTable']
        self.psqiTable = psqi

    def psqiIDs(self):
        self.ids = self.psqiTable['ID'].unique()

    def psqiParse(self, idToFind):
        # Generate PSQI table from DataFrame
        # Convert Unix to DateTime
        # select from psqi table where id like # idToFind - > continue
        cols = ['PSQIQuestionID', 'Value', 'ID', 'TimeCompleted']
        psqiTable = self.psqiTable
        psqiTable = psqiTable[psqiTable['ID'] == idToFind][cols]
        psqiTable = readableDate(psqiTable)
        idSeries = []
        scoreSeries = []
        dateSeries = []
        for date in psqiTable['TimeCompleted'].unique():
            uniqueDateFrame = psqiTable[psqiTable['TimeCompleted'] == date]
            scaledScoreArray = map(lambda x: x, scoreRaw(uniqueDateFrame))
            newScore = Psqi(scaledScoreArray)
            newScore.scoreall()
            scaledScore = newScore.globalPsqi()
            scoreSeries.append(scaledScore)
            dateSeries.append(date)
            idSeries.append(idToFind)
        psqiDataFrame = {
            'ID': idSeries,
            'Score': scoreSeries,
            'Date': dateSeries}
        psqiFrame = pd.DataFrame(psqiDataFrame)
        return psqiFrame

    #print psqiParse("BLqS60")
     