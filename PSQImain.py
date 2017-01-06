import parser
import pandas as pd


def psqiParse(idToFind):

    # Generate PSQI table from DataFrame

    psqiTable = pd.HDFStore('psqiTable.h5')
    psqiTable = psqiTable['psqiTable']
    # Convert Unix to DateTime

    # select from psqi table where id like # idToFind - > continue
    psqiTable = psqiTable[psqiTable['ID'] == idToFind][[
        'PSQIQuestionID', 'Value', 'ID', 'TimeCompleted']]
    psqiTable = parser.readableDate(psqiTable)
    # Loop over each ID and Score PSQI
    i = 0
    # create dictionaries for DataFrame:
    # outline of method:
    # for each column:
    # {column name: [array of values]}
    # 3 arrays needed: IDs, scores, Times
    idSeries = []
    scoreSeries = []
    dateSeries = []
    # return map(lambda x: x, parser.scoreRaw(psqi))
    while i < len(parser.getUniqueIds(psqiTable)):
        # Find each unique ID
        itemToScore = parser.getUniqueIds(psqiTable)[i]
        ptID = idToFind
        ptTime = itemToScore['TimeCompleted'].unique()[0]
        scoreArray = parser.scoreRaw(itemToScore)
        newScore = parser.Psqi(scoreArray)
        newScore.scoreall()
        idSeries.append(ptID)
        scoreSeries.append(newScore.globalPsqi())
        dateSeries.append(ptTime)
        i += 1
#
    psqiDataFrame = {
        'ID': idSeries,
        'Score': scoreSeries,
        'Date': dateSeries}
#
    psqiFrame = pd.DataFrame(psqiDataFrame)
    return psqiFrame

# psqiParse("BLqS60")
