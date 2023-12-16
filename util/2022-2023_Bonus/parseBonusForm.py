#!/usr/bin/env python
import os
import sys
import numpy as np

formFileName = '2022-2023_National_Championship_Bonus_Round.csv'
bowlResultsFileName = 'bowlResults.csv'

formResultsLines = file(formFileName).read().strip().split('\n')
bowlResultsLines = file(bowlResultsFileName).read().strip().split('\n')

nBowls = 1
nTeams = 10
teamNameIdx = 2
firstBowlIdx = 3

bowlNameIdx = 1
lineIdx = 2
favIdx = 3
dogIdx = 4

# build list of bowls, favs, and dogs
bowlNameList = []
favsList = []
dogsList = []
for j,line in enumerate(bowlResultsLines):
    data = line.split(',')
    bowlNameList.append(data[bowlNameIdx])
    favsList.append(data[favIdx])
    dogsList.append(data[dogIdx])

# build the dictionary of picks
bowlPicksDict = {}
for i,line in enumerate(formResultsLines[1:]):
    data = line.split(',')
    teamName = data[teamNameIdx]
    bowlPicksDict[teamName] = []
    for j,pick in enumerate(data[firstBowlIdx:firstBowlIdx+nBowls]):
        if pick in favsList[j]: bowlPicksDict[teamName].append(1)
        elif pick in dogsList[j]: bowlPicksDict[teamName].append(0)
        else:
            sys.stderr.write('error: did not recognize pick.')
            sys.exit()

# created a sorted list of team names
sortedNames = sorted(bowlPicksDict.keys(), key=lambda x:x.lower())

## write the bowlPicks.csv file
#bowlPicksFileName = 'bowlPicks.csv'
#outfile = open(bowlPicksFileName,'w')
#for i,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
#    outfile.write(teamName+',')
#outfile.write(sortedNames[len(sortedNames)-1]+'\n')
#for i in range(nBowls):
#    for j,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
#        outfile.write('%s'%bowlPicksDict[teamName][i]+',')
#    outfile.write('%s'%bowlPicksDict[sortedNames[len(sortedNames)-1]][i]+'\n')
#outfile.close()

# bonus questions
bonusLines = formResultsLines
bonusPicksDict = {}
for i,teamName in enumerate(sortedNames): bonusPicksDict[teamName] = []
bonusQuestionList = []
firstQuestionIdx = 4

for i,line in enumerate(bonusLines):
    data = line.split(',')
    if i==0:
        [bonusQuestionList.append(question) for question in data[firstQuestionIdx:]]
        continue
    teamName = data[teamNameIdx]
    [bonusPicksDict[teamName].append(answer) for answer in data[firstQuestionIdx:]]
    
# write the bonusPicks.csv file
bonusPicksFileName = 'bonusPicks.csv'
outfile = open(bonusPicksFileName,'w')
for i,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
    outfile.write(teamName+',')
outfile.write(sortedNames[len(sortedNames)-1]+'\n')
nBonus = 7
for i in range(nBonus):
    for j,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
        outfile.write('%s'%bonusPicksDict[teamName][i]+',')
    outfile.write('%s'%bonusPicksDict[sortedNames[len(sortedNames)-1]][i]+'\n')
outfile.close()



