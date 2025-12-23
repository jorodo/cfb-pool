#!/usr/bin/env python
import os
import sys
import numpy as np

formResultsFileName = 'formResults.csv'
bowlResultsFileName = 'bowlResults.csv'

formResultsLines = file(formResultsFileName).read().strip().split('\n')
bowlResultsLines = file(bowlResultsFileName).read().strip().split('\n')
nBowls = len(bowlResultsLines)
nTeams = len(formResultsLines) - 1
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

# write the bowlPicks.csv file
bowlPicksFileName = 'bowlPicks.csv'
outfile = open(bowlPicksFileName,'w')
for i,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
    outfile.write(teamName+',')
outfile.write(sortedNames[len(sortedNames)-1]+'\n')
for i in range(nBowls):
    for j,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
        outfile.write('%s'%bowlPicksDict[teamName][i]+',')
    outfile.write('%s'%bowlPicksDict[sortedNames[len(sortedNames)-1]][i]+'\n')
outfile.close()

# load sure thing picks
sureThing1Idx = 3
sureThing2Idx = sureThing1Idx + 1
sureThing3Idx = sureThing1Idx + 2

sureThingFileName = 'formResultsSureThing.csv'
sureThingLines = file(sureThingFileName).read().strip().split('\n')

sureThingPicksDict = bowlPicksDict.copy()

for key in sureThingPicksDict.keys():
    for i in range(nBowls):
        sureThingPicksDict[key][i] = 0

for i,line in enumerate(sureThingLines[1:]):
    data = line.split(',')
    teamName = data[teamNameIdx]
    stpick1 = data[sureThing1Idx]
    try: st1bowlidx = favsList.index(stpick1)
    except: st1bowlidx = dogsList.index(stpick1)
    sureThingPicksDict[teamName][st1bowlidx] = 1
    stpick2 = data[sureThing2Idx]
    try: st2bowlidx = favsList.index(stpick2)
    except: st2bowlidx = dogsList.index(stpick2)
    sureThingPicksDict[teamName][st2bowlidx] = 1
    stpick3 = data[sureThing3Idx]
    try: st3bowlidx = favsList.index(stpick3)
    except: st3bowlidx = dogsList.index(stpick3)
    sureThingPicksDict[teamName][st3bowlidx] = 1

# write the bowlPicksSureThing.csv file
bowlPicksSureThingFileName = 'bowlPicksSureThing.csv'
outfile = open(bowlPicksSureThingFileName,'w')
for i,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
    outfile.write(teamName+',')
outfile.write(sortedNames[len(sortedNames)-1]+'\n')
for i in range(nBowls):
    for j,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
        outfile.write('%s'%sureThingPicksDict[teamName][i]+',')
    outfile.write('%s'%sureThingPicksDict[sortedNames[len(sortedNames)-1]][i]+'\n')
outfile.close()

# bonus questions
bonusFileName = 'formResultsBonus.csv'
bonusLines = file(bonusFileName).read().strip().split('\n')
bonusPicksDict = {}
bonusQuestionList = []
nBonusQuestions = 5
for i,teamName in enumerate(sortedNames): bonusPicksDict[teamName] = ['None' for i in range(nBonusQuestions)]
firstQuestionIdx = 3
for i,line in enumerate(bonusLines):
    data = line.split(',')[:firstQuestionIdx+nBonusQuestions]
    if i==0:
        [bonusQuestionList.append(question) for question in data[firstQuestionIdx:]]
        continue
    teamName = data[teamNameIdx]
    for j,answer in enumerate(data[firstQuestionIdx:]):
#        print(bonusPicksDict[teamName])
#        print(j)
        sys.stdout.flush()
        bonusPicksDict[teamName][j] = answer
    
# write the bonusPicks.csv file
bonusPicksFileName = 'bonusPicks.csv'
outfile = open(bonusPicksFileName,'w')
for i,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
    outfile.write(teamName+',')
outfile.write(sortedNames[len(sortedNames)-1]+'\n')
for i in range(nBonusQuestions):
    for j,teamName in enumerate(sortedNames[:len(sortedNames)-1]):
        outfile.write('%s'%bonusPicksDict[teamName][i]+',')
    outfile.write('%s'%bonusPicksDict[sortedNames[len(sortedNames)-1]][i]+'\n')
outfile.close()



