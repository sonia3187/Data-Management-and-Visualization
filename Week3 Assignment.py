# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:06:24 2018

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

# Set required variables to numeric
data['internetuserate'] = pandas.to_numeric(data['internetuserate'])
data['suicideper100th'] = pandas.to_numeric(data['suicideper100th'])
data['suicide0to14per100th'] = pandas.to_numeric(data['suicide0to14per100th'])

# Create a new dataset that contains only the reqiured variables. Drop everything else.
sub1 = data[['country','internetuserate', 'suicideper100th','suicide0to14per100th']]
sub2 = sub1.copy()

#remove missing values - we only need cases where we have data in all three columns
sub2.head(10)
sub2 = sub2.dropna()
print(len(sub2))       #Left with only 49 countries to analyze
print(len(sub2.columns))

# Lets check the counts and percentages i.e. Frequency Distribution
print("Frequency Distribution for Internet Usage")
c1 = sub2["internetuserate"].value_counts(sort=False)
p1 = sub2["internetuserate"].value_counts(sort=False,normalize = True)
internet_freq = pandas.concat(dict(counts = c1, percentages = p1),axis = 1)
print(internet_freq.head(10))
                         
print("Frequency Distribution for Suicide Per 100th")
c2 = sub2.groupby("suicideper100th").size()
p2 = sub2.groupby("suicideper100th").size() * 100 / len(sub2)
suicide_freq = pandas.concat(dict(counts = c2, percentages = p2),axis = 1)
print(suicide_freq.head(10))

print("Freq. Dist. for Suicide Per 100th in children under 14 years of age")
c3 = sub2["suicide0to14per100th"].value_counts(sort=False)
p3 = sub2["suicide0to14per100th"].value_counts(sort=False,normalize = True)
suicide_14_freq = pandas.concat(dict(counts = c3, percentages = p3),axis = 1)
print(suicide_14_freq.head(10))

# Frequency distribution of numeric variables provides no useful information
# Lets convert the numeric variables into categorical variables
print("Frequency distribution of internet use rate - in categories")
sub2["internetlabel"] =pandas.cut(sub2.internetuserate,4,labels=["low","medium","high","very high"])
c4 = sub2["internetlabel"].value_counts(sort=False)
p4 = sub2["internetlabel"].value_counts(sort=False,normalize = True)
internet_label_freq = pandas.concat(dict(counts = c4, percentages = p4),axis = 1)
print(internet_label_freq)

# Check the va;lues of categorical variable - internetlabel
a = sub2[["country","internetlabel","internetuserate"]]
print(a.head(10))

# Lets convert the other two as well
print("Frequency distribution of suicide per 100th - in categories")
sub2["suicidelabel"] =pandas.cut(sub2.suicideper100th,4,labels=["low","medium","high","very high"])
c5 = sub2["suicidelabel"].value_counts(sort=False)
p5 = sub2["suicidelabel"].value_counts(sort=False,normalize = True)
suicide_label_freq = pandas.concat(dict(counts = c5, percentages = p5),axis = 1)
print(suicide_label_freq)

print("Frequency distribution of suicide in children under 14- in categories")
sub2["child_suicide_label"] =pandas.cut(sub2.suicide0to14per100th,4,labels=["low","medium","high","very high"])
c6 = sub2["child_suicide_label"].value_counts(sort=False)
p6 = sub2["child_suicide_label"].value_counts(sort=False,normalize = True)
child_suicide_label = pandas.concat(dict(counts = c6, percentages = p6),axis = 1)
print(child_suicide_label)

# Lets see if there is a co-relation between our high internet usage and high overall suicide rate
print("High internet usage in correlation with high suicide rate per country")
intsui = sub2[(sub2["suicidelabel"] == "high") | (sub2["suicidelabel"] == "very high")]
intsui=intsui.sort_values(by="internetlabel", ascending = False)
print(intsui.loc[:, ["country", "internetlabel", "suicidelabel"]])    

# Lets see if the countries with high child suicide rate have high internet rates too
print("High high suicide rate in children under 14 in correlation with High internet usage - per country")
intchisui= sub2[(sub2["internetlabel"] == "high") | (sub2["internetlabel"] == "very high")]
intchisui=intchisui.sort_values(by="child_suicide_label", ascending = False)
print(intchisui.loc[:, ["country", "child_suicide_label", "internetlabel"]])    
