# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:42:58 2018

@author: sonia
"""

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt

# Read the data from csv
data = pandas.read_csv("gapminder.csv", low_memory = False)

# Set pandas to show all columns and rows in Dataframe
pandas.set_option("display.max_columns",None)
pandas.set_option("display.max_rows",None)

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

# Lets convert the other two as well
print("Frequency distribution of suicide per 100th - in categories")
sub2["suicidelabel"] =pandas.cut(sub2.suicideper100th,4,labels=["low","medium","high","very high"])
c5 = sub2["suicidelabel"].value_counts(sort=False)
p5 = sub2["suicidelabel"].value_counts(sort=False,normalize = True)
suicide_label_freq = pandas.concat(dict(counts = c5, percentages = p5),axis = 1)
print(suicide_label_freq)

print("Frequency distribution of suicide in children under 14- in categories")
sub2["childsuicidelabel"] =pandas.cut(sub2.suicide0to14per100th,4,labels=["low","medium","high","very high"])
c6 = sub2["childsuicidelabel"].value_counts(sort=False)
p6 = sub2["childsuicidelabel"].value_counts(sort=False,normalize = True)
child_suicide_label_freq = pandas.concat(dict(counts = c6, percentages = p6),axis = 1)
print(child_suicide_label_freq)

# Lets plot the categorical variables - 
seaborn.countplot(x="internetlabel", data = sub2)
plt.xlabel("Internet Usage Rate")
plt.title("Internet Usage Rate in countries that have Suicide data available")

seaborn.countplot(x="suicidelabel", data = sub2)
plt.xlabel("Suicide Rate per 100th")
plt.title("Suicide Per 100th in countries that have suicide data available for children under 14 years of age")

# Get the descriptive statistics for the 3 variables
print("Descriptive Stastistics for Internet Use Rate")
desc1 = sub2["internetuserate"].describe()
print(desc1)

print("Descriptive Stastistics for Suicide Rate")
desc2 = sub2["suicideper100th"].describe()
print(desc2)

# TESTING CAUSALITY
# High internet use rate leads to high suicide rate
# Both Response and Explanatory variables are categorical
# Since Response variable has more than 2 categories, lets reduce the categories to 2
suicide_mean = sub2["suicideper100th"].mean()

def change_suicide(row):
    if row["suicideper100th"] > suicide_mean:
        return 1
    else:
        return 0

sub2["suicide"] = sub2.apply(lambda row:change_suicide(row),axis = 1)

# Convert this new variable to a numeric variable to use factorplot
sub2["suicide"] = pandas.to_numeric(sub2["suicide"])

seaborn.factorplot(x="internetlabel",y="suicide",data=sub2,kind="bar",ci=None)
plt.xlabel("Internet Use Rate")
plt.ylabel("Proportion High Suicide Rate")
plt.title("Internet Use Rate vs. Proportion of Higher than mean suicide rates")

# Lets try scatter plot
seaborn.regplot(x="internetuserate",y="suicideper100th",data = sub2)
plt.xlabel("Internet Use Rate")
plt.ylabel("Suicide Rate per 100th")
plt.title("Scatter plot for association between Internet Use Rate and Suicide Rates per 100th")
