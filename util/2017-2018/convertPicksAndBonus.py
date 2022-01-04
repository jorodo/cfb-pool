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

nBowls = 39

i = 0
for i,line in enumerate(csvlines[1:]):
        for j,pick in enumerate(line.split(',')):
            if i < nBowls:
                pick_info = [0,0,0]
                if pick == 'F':
                    pickedFav = True
                    pick_info[0] = 1
                    pick_info[1] = 0
                elif pick == 'FS':
                    pickedFav = True
                    pick_info[0] = 1
                    pick_info[1] = 0
                    pickedSureThingBowl = True
                    pick_info[2] = 1
                elif pick == 'U':
                    pickedFav = False
                    pick_info[0] = 0
                    pick_info[1] = 1
                elif pick == 'US':
                    pickedFav = False
                    pick_info[0] = 0
                    pick_info[1] = 1
                    pickedSureThingBowl = True
                    pick_info[2] = 1
                else:
                    # FIXME.  This is still kind of a hack.  Need to do more
                    # thorough error checking here.  Or better yet, automate
                    # the pick process using a web form so I don't have to deal
                    # with this s***!
                    print 'error: %s - pick %s does not match fav or dog.'%(teams[j], pick)
                    print '    guessing favorite.'
                    pickedFav = True
                    pick_info[0] = 1
                    pick_info[1] = 0
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

