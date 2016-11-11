import parser
import pandas as pd

def main ():

    fpath = '/Volumes/rubin-lab/UChicagoIBD_data.json'
    # get PSQI scores from all individuals
    # parse Json to DataFrame
    fullDataFrame = parser.parseJsonFile(fpath)
    # Generate PSQI table from DataFrame
    psqiTable = parser.createSurveyTable(fullDataFrame, 'PSQI')
    # Convert Unix to DateTime
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
    while i < len(parser.getUniqueIds(psqiTable)):
        # Find each unique ID
        itemToScore = parser.getUniqueIds(psqiTable)[i]
        ptID = itemToScore['ID'].unique()[0]
        ptTime = itemToScore['TimeCompleted'].unique()[0]
        scoreArray = parser.scoreRaw(itemToScore)
        newScore = parser.Psqi(scoreArray)
        newScore.scoreall()
        idSeries.append(ptID)
        scoreSeries.append(newScore.globalPsqi())
        dateSeries.append(ptTime)
        i += 1

    psqiDataFrame = {
        'ID' : idSeries,
        'Score' : scoreSeries,
        'Date' : dateSeries,}

    return pd.DataFrame(psqiDataFrame)

if __name__ == '__main__':
    print main()