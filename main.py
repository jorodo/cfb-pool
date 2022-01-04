#!/usr/bin/env python

import os
import sys
import bowl_pool
import datetime
from optparse import OptionParser

# bowlResultsFileName = "input/bowlResults.csv"
# bowlPicksFileName = "input/bowlPicks.csv"
# STPicksFileName = "input/STPicks.csv"
# bonusResultsFileName = "input/bonusResults.csv"
# bonusPicksFileName = "input/bonusPicks.csv"
# dogScoreBonusFileName = "input/dogScoreBonus.csv"

parser = OptionParser()
parser.set_defaults(srvdir='srv')
parser.add_option('-d', dest='srvdir')
(options, args) = parser.parse_args()
srvdir = options.srvdir

if not os.path.isdir(srvdir):
    os.mkdir(srvdir)
mainfile = os.path.join(srvdir, 'index.txt')
main_fout = open(mainfile,'w')
main_fout.write('**Bowl Pools**\n')
main_fout.write('\n')

BowlPoolList = ['2014-2015','2015-2016','2016-2017', '2017-2018','2021-2022']
CompletedBowlPools = ['2014-2015','2015-2016', '2016-2017', '2017-2018']
#highlightList = ['Nerf Herder','Static', 'Lightning', 'Thunder',
#                 'D-Bo','Em214', 'GlamKam', 'Bumblerooski', '#MamaBear',
#                 'Eclipse']
#highlightList = ['Bumblerooski', "Can't Stop a Badger!", "Knights of Ren",
#                 "Leeerroyyy Jeennkinns!!", "Ms. Snuffleupagus", "Sweet Lou"]
highlightList = []
performAnalysis = True
#performAnalysis = False

for bowlPoolName in BowlPoolList:
    main_fout.write('- `%s <%s/>`_'%(bowlPoolName, bowlPoolName))

    if bowlPoolName in CompletedBowlPools:
        main_fout.write('\n')
        continue

    # setup bowl pool object
    input_dir = os.path.join('input/', bowlPoolName)
    if not os.path.isdir(input_dir):
        sys.stdout.write('error: could not find input directory, %s'%input_dir)
        sys.exit()
    output_dir = os.path.join(srvdir, bowlPoolName)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    nbins = 20
    B = bowl_pool.BowlPool(input_dir, output_dir, highlightList)
    
    # run bowl pool
    B.computeResults()
    B.writeScoreTotals()
    B.writeScoreTotalsCSVFile()
    B.writePicksTable()
    B.writePicksCSVFile()
    B.writeResultsTable()
    B.writeResultsCSVFile()
    
    # analyze results
    if performAnalysis:
        B.plotScoresHistogram(nbins)
        B.plotTrajectories(highlightList)
    
    # # print info and debug
    # B.listBowlData()
    for highlightedName in highlightList:
        B.printPicks(highlightedName)
    B.checkSTBowls()

    bp_index_path = os.path.join(output_dir,'index')
    bp_fout = open(bp_index_path + '.txt', 'w')
    bp_fout.write('**%s Bowl Pool**\n'%bowlPoolName)
    bp_fout.write('\n')
    fmt = "%Y-%m-%d %H:%M:%S"
    lastBowlIdx = B._nResults - 1
    today = datetime.datetime.today()
    bp_fout.write('| *Last updated:  %s*\n'%today.strftime(fmt))
    bp_fout.write('| *Last bowl scored:  %s (%s vs. %s)*\n\n'%(B._bowlList[lastBowlIdx],
                                                               B._favList[lastBowlIdx],
                                                               B._dogList[lastBowlIdx]))
    bp_fout.write('\n')
    bp_fout.write('- `Rankings <rankings.html>`_ (`csv <rankings.csv>`__)\n')
    bp_fout.write('- `Results <results.html>`_ (`csv <results.csv>`__)\n')
    bp_fout.write('- `Picks <picks.html>`_ (`csv <picks.csv>`__)\n')
    # bp_fout.write('- Rankings (`csv <rankings.csv>`__ | `html <rankings.html>`__)\n')
    # bp_fout.write('- Results (`csv <results.csv>`__ | `html <results.html>`__)\n')
    # bp_fout.write('- Picks (`csv <picks.csv>`__ | `html <picks.html>`__)\n')
    bp_fout.write('\n')
    if performAnalysis:
        bp_fout.write('Analysis\n')
        bp_fout.write('\n')
        bp_fout.write('- `Score distribution <scoresHistogram.png>`_\n')
        bp_fout.write('- `Points Trajectories <pointsTrajectories.png>`_\n')
        bp_fout.write('- `Rankings Trajectories <rankingsTrajectories.png>`_\n')
        bp_fout.write('\n')
    bp_fout.close()

    os.system('rst2html %s.txt %s.html'%(bp_index_path, bp_index_path))

    rankings_path = os.path.join(output_dir, 'rankings')
    os.system('rst2html %s.txt %s.html'%(rankings_path, rankings_path))
    results_path = os.path.join(output_dir, 'results')
    os.system('rst2html %s.txt %s.html'%(results_path, results_path))
    picks_path = os.path.join(output_dir, 'picks')
    os.system('rst2html %s.txt %s.html'%(picks_path, picks_path))

main_fout.write('\n')
main_fout.close()
