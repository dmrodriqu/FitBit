import parser
import pandas as pd
import matplotlib.pyplot as plt

fpath = '/Volumes/rubin-lab/UChicagoIBD_data.json'
    # get PSQI scores from all individuals
    # parse Json to DataFrame
fullDataFrame = parser.parseJsonFile(fpath)
    # Generate PSQI table from DataFrame
sleep = parser.Table()
sleepSeries = sleep.recursiveRows(fullDataFrame, 'Fitbit', 'Sleep')
sleepFrame = sleep.createSleepColumns(fullDataFrame, sleepSeries)
    # Convert Unix to DateTime
print sleepFrame[sleepFrame['ID'] == '5Ufjnr']


#5Ufjnr