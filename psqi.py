import parser
import pandas as pd
import matplotlib.pyplot as plt
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
        'Date' : dateSeries}

    psqiFrame = pd.DataFrame(psqiDataFrame)
    vas = parser.Table()
    vasRows = vas.recursiveRows(fullDataFrame, 'Litmus', "UChicagoIBD/SubjectGlobalAssessmentVAS")
    vasTable = vas.createStepOrHeartColumns(fullDataFrame, vasRows)
    vasTable = parser.readableDate(vasTable)
    psqiGlobalVas = pd.merge(psqiFrame, vasTable, on = 'ID')
    psqiVasSameDay = psqiGlobalVas[psqiGlobalVas['Date'] == psqiGlobalVas['TimeCompleted']][
        ['ID', 'Value', 'Score', 'Date', 'TimeCompleted']]

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