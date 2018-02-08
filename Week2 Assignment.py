# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 18:08:09 2018

@author: sonia
"""
import pandas
import numpy

# Read the data from csv
data = pandas.read_csv("gapminder.csv", low_memory = False)

# Bug fix to avoid run time errors for display formats
pandas.set_option("display.float_format",lambda x:'%f'%x)

#lower-case all Dataframe column names
data.columns = map(str.lower,data.columns)

# Get to know the data
print(len(data))            # Print number of rows
print(len(data.columns))    # Print number of columns
print(data.columns)         # Print column names

# Set required variables to numeric
data['internetuserate'] = pandas.to_numeric(data['internetuserate'])
data['suicideper100th'] = pandas.to_numeric(data['suicideper100th'])
data['suicide0to14per100th'] = pandas.to_numeric(data['suicide0to14per100th'])
# Couldn't use .convert_objects(convert_numeric=True) because it has been deprecated

# Lets check the counts and percentages i.e. Frequency Distribution
print("Frequency Distribution for Internet Usage")
c1 = data["internetuserate"].value_counts(sort=False)
p1 = data["internetuserate"].value_counts(sort=False,normalize = True)
internet_freq = pandas.concat(dict(counts = c1, percentages = p1),axis = 1)
print(internet_freq.head(10))
                         
print("Frequency Distribution for Suicide Per 100th")
c2 = data.groupby("suicideper100th").size()
p2 = data.groupby("suicideper100th").size() * 100 / len(data)
suicide_freq = pandas.concat(dict(counts = c2, percentages = p2),axis = 1)
print(suicide_freq.head(10))

print("Freq. Dist. for Suicide Per 100th in children under 14 years of age")
c3 = data["suicide0to14per100th"].value_counts(sort=False)
p3 = data["suicide0to14per100th"].value_counts(sort=False,normalize = True)
suicide_14_freq = pandas.concat(dict(counts = c3, percentages = p3),axis = 1)
print(suicide_14_freq.head(10))

# Refining the search question to see how many countries with high suicide rate 
# have a high internetuserate too

# Select countries that have higher than average suicide rates
sub1 = data[data["suicideper100th"]>=data["suicideper100th"].mean()]
print("Out of total %d countries, %d countries have higher than average suicide rate" %(len(data),len(sub1)))

# Check frequency distribution of internet usage in these countries now
print("Frequency Distribution for Internet Usage in countries with higher than average suicide rates")
c4 = sub1["internetuserate"].value_counts(sort=False)
p4 = sub1["internetuserate"].value_counts(sort=False,normalize = True)
internet_freq_new = pandas.concat(dict(counts = c4, percentages = p4),axis = 1)
print(internet_freq_new.head(10))

# Check how many of these countries have higher than average internet usage
sub2 = sub1[sub1["internetuserate"]>=data["internetuserate"].mean()]
print("%d%% of the countries with higher than average suicide rate have higher than average internet use rates too." %(len(sub2) * 100 / len(sub1)))
