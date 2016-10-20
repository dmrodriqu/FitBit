# Dylan Rodriquez
# import packages here
import os
import json
import pandas as pd
import datetime
import math
from pandas.io.json import json_normalize

# file i/o

# path to fitbit data here

path = '/Users/Dylan/Dropbox/FitBit/data_20161012'


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

def createdataframe(path, datatofind):
    # type: (string, string) -> np.dataFrame
    # setup of divide and conquer for creation of dictionary of directory and subdirectory of patient information
    # set json keys and path values
    string_to_search_for = ''
    json_key = ''
    if datatofind == 'sleep':
        string_to_search_for = 'sleep'
        json_key = 'sleep'
    elif datatofind == 'step':
        string_to_search_for = 'step'
        json_key = 'activities-steps'
    elif datatofind == 'survey':
        string_to_search_for = '_'

    # path  --> list of directories in data_1
    def directList(path):
        # type: (string) -> [string]
        directoryList = [x for x in os.listdir(path) if os.path.isdir(x) and x != '.git']
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
        f = path + '/' + dictionaryOfDirectories.keys()[dictionary_index] + '/' + \
            str(dictionaryOfDirectories.values()[dictionary_index])
        list_of_json_files.append(f)
        dictionary_index += 1
    # [filepath] --> JSON data object
    all_frames = []
    # condition block if sleep or step here
    # abstract to function later
    if datatofind == 'survey':
        df = []
        for json_file in list_of_json_files:
            json_to_parse = open(json_file).read()
            data = json.loads(json_to_parse)
            # data.key[0]: data.value[1][0], # key[1]: value[1][1], # key[2]: value[1][2]...# key[n]: value[1][n]
            df.append(json_normalize(data))
            # JSON --> [pd.DataFrame]
        return pd.concat(df)
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
                df.append(json_normalize(data[date], json_key))
            singleframe = pd.concat(df)
            singleframe['id'] = json_file
            all_frames.append(singleframe)
        return pd.concat(all_frames)


# data =  createdataframe(path, datatofind = str(where datatofind =='sleep'|'step'|'survey')
# idbl = data[data['id']=='/Users/Dylan/Dropbox/FitBit/data_1/BLqS60/BLqS60-sleep-data.json']

# examples
step_data = createdataframe(path, 'step')
sleep_data = createdataframe(path, 'sleep')
survey_data = createdataframe(path, 'survey')



def get_gps(survey_dataframe):
    # type: (np.dataFrame) -> [{'string':int, 'string':{'string':float, 'string':float}}]
    location_dictionary_array = []
    i = 0
    while i < len(survey_data):
        location_dictionary_array.append([x for x in survey_data['location']][i])
        i += 1
    return location_dictionary_array


testing = get_gps(survey_data)

def gps_to_distance(locationdictionary, index):
    # type: [{'string':int, 'string':{'string':float, 'string':float}}] -> [float],[float],[int]
    array_of_longitudes = []
    array_of_latitudes = []
    array_of_time = []
    # just one at a time, iterate with function
    for x in locationdictionary[index]:
        array_of_latitudes.append(x[u'Value'][u'Lat'])
        array_of_longitudes.append(x[u'Value'][u'Lng'])
        array_of_time.append(x[u'TimeCompleted']/1000)
    return array_of_latitudes, array_of_longitudes, array_of_time

euclidlist =  gps_to_distance(testing, 0)


# latitude_array, longitude_array, time_list -->[average velocity]
def euclid_slope_lat_long(latitude_array, longitude_array, time_list):
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

    while index_of_n + 1 < len(latitude_array):
        distance = haversine(latitude_array[index_of_n], latitude_array[index_of_n + 1],
                             longitude_array[index_of_n], longitude_array[index_of_n + 1])
        time_difference_a = time_list[index_of_n + 1] - time_list[index_of_n]
        time_difference_a = time_difference_a / (3600.00)
        velocities.append(distance / time_difference_a)
        times.append(int(str(time_list[index_of_n])))
        index_of_n += 1
    return times, velocities

data = euclid_slope_lat_long(euclidlist[0], euclidlist[1], euclidlist[2])
import collections


import time

from bokeh.plotting import figure, output_file, show
from bokeh.plotting import *
import numpy as np

# from bokeh.plotting import figure, output_file, show
# print data
x = data[0]
# x = (map(lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d'),data[0]))
#print x
y = data[1]

# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title="Velocity Vs Time Using Raw GPS Data", x_axis_label='Date Time', y_axis_label='MPH', )

# add a line renderer with legend and line thickness
p.line(x, y, legend="Velocity.", line_width=2)
p.xaxis.major_label_orientation = np.pi / 4
# show the results
show(p)
