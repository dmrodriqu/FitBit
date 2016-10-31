# Dylan Rodriquez
# import packages here
import os
import json
import pandas as pd
import re
import datetime
import math
from pandas.io.json import json_normalize

# file i/o

# path to fitbit data here

fpath = '/Users/Dylan/Dropbox/FitBit/data_20161012'


# data organized in the following manner:
# ID_1_dir
# ----sleep_json_file
# ----step_json_file
# ----survey_json_file
# ID_2_dir
# ----sleep_json_file
# ----step_json_file
# ----survey_json_file
# ...
# ID_n_dir
# ----sleep_json_file
# ----step_json_file
# ----survey_json_file

class Table:
    def __init__(self):
        self.listofframes = []
        self.dataType = ''

    def parseJSON(self, path, datatofind):
        # type: (string, string) -> np.dataFrame
        # setup of divide and conquer for creation of dictionary of directory and subdirectory of patient information
        # set json keys and path values
        string_to_search_for = ''
        json_key = ''
        if datatofind == 'sleep':
            string_to_search_for = 'sleep'
            self.dataType = 'sleep'
            json_key = 'sleep'
            json_key_2 = 'summary'
        elif datatofind == 'step':
            self.dataType = 'step'
            string_to_search_for = 'step'
            json_key = 'activities-steps'
            json_key_2 = "activities-steps-intraday"
        elif datatofind == 'survey':
            self.dataType = 'survey'
            string_to_search_for = '_'

        # path  --> list of directories in data_1
        def directList(path):
            # type: (string) -> [string]
            directoryList = [path + '/' + str(x) for x in os.listdir(path) if os.path.isdir(path + '/' + str(x))]
            return directoryList

        # path  --> list of subdirectories in data_1
        def directNestList(path):
            # type: (string) -> [string]
            sleepfiles = []
            fileList = [os.listdir(x) for x in directList(path)]
            for sublist in fileList:
                index_of_sleep_JSON = 0
                ###
                ### adjust for binary search later...will be inefficient after larger dataset introduced if not!#
                ###
                # search for string in file name
                # can later be abstracted to include sleep, step, survey class
                while index_of_sleep_JSON < len(sublist):
                    if sublist[index_of_sleep_JSON].find(string_to_search_for) == -1:
                        # not found, increment index by one
                        index_of_sleep_JSON += 1
                    else:
                        break
                sleepfiles.append(sublist[index_of_sleep_JSON])
            return sleepfiles

        # create dictoionary
        dictionaryOfDirectories = {}
        # [directories];[files in directories] ---> {directory:files in directory}
        # annotation of method:
        # index 0 updated with index 0, {1:1}, {2:2}... {n:n}...
        i = 0
        # highest index will be len-1
        while i < len(directList(path)):
            dictionaryOfDirectories.update({directList(path)[i]: directNestList(path)[i]})
            i += 1
        ######for each data frame#####
        # with dictionary of directories, for each key: take value and form file path
        # {directory:files in directory} --> str(filepath)
        dictionary_index = 0
        list_of_json_files = []
        while dictionary_index < len(dictionaryOfDirectories.keys()):
            f = dictionaryOfDirectories.keys()[dictionary_index] + '/' + \
                str(dictionaryOfDirectories.values()[dictionary_index])
            list_of_json_files.append(f)
            dictionary_index += 1
        # [filepath] --> JSON data object
        # self.listofframes = []
        # condition block if sleep or step here
        # abstract to function later
        if datatofind == 'survey':
            for json_file in list_of_json_files:
                json_to_parse = open(json_file).read()
                data = json.loads(json_to_parse)
                # data.key[0]: data.value[1][0], # key[1]: value[1][1], # key[2]: value[1][2]...# key[n]: value[1][n]
                self.listofframes.append(json_normalize(data))
                # JSON --> [pd.DataFrame]

        else:

            for json_file in list_of_json_files:
                json_to_parse = open(json_file).read()
                data = json.loads(json_to_parse)
                dates = data.keys()
                # normalize json survey via iteration over survey values
                # JSON --> [pd.DataFrame]
                df = []
                # insert ID by traversing dictionary of directory/files again
                for date in dates:
                    # create the dataframe for each date
                    df.append(json_normalize(data[date], json_key, json_key_2))
                singleframe = pd.concat(df)
                singleframe['id'] = json_file
                self.listofframes.append(singleframe)

    def getDataFrame(self):
        return pd.concat(self.listofframes).reset_index()

    def getGPS(self, tableFrame):
        # type: (np.dataFrame) -> [{'string':int, 'string':{'string':float, 'string':float}}]
        location_dictionary_array = []
        i = 0
        while i < len(tableFrame):
            location_dictionary_array.append([x for x in tableFrame['location']][i])
            i += 1
        return location_dictionary_array

    def gps_rdt(self, locationDictionary, index):
        # type: [{'string':int, 'string':{'string':float, 'string':float}}] -> [float],[float],[int]
        array_of_longitudes = []
        array_of_latitudes = []
        array_of_time = []
        # just one at a time, iterate with function
        for x in locationDictionary[index]:
            array_of_latitudes.append(x[u'Value'][u'Lat'])
            array_of_longitudes.append(x[u'Value'][u'Lng'])
            array_of_time.append(x[u'TimeCompleted'] / 1000)
        return array_of_latitudes, array_of_longitudes, array_of_time

    # latitude_array, longitude_array, time_list -->[average velocity]
    def euclid_slope_lat_long(self, latitude_array, longitude_array, time_list):
        # method -->
        # start n=1
        #
        #  xn - x(n-1)
        # -------------
        #  tn-t(n-1)
        # repeat for n and n + 1
        # average
        # use as t(n)
        # x(n) is the haversine formula
        index_of_n = 1
        times = []
        velocities = []

        def haversine(lat1, lat2, lon1, lon2):
            # type: (float, float, float, float) -> float
            r = 3959
            lat1, lat2, lon1, lon2 = map(math.radians, [lat1, lat2, lon1, lon2])
            lat_part = math.sin((lon2 - lon1) / 2) ** 2
            lon_part = math.sin((lat2 - lat1) / 2) ** 2
            sqrt_part = (lon_part + math.cos(lat1) * math.cos(lat2) * lat_part) ** (0.5)
            return 2 * r * math.asin(sqrt_part)

        # similar to fibonacci alg. change to address efficiency.
        # create array of size n
        # iterate over distances, change values of array
        while index_of_n + 1 < len(latitude_array):
            distance = haversine(latitude_array[index_of_n], latitude_array[index_of_n + 1],
                                 longitude_array[index_of_n], longitude_array[index_of_n + 1])
            time_difference_a = time_list[index_of_n + 1] - time_list[index_of_n]
            time_difference_a = time_difference_a / (3600.00)
            velocities.append(distance / time_difference_a)
            times.append(int(str(time_list[index_of_n])))
            index_of_n += 1
        return times, velocities


