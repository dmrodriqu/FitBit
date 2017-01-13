# $csvparser
# ----------
# $csvparser parses JSON to HD5. The program originally parsed to csv files
# hence, the name.
#
# This program parses several tables from the main JSON file to several persistent
# files:
#
# globalVas.h5
# heartFrame.h5
# sleepFrame.h5
# stepFrame.h5
# psqiFrame.h5
#
#
#
# requires pytables
# brew tap homebrew/science
# brew install hdf5
#
# outputs an hd5 file indexed by patient ID. use for i/o in pandas
# >>> fpath = filepath to hd5 file
# >>> nameOfTable = name of table saved in hd5
# >>> idCond = string formatted : 'ID' == "PT_ID_TO_FIND" <---- double quotes neccesary
# >>> pd.read_hdf(fpath, nameOfTable, idCond)
# Data Frame
#
#

import pandas as pd
from parser import parseJsonFile, createSurveyTable
from parser import convertToDate
from parser import Table

fpath = '/Volumes/rubin-lab/UChicagoIBD_data.json'


def encodeAndExport(df, nameOfFrame):

    def unicodeToString(df):
        types = df.apply(lambda x: pd.lib.infer_dtype(x.values))
        unicodeType = types[types == 'unicode']
        for col in unicodeType.index:
            df[col] = df[col].astype(str)
        return df

    def parseAndExport(df, dfName):
        stringtoname = dfName
        fileAndExt = "%s.h5" % stringtoname
        storageName = "%s" % stringtoname
        print (stringtoname)
        return df.to_hdf(fileAndExt, storageName,
                     mode='w', format='table', data_columns=['ID'])

    encoded = unicodeToString(df)
    return parseAndExport(encoded, nameOfFrame)
# parsing data storing as csv
def main():
    fullDataFrame = parseJsonFile(fpath)
    Vas = Table()
    globalVas = Vas.recursiveRows(
        fullDataFrame, 'Litmus', "UChicagoIBD/SubjectGlobalAssessmentVAS")
    globalVasFrame = Vas.createStepOrHeartColumns(fullDataFrame, globalVas)
    encodeAndExport(globalVasFrame, 'globalVas')

    # all but timeseries data
    # store timeseries separately i/o bound/hdf encoding to solve
    # maybe coerce to string -> eval back later.
    steps = Table()
    stepSeries = steps.recursiveRows(fullDataFrame, 'Fitbit', 'Steps')
    stepFrame = steps.createStepOrHeartColumns(fullDataFrame, stepSeries)
    stepFrame = stepFrame.drop(['Timeseries'], axis=1)
    encodeAndExport(stepFrame, 'stepFrame')



    psqiTable = createSurveyTable(fullDataFrame, 'PSQI')
    encodeAndExport(psqiTable, 'psqiTable')


  # sibdqTable = createSurveyTable(fullDataFrame, 'SIBDQ')




  # sleep = parser.Table()
  # sleepSeries = sleep.recursiveRows(fullDataFrame, 'Fitbit', 'Sleep')
  # sleepFrame = sleep.createSleepColumns(fullDataFrame, sleepSeries)

  # heart = parser.Table()
  # heartSeries = heart.recursiveRows(fullDataFrame, 'Fitbit', 'Heart')
  # heartFrame = heart.createStepOrHeartColumns(fullDataFrame, heartSeries)


  # types = globalVasFrame.apply(lambda x: pd.lib.infer_dtype(x.values))
  # unicodeType = types[types == 'unicode']
  # for col in unicodeType.index:
  #    globalVasFrame[col] = globalVasFrame[col].astype(str)
  # globalVasFrame.to_hdf('globalVas.h5', 'globalVas',
  #                      mode='w', format='table', data_columns=['ID'])


  # stepFrame.to_hdf('stepFrame.h5', 'stepFrame')
  # sleepFrame.to_hdf('sleepFrame.h5', 'sleepFrame')
  # heartFrame.to_hdf('heartFrame.h5', 'heartFrame')


if __name__ == '__main__':
    main()
