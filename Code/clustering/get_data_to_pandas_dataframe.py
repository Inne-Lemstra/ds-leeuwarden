#! /bin.usr/python3
#(C) Inne Lemstra 22-06-18
"""Read in data from locatus CSV file and transform it in such a way that the resulting pandas data frame contains: 
rows: unique ID's cols: binned time period (every half hour). 

The indexes are number of hits in a half hour. 
Data is only loaded in for the specific data 2016-11-17. To improve speed and responsivness during testing """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Save way to open a file
data_path = "/home/inne/Documents/lw_data_science/data/locatus/locatusdata_bewerkt.csv"

def load_date(date, data_path):
    """load in only the lines data with a spefic date in them"""
    with open(data_path, 'r') as data_handle:
        #skip first header line
        header = data_handle.readline()
        line = data_handle.readline()
        #save the data we want to keep, as python list
        data = []
        #loop over all lines in file, reading after last line will return empty
        #i.e. false
        while line:
            #select for specific data
            if date in line:
                data.append(line)
            #go to next line
            line = data_handle.readline()
    return (data, header)


#split and clean each row of data into its own list
#using python list comprehensions it loops over all rows in data list
#and splits on ; then picks an index and strips this of " afterwards gets put in 
#new list
(data, header) = load_date("2016-11-17", data_path)

nodes = [row.split(";")[1].strip("\"")  for row in data]
times = [row.split(";")[2].strip("\"")  for row in data]
durations = [row.split(";")[3].strip("\"")  for row in data]
individuals = [row.split(";")[4].strip("\n")  for row in data]

#create the col names which is the day split in 30 min segments
cols = pd.date_range('2016-11-17', periods = 49, freq = '30Min')

#test to histogram over every hour 
t4 = pd.DataFrame({"individual": individuals, "time": times})

t4["time"] = t4["time"].astype("datetime64")

#t4.groupby(t4["time"].dt.hour).count().plot()
#plt.show

hist_df = pd.DataFrame(columns = cols)

print("begonnen met de super lange histogram loop")

for row in range(int(len(t4)/10)):
    colNr = 0
    for col in cols:
        if t4.iloc[row,:]["time"] > cols[colNr]:
            #print(t4.iloc[row,:]["time"])
            colNr += 1
        else:
            try:
                hist_df.loc[t4.iloc[row,:]["individual"],cols[colNr]] += 1
            except KeyError:
                hist_df.loc[t4.iloc[row,:]["individual"],cols[colNr]] = 1
                #hist_df[t4.iloc[row,:]["individual"],hist_df.columns != cols[colNr]] = 0
                
            continue

print(hist_df.head())

hist_df.to_csv("./output.csv")

 



