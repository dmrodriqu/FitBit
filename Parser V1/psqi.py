import parser
import pandas as pd
import matplotlib.pyplot as plt
def main ():

    fpath = '/Volumes/rubin-lab/FitBit/psqiTable.csv'
    # get PSQI scores from all individuals
    # parse Json to DataFrame
    # Generate PSQI table from DataFrame
    psqiTable = pd.read_csv(fpath)
    # Convert Unix to DateTime
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
    #print parser.getUniqueIds(psqiTable)
    #while i < len(psqiTable.ID.unique()):
    # while i is less than the length of the number of unique IDs present
    while i < len(psqiTable.ID.unique()):
        # ID to score in array indexed with i
        # psqiTable.ID.unique() = [id1, id2, id3... idN]
        # itemToScore = ID[i] where += 1 over loop
        itemToScore = psqiTable.ID.unique()[i]
        # ptID = IDn
        ptID = itemToScore
        # time from frame where same as the ID ix. take only unique vals.
        ptTime = psqiTable[psqiTable['ID'] == itemToScore]['TimeCompleted'].unique()[0]
        # rawscore(ID) ->  values
        testing = psqiTable[psqiTable['ID'] == itemToScore]
        scoreArray = parser.scoreRaw(psqiTable[psqiTable['ID'] == itemToScore])
        newScore = parser.Psqi(scoreArray)
        newScore.scoreall()
        idSeries.append(ptID)
        scoreSeries.append(newScore.globalPsqi())
        dateSeries.append(ptTime)
        i += 1

    psqiDataFrame = {
        'ID' : idSeries,
        'Score' : scoreSeries,
        'Date' : dateSeries}

    psqiFrame = pd.DataFrame(psqiDataFrame)
    psqiFrame['Date'] = map(lambda x: parser.convertToDate(x), psqiFrame['Date'])
    vasTable = pd.read_csv('globalVas.csv')
    vasTable['TimeRequested'] = map(lambda x: parser.convertToDate(x), vasTable['TimeRequested'])
    psqiGlobalVas = pd.merge(psqiFrame, vasTable, on = 'ID')
    print psqiGlobalVas
    psqiVasSameDay = psqiGlobalVas[psqiGlobalVas['Date'] == psqiGlobalVas['TimeRequested']][
        ['ID', 'Value', 'Score', 'Date', 'TimeRequested']]
    psqiVasSameDay.plot(x= 'Score', y = 'Value', kind = 'scatter')
    #create groups
    groups = psqiVasSameDay.groupby(['ID'])

    # plot

    fig, ax = plt.subplots()
    ax.margins(0.05)
    for name, group in groups:
        ax.plot(group.Score, group.Value, marker= 'o', linestyle = '', ms=12, label=name)

    plt.show()
    return psqiVasSameDay

    #need to find the time between the VAS and the PSQI. find delta

if __name__ == '__main__':
    print main()