table1 = Table()
table1.parseJSON(fpath, 'survey')
frame = table1.getDataFrame()
gps = table1.getGPS(frame)
gps1 = table1.gps_rdt(gps, 0)
#distance1 = table1.gps_to_distance(gps1,0)
euclidiangps1 = table1.euclid_slope_lat_long(gps1[0], gps1[1], gps1[2])
print euclidiangps1



# data = euclid_slope_lat_long(euclidlist[0], euclidlist[1], euclidlist[2])
import collections

import time

from bokeh.plotting import figure, output_file, show
from bokeh.plotting import *
import numpy as np

# from bokeh.plotting import figure, output_file, show
# print data
# x = data[0]
# x = (map(lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d'),data[0]))
# print x
# y = data[1]

# output to static HTML file
# output_file("lines.html")

# create a new plot with a title and axis labels
# p = figure(title="Velocity Vs Time Using Raw GPS Data", x_axis_label='Date Time', y_axis_label='MPH', )

# add a line renderer with legend and line thickness
# p.line(x, y, legend="Velocity.", line_width=2)
# p.xaxis.major_label_orientation = np.pi / 4
# show the results
# show(p)

# get IDs from filepaths, create new colums for patient ID
ID_array = []
for each in step_data['id']:
    regex = r"(?<=\W)[a-zA-Z0-9]{6}"
    test_str = each
    matches = re.findall(regex, test_str)
    ID_array.append(matches[3])
step_data['ID'] = ID_array

# last minute graphing
'''ID_array = []
for each in sleep_data['id']:
    regex = r"(?<=\W)[a-zA-Z0-9]{6}"
    test_str = each
    matches = re.findall(regex, test_str)
    ID_array.append(matches[3])
sleep_data['ID'] = ID_array






step = step_data[step_data['ID'] == 'BLqS60']
sleep = sleep_data[sleep_data['ID']=='BLqS60']
#survey = survey_data[survey_data['ID'] == 'BLqS60']
survey = survey_data.reset_index()
print step
print sleep
print survey

timeframes=[]
answers = []
for each in survey.ix[0]['UChicagoIBD/']:
    timeframes.append(each['TimeCompleted'])
    answers.append(each['Value'])


import time


datetimes = map(lambda x: time.strftime('%Y-%m-%d', time.localtime(x/1000)), timeframes)
sleepepochs = []
from datetime import datetime
import time
from calendar import timegm

sleeptime = sleep['dateOfSleep'].values
for each in sleeptime:
    utc_time = time.strptime(each, '%Y-%m-%d')
    epoch_time = timegm(utc_time)*1000
    sleepepochs.append(epoch_time)

sleepeffic = sleep['efficiency'].values




import numpy as np
import bokeh.plotting as bp
from bokeh.models import HoverTool
bp.output_file('test.html')

fig = bp.figure()
x1 = timeframes
x2 = sleepepochs
y1 = [float(i)/max(answers) for i in answers]
y2 = [float(i)/max(sleepeffic) for i in sleepeffic]
s1 = fig.scatter(x=x1,y=y1,color='#0000ff',legend='='')
s2 = fig.scatter(x=x2,y=y2,color='#ff0000',legend='')
bp.show(fig)


print x2

print "x"
print x1
print x2
'''
