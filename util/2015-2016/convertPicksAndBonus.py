#!/usr/bin/env python

import os
import sys
import numpy as np
import csv

# csvInFileName = "2014-2015 All Bowl Picks.csv"
csvInFileName = "bowlPicksOriginal.csv"
bowlPicksFileName = "bowlPicks.csv"
STPicksFileName = "bowlPicksSureThing.csv"
bonusPicksFileName = "bonusPicks.csv"

csvlines = file(csvInFileName).read().strip().split('\n')

bowlPicksOutfile = open(bowlPicksFileName,'w')
STPicksOutfile = open(STPicksFileName,'w')
bonusPicksOutfile = open(bonusPicksFileName,'w')

teams = []
for team in csvlines[0].split(','):
    bowlPicksOutfile.write("%s,"%team)
    STPicksOutfile.write("%s,"%team)
    bonusPicksOutfile.write("%s,"%team)
    teams.append(team)
bowlPicksOutfile.write('\n')
STPicksOutfile.write('\n')
bonusPicksOutfile.write('\n')

favoritesKey = ['U','TE','B','B','W','C','M','W','W','I','V','U','N',
                'M','C','B','C','L','A','M','L','U','F','O','A','T',
                'O','M','S','OM','G','A','O','W']

# FIXME: Also need to have a "dog key" here so that we can check the input to be
# sure that if a favorite wasn't picked, a dog was.  As it is right now my code
# will assume that if the favorite key isn't found, the dog was picked.  But it
# can be the case that there was an error in entry and the pick matches neither
# the fav nor the dog.  Need to check for this.

favoritesKeyLengths = [len(key) for key in favoritesKey]
nBowls = len(favoritesKey)

i = 0
for i,line in enumerate(csvlines[1:]):
        for pick in line.split(','):
            if i < nBowls:
                pick_info = [0,0,0]
                # jrd, 2015-12-29: this assumes favorite key length and dog key
                # length are the same, which has always been the case thus far.
                if pick[:favoritesKeyLengths[i]]==favoritesKey[i]:
                    pickedFav = True
                    pick_info[0] = 1
                    pick_info[1] = 0
                else:
                    pickedFav = False
                    pick_info[0] = 0
                    pick_info[1] = 1
                if len(pick) > favoritesKeyLengths[i] and pick[-1]=='S':
                    # print teams[i], pick, favoritesKey[i], len(pick), favoritesKeyLengths[i], pick[-1]
                    pickedSureThingBowl = True
                    pick_info[2] = 1
                bowlPicksOutfile.write('%s,'%(pick_info[0]))
                STPicksOutfile.write('%s,'%(pick_info[2]))
            else:
                bonusPicksOutfile.write('%s,'%pick)
        if i < nBowls:
            bowlPicksOutfile.write('\n')
            STPicksOutfile.write('\n')
        else:
            bonusPicksOutfile.write('\n')

bowlPicksOutfile.close()
STPicksOutfile.close()
bonusPicksOutfile.close()

