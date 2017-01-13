from parser import readableDate, scoreRaw, Psqi
import pandas as pd


def psqiParse(idToFind):
    # Generate PSQI table from DataFrame
    psqiTable = pd.HDFStore('psqiTable.h5')
    psqiTable = psqiTable['psqiTable']
    # Convert Unix to DateTime
    # select from psqi table where id like # idToFind - > continue
    cols = ['PSQIQuestionID', 'Value', 'ID', 'TimeCompleted']
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
    
#psqiParse("BLqS60")
