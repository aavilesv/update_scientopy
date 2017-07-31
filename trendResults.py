#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import csv
import paperUtils
import paperSave
import globalVar
import os
import sys
import matplotlib.pyplot as plt
import math
import pprint


import argparse
parser = argparse.ArgumentParser()

parser.add_argument("criteria", choices=["authors", "source", "subject",
"authorKeywords", "indexKeywords", "documentType", "dataBase", "country"], 
help="Search criteria, ex: ")

parser.add_argument("-l", "--length", type=int, default=10, help="Length of the top items listed")

parser.add_argument("-s", "--start", type=int, default=0,  help="To filter the \
first element, ex to filter the first 2 elements on the list use -s 2")

parser.add_argument("--startYear", type=int, default=2000,  help="Start year to limit the search")
parser.add_argument("--endYear", type=int, default=2016,  help="End year year to limit the search")

parser.add_argument("--pYear", 
help="To present the results in percentage per year", action="store_true")

parser.add_argument("--neg", 
help="Get the top documents with the worst growth rate", action="store_true")

args = parser.parse_args()

INPUT_FILE = globalVar.DATA_OUT_FOLDER + "papersOutput.txt"

# Program start ********************************************************
 
# Start paper list empty
papersDict = []

# Open the database and add to papersDict 
ifile = open(INPUT_FILE, "rb")
print("Reading file: %s" % (INPUT_FILE))
paperUtils.analyzeFileDict(ifile, papersDict)
ifile.close()

print("Scopus papers: %s" % globalVar.papersScopus)
print("WoS papers: %s" % globalVar.papersWoS)
print("Omited papers: %s" % globalVar.omitedPapers)
print("Total papers: %s" % len(papersDict))

# Create a yearArray
yearArray = range(args.startYear, args.endYear + 1)

# Create yearPapers dict to store the total papers per year
yearPapers = {}
for i in range(args.startYear, args.endYear + 1):
  yearPapers[i] = 0
  
# Create a topic list
topicList = {}

# Find the total documents per topic
for paper in papersDict:
  if int(paper["year"]) in yearPapers.keys():
    yearPapers[int(paper["year"])] += 1 
    
  for item in paper[args.criteria].split("; "):
    if item == "":
      continue
    
    # filter not included years
    if int(paper["year"]) not in yearArray:
      continue
    if item.upper() in topicList:
      topicList[item.upper()] += 1 
    else:
      topicList[item.upper()] = 1 


# Get the top topics
topTopcis = sorted(topicList.iteritems(), 
key=lambda x:-x[1])[int(args.start):globalVar.TOP_TREND_SIZE]

count = 0
print("\nTop topics:")
for x in topTopcis:
  count += 1
  print "{0}-> {1}: {2}".format(count,*x)
  
if args.start > 0:
  topTopicsFilterd = sorted(topicList.iteritems(), 
  key=lambda x:-x[1])[0:int(args.start)]
  print("\nTop topics before start:")
  count = 0
  for x in topTopicsFilterd:
    count += 1
    print "{0}-> {1}: {2}".format(count,*x)
    
  

# Create results data dictionary
dataDic = {}

for topic in topTopcis:
  dataDic[topic[0]] = {}
  dataDic[topic[0]]["year"] = yearArray
  dataDic[topic[0]]["count"] = [0] * len(yearArray)
  dataDic[topic[0]]["rate"] = [0] * len(yearArray)
  dataDic[topic[0]]["averageRate"] = 0
  dataDic[topic[0]]["total"] = 0
  dataDic[topic[0]]["name"] = 0


# Find the documents per year for topTopics
noIncludedInRange = 0
for paper in papersDict:
  # run on input arguments
  for item in paper[args.criteria].split("; "):
    for topic in topTopcis:
      if topic[0].upper() == item.upper():
        try:
          index = dataDic[item.upper()]["year"].index(int(paper["year"]))
          dataDic[item.upper()]["count"][index] += 1
          dataDic[item.upper()]["total"] += 1
          dataDic[item.upper()]["name"] = item
        except:
          noIncludedInRange += 1
          #print("Paper on year: %s" % paper.year)

#print(dataDic)


# Get the rate per year, and averageRate
for key, data in dataDic.iteritems():
  pastCount = 0
  data["averageRate"] = 0
  for i in range(0,len(data["year"])):
    data["rate"][i] = data["count"][i] - pastCount
    pastCount = data["count"][i]
    
    if i > (len(data["year"]) - (globalVar.AVERAGE_RATE_YEARS + 1)):
      data["averageRate"] += data["rate"][i]
  data["averageRate"] /= globalVar.AVERAGE_RATE_YEARS
    
# Get the top trends
if args.neg:
  topTrends = sorted(dataDic.iteritems(), key=lambda (k,v): (v["averageRate"],k))
else:
  topTrends = sorted(dataDic.iteritems(), key=lambda (k,v): (-v["averageRate"],k))
  
count = 1
print("\nTop average rate")
for item in topTrends:
  print("%s. %s: %s" % (count, item[1]["name"], item[1]["averageRate"]))
  count += 1


if args.pYear:
  for topic in topTopcis:
    for year, value in yearPapers.iteritems():
      index = dataDic[topic[0].upper()]["year"].index(year)
      if value != 0:
        dataDic[topic[0].upper()]["count"][index] /= (float(value)/100.0)


legendArray=[]
count = 0
for i in range(0,args.length):
   
  plt.plot(dataDic[topTrends[i][0]]["year"], dataDic[topTrends[i][0]]["count"]
  linewidth=1.2, marker=globalVar.MARKERS[count], markersize=10, 
  zorder=(len(topicList) - count), color=globalVar.COLORS[count],markeredgewidth=0.0)

  legendArray.append(dataDic[topTrends[i][0]]["name"])
  
  count += 1
  
  
'''
legendArray=[]
for topic in topTrends:
  #print("Key: %s, total: %s" % (topic[0].upper(), dataDic[topic[0].upper()]["total"]))
  #for j in range (0, len(dataDic[topic[0].upper()]["year"])):
  #  print("\t%s = %s" % ((dataDic[topic[0].upper()]["year"][j])
  #  , dataDic[topic[0].upper()]["count"][j]))
    

  plt.plot(topic[1]["year"], topic[1]["rate"], linewidth=2.0)
  
  legendArray.append(topic[1]["name"])
'''
  
plt.legend(legendArray, loc = 0)  
plt.xlabel("Publication year")
plt.ylabel("Number of documents")
if args.pYear:
  plt.ylabel("% of documents per year")

plt.show()



