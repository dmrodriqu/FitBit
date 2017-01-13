# About
# -------
# psqivstep.py creates a graph ready solution for psqi data and step data from all fitbit data
#
#
#
# Input/Output Format
# ------------
# the function psqiStep takes an ID and outputs a graph of total steps for each psqi interval
# i.e. date1 for PSQI score1  = (steps will be totaled for 14 days prior)
# datapoint 1 = totaledSteps1 vs PSQIscore1
#
#
# Reqiurements
# ------------
#
# modules required:
# -----------------
# stepProcessor.py
# PSQImain.py
# pandas (pip install pandas)
# matplotlib (pip install matplotlib)
#
# Usage
# -----
# >>> id = "PATIENT_IDENTIFIER_WITH_QUOTES"
# >>> idPsqiSteps = psqiStep(id)
# (          Date  Total
# 0   2016-07-01   3191
# 1   2016-07-02  16256
# 2   2016-07-03  21690
# 3   2016-07-04   9092
# .       .         .
# .       .         .
# .       .         .
# 19  2016-07-20   4921
#          Date      ID  Score
# 0  2016-07-05  BLqS60      7
# 1  2016-07-20  BLqS60      7)
#
#
# Support
# -------
# for issues dylanmr@uchicago.edu


from stepProcessor import Timeseries
from PSQImain import psqiParse
# goal is to take one ID and to return a graph of PSQI
# vs Step Count(two week prior)
# testID 'BLqS60'


def returnStepsPerID(ID):

    newSeries = Timeseries(ID)
    return newSeries.stepCountByID()


def returnPsqiPerID(ID):
    newFrame = psqiParse(ID)
    return newFrame


def pqsiStep(ID):
    steps = returnStepsPerID(ID)
    psqi = returnPsqiPerID(ID)
    return steps, psqi


print pqsiStep('BLqS60')
