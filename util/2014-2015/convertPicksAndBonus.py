#!/usr/bin/env python

import os
import sys
import numpy as np
import csv

# csvInFileName = "2014-2015 All Bowl Picks.csv"
csvInFileName = "bowlPicksOriginal.csv"
bowlPicksFileName = "bowlPicks.csv"
STPicksFileName = "STPicks.csv"
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

favoritesKey = ['M','S','W','R','L','N','U','C','A','M','B','U','W',
                'O','A','L','G','S','T','A','M','A','B','MO','O','A',
                'P','T','U','W','F','T']
favoritesKeyLengths = [len(key) for key in favoritesKey]
nBowls = len(favoritesKey)

i = 0
for i,line in enumerate(csvlines[1:]):
        for pick in line.split(','):
            if i < nBowls:
                pick_info = [0,0,0]
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

