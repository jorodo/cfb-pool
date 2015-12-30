#!/usr/bin/env python

import os
import sys
import numpy as np
import datetime
import csv
from operator import itemgetter, attrgetter
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import fitz.misc

class BowlPool():
    """
    Base class for organizing the Bowl Pool info and results.

    """

    def __init__(self, input_dir, output_dir, highlightList=[],
                 bowlResultsFileName='bowlResults.csv',
                 bowlPicksFileName='bowlPicks.csv',
                 STPicksFileName='bowlPicksSureThing.csv',
                 bonusResultsFileName='bonusResults.csv',
                 bonusPicksFileName='bonusPicks.csv',
                 dogScoreFileName='dogScoreBonus.csv'):
        """Initialize the bowl pool object.

        """
        self._input_dir = input_dir
        self._output_dir = output_dir
        self._bowlResultsFileName = os.path.join(input_dir,bowlResultsFileName)
        self._bowlPicksFileName = os.path.join(input_dir,bowlPicksFileName)
        self._STPicksFileName = os.path.join(input_dir,STPicksFileName)
        self._bonusResultsFileName = os.path.join(input_dir,bonusResultsFileName)
        self._bonusPicksFileName = os.path.join(input_dir,bonusPicksFileName)
        self._dogScoreFileName = os.path.join(input_dir,dogScoreFileName)
        self._highlightList = highlightList
        self._nBowls = None
        self._nBonus = None
        self._nTeams = None
        self._nResults = 0
        self._nBonusResults = 0
        self._teamList = []
        self._favPointsList = []
        self._favList = []
        self._dogList = []
        self._bowlList = []
        self._spreadList = []
        self._bonusList = []
        self._bonusPointsList = []
        self._bonusIDList = []
        self._resultsList = []
        self._rankingsList = []
        self._resultsVector = None
        self._bonusResultsList = []
        self._resultsArray = None
        self._picksArray = None
        self._bonusPicksArray = None
        self._dogScoreArray = None
        self._favWinsArray = None
        self._dogWinsArray = None
        self._winsArray = None
        self._stbArray = None
        self._favPointsArray = None
        self._dogPointsArray = None
        self._pointsArray = None
        self._scoreArray = None
        self._bonusScoreArray = None
        self._scoreTotals = None
        self._sortedScoresList = []
        self._parseResultsFile()
        self._parseBonusFile()
        self._parseBowlPicksFile()
        self._parseSTPicksFile()
        self._parseBonusPicksFile()
        self._parseDogScoreFile()

    # ---- file parsing -------------------------------------------------

    def _parseResultsFile(self):
        """Load the bowl info and results from the text file."""
        lines = file(self._bowlResultsFileName).read().strip().split('\n')
        self._nBowls = len(lines)
        self._resultsVector = -1.*np.ones(self._nBowls)
        for i,line in enumerate(lines):
            line_data = line.split(',')
            self._bowlList.append(line_data[1])
            self._spreadList.append(float(line_data[2]))
            self._favList.append(line_data[3])
            self._dogList.append(line_data[4])
            self._favPointsList.append(float(line_data[5]))
            favWon = line_data[6]
            self._resultsList.append(int(favWon))
            self._resultsVector[i] = float(favWon)
            if float(favWon) >= 0: self._nResults += 1

    def _parseBowlPicksFile(self):
        lines = file(self._bowlPicksFileName).read().strip().split('\n')
        for team in lines[0].split(','):
            if team != '': self._teamList.append(team)
        self._nTeams = len(self._teamList)
        self._picksArray = np.zeros((self._nBowls, self._nTeams))

        for i,line in enumerate(lines[1:]):
            line_data = line.split(',')[:self._nTeams]
            for j,pick in enumerate(line_data):  # FIXME: don't let csv line end in ','
                self._picksArray[i,j] = float(pick)

    def _parseSTPicksFile(self):
        lines = file(self._STPicksFileName).read().strip().split('\n')
        self._stbArray = np.zeros((self._nBowls, self._nTeams))

        for i, line in enumerate(lines[1:]):
            line_data = line.split(',')[:self._nTeams]
            for j, pick in enumerate(line_data):  # FIXME: don't let csv line end in ','
                self._stbArray[i,j] = float(pick)

    def _parseBonusFile(self):
        """Load the bonus info the text file."""
        lines = file(self._bonusResultsFileName).read().strip().split('\n')
        self._nBonus = len(lines)
        for i,line in enumerate(lines):
            line_data = line.split(',')
            self._bonusIDList.append(line_data[0])
            self._bonusList.append(line_data[1])
            self._bonusPointsList.append(float(line_data[2]))
            bonusResult = line_data[3].strip()
            self._bonusResultsList.append(bonusResult)
            if bonusResult != 'None': self._nBonusResults += 1

    def _parseBonusPicksFile(self):
        lines = file(self._bonusPicksFileName).read().strip().split('\n')
        self._bonusPicksArray = []
        
        for i, line in enumerate(lines[1:]):
            line_data = line.split(',')[:self._nTeams]
            # # DEBUG
            # print line_data
            # print len(line_data)
            # print self._nTeams
            # print self._nBonus
            # sys.exit()
            # # END DEBUG
            self._bonusPicksArray.append([])
            for j, pick in enumerate(line_data):   # FIXME: don't let csv line end in ','
                # # --- debug (FIXME: trying to find invalid entries here.)
                # if i > 0 and pick != 'Y' and pick != 'N':
                #     teamName = self._teamList[j]
                #     print '%s picked %s for: %s'%(teamName, pick, self._bonusList[i])
                #     # if pick == 'T': pick = 'Y'
                # # --- end debug
                self._bonusPicksArray[i].append(pick)

    def _parseDogScoreFile(self):
        lines = file(self._dogScoreFileName).read().strip().split('\n')
        self._dogScoreArray = np.zeros((len(lines),3))
        
        for i, line in enumerate(lines):
            line_data = line.split(',')
            for j, value in enumerate(line_data):
                self._dogScoreArray[i,j] = float(value)

    # ---- end file parsing ---------------------------------------------

    # ---- calculate results of bowl pool -------------------------------

    def computeResults(self):
        """
        Compute the scores for each team in each bowl and store the result
        in the score matrix.


        """
        self._loadArrays()
        self._scoreArray = self._winsArray*(self._pointsArray + self._stbArray)
        self._loadBonusScoreArray()
        self._scoreTotals = self._scoreArray[:self._nResults].sum(axis=0) \
                            + self._bonusScoreArray[:self._nBonusResults].sum(axis=0)
        self._rankTeams()

    def _loadArrays(self):
        """
        Load the arrays needed for computing the score total.

        """
        self._resultsArray = np.array([self._resultsVector,]*self._nTeams).transpose()
        self._favWinsArray = np.zeros(self._resultsArray.shape)
        self._dogWinsArray = np.zeros(self._resultsArray.shape)
        self._winsArray = np.zeros(self._resultsArray.shape)
        self._favPointsArray = np.zeros(self._resultsArray.shape)
        self._dogPointsArray = np.zeros(self._resultsArray.shape)
        self._pointsArray = np.zeros(self._resultsArray.shape)
        self._favPointsArray = np.array([np.array(self._favPointsList),]*self._nTeams).transpose()
        self._dogPointsList = [self._scoreBowl(i, (0,0), False) for i in xrange(self._nBowls)]
        self._dogPointsArray = np.array([np.array(self._dogPointsList),]*self._nTeams).transpose()
        self._pointsArray = self._resultsArray*self._favPointsArray \
                             + (1-self._resultsArray)*self._dogPointsArray
        self._favWinsArray = self._resultsArray * self._picksArray
        self._dogWinsArray = (1.-self._resultsArray)*(1.-self._picksArray)
        self._winsArray = self._favWinsArray + self._dogWinsArray
        
    def _rankTeams(self):
        results_list = []
        for j in xrange(self._nTeams):
            teamName = self._teamList[j]
            results_list.append((teamName,self._scoreTotals[j]))

        self._sortedScoresList = sorted(results_list, key=itemgetter(1))
        self._sortedScoresList.reverse()
        rank = 1
        pvsScore = 0.
        self._rankingsList = [None for i in xrange(self._nTeams)]
        for i in xrange(self._nTeams):
            teamName = self._sortedScoresList[i][0]
            teamIndex = self._getTeamIndex(teamName)
            score = self._sortedScoresList[i][1]
            if i > 0:
                if score < pvsScore: rank = i+1
            self._rankingsList[teamIndex] = rank
            pvsScore = score

    def _getTrajectories(self, pointsTrajectories, rankingsTrajectories):
        nResults = self._nResults
        for i in xrange(1, self._nResults + 1):
            self._nResults = i
            self.computeResults()
            pointsTrajectories[i-1,:] = self._scoreTotals.copy()
            for j in xrange(self._nTeams):
                teamName = self._sortedScoresList[j][0]
                teamIndex = self._getTeamIndex(teamName)
                rank = self._rankingsList[teamIndex]
                rankingsTrajectories[i-1,teamIndex] = rank
        self._nResults = nResults
                
    def _scoreBowl(self, bowlID, pick, favWon=None):
        """
        Return the points won for the given bowl.  Scoring function
        just follows the rules of the bowl pool.


        """
        if favWon==None: favWon = self._resultsList[bowlID]
        dogWon = not favWon
        points = 0.
        if favWon < 0: return 0.

        # the pick is whether or not the favorite won, given by pick[0]
        if favWon and pick[0]==1:
            favPoints = self._favPointsList[bowlID]
            points += favPoints
            # sure thing bowl
            if pick[1]==1: points += 1.
        elif dogWon and pick[0]==0:
            dogPoints = self._getDogPoints(bowlID)
            points += dogPoints
            # sure thing bowl
            if pick[1]==1: points += 1.

        return points

    def _getDogPoints(self,bowlID):
        """
        Return the bonus points for guessing a dog right.

        """
        spread = self._spreadList[bowlID]
        favPoints = self._favPointsList[bowlID]
        dogPoints = None
        for i in xrange(len(self._dogScoreArray)):
            lowerBound = self._dogScoreArray[i,0]
            upperBound = self._dogScoreArray[i,1]
            bonusFactor = self._dogScoreArray[i,2]
            if spread >= lowerBound and spread < upperBound:
                dogPoints = bonusFactor*favPoints
                
        if dogPoints == None:
            sys.stdout.write('error: could not assign dogPoints')
            sys.exit()

        return dogPoints

    def _loadBonusScoreArray(self):
        self._bonusScoreArray = np.zeros((self._nBonus, self._nTeams))
        for i in xrange(self._nBonus):
            bonusResult = self._bonusResultsList[i]
            for j in xrange(self._nTeams):
                if self._bonusPicksArray[i][j] == self._bonusResultsList[i]:
                    self._bonusScoreArray[i][j] = self._bonusPointsList[i]

        return

    # ---- end calculate results ---------------------------------------

    # ---- file I/O ----------------------------------------------------

    def writeScoreTotals(self, printScoreTotals=False):
        outfilename=os.path.join(self._output_dir, 'rankings.txt')
        fmt = "%Y-%m-%d %H:%M:%S"
        lastBowlIdx = self._nResults - 1
        today = datetime.datetime.today()
        fout = open(outfilename,'w')
        # fout.write('| *Last updated:  %s %s*\n'%(today.strftime(fmt), ' CST'))
        fout.write('| *Last updated:  %s*\n'%today.strftime(fmt))
        fout.write('| *Last bowl scored:  %s (%s vs. %s)*\n\n'%(self._bowlList[lastBowlIdx],
                                                                self._favList[lastBowlIdx],
                                                                self._dogList[lastBowlIdx]))
        for i in xrange(self._nTeams):
            teamName = self._sortedScoresList[i][0]
            score = self._sortedScoresList[i][1]
            teamIndex = self._getTeamIndex(teamName)
            rank = self._rankingsList[teamIndex]
            if printScoreTotals: print '%s. %s %s'%(rank, teamName, score)
            if teamName in self._highlightList:
                fout.write('| %s. **%s %s**\n'%(rank, teamName, score))
            else:
                fout.write('| %s. %s %s\n'%(rank, teamName, score))
        fout.close()

    def writeScoreTotalsCSVFile(self):
        outfilename=os.path.join(self._output_dir, 'rankings.csv')
        fmt = "%Y-%m-%d %H:%M:%S"
        lastBowlIdx = self._nResults - 1
        today = datetime.datetime.today()
        fout = open(outfilename,'w')
        # fout.write('| *Last updated:  %s %s*\n'%(today.strftime(fmt), ' CST'))
        fout.write('Last updated:  %s\n'%today.strftime(fmt))
        fout.write('Last bowl scored:  %s (%s vs. %s)\n\n'%(self._bowlList[lastBowlIdx],
                                                            self._favList[lastBowlIdx],
                                                            self._dogList[lastBowlIdx]))
        for i in xrange(self._nTeams):
            teamName = self._sortedScoresList[i][0]
            score = self._sortedScoresList[i][1]
            teamIndex = self._getTeamIndex(teamName)
            rank = self._rankingsList[teamIndex]
            fout.write('%s,%s,%s\n'%(rank, teamName, score))
        fout.close()

    def writePicksTable(self):
        outfilename=os.path.join(self._output_dir, 'picks.txt')
        emptyCell = ' '
        headerString = '"ID", "Bowl Name", "Favorite", "Underdog", "Spread"'
        picksMap = {}
        for j in xrange(self._nTeams):
            picksMap[j] = []
            for i in xrange(self._nBowls):
                if int(round(self._picksArray[i][j])):
                    pick = self._favList[i]
                else:
                    pick = self._dogList[i]
                picksMap[j].append(pick)
            headerString += ', %s'%self._teamList[j]
        fout = open(outfilename, 'w')
        fout.write('.. csv-table:: \n')
        fout.write('   :header: %s\n'%headerString)
        fout.write('\n')
        for i in xrange(self._nBowls):
            fout.write('   "%s", "%s", "%s", "%s", "%s"'%(i+1, self._bowlList[i],
                                                          self._favList[i],
                                                          self._dogList[i],
                                                          self._spreadList[i]))
            for j in xrange(self._nTeams):
                if self._stbArray[i][j]:
                    pick = picksMap[j][i] + '\ :sup:`*`'
                else:
                    pick = picksMap[j][i]
                fout.write(', "%s"'%pick)
            fout.write('\n')

        for i in xrange(self._nBonus):
            fout.write('   "%s", "%s", "%s", "%s", "%s"'%(self._bonusIDList[i], self._bonusList[i],
                                                          emptyCell, emptyCell, emptyCell))
            for j in xrange(self._nTeams):
                fout.write(', "%s"'%self._bonusPicksArray[i][j])
            fout.write('\n')
            
        fout.write('\n')
        fout.write('\* *Denotes sure thing bowl*\n')
        fout.write('\n')
        fout.close()

    def writePicksCSVFile(self):
        outfilename=os.path.join(self._output_dir, 'picks.csv')
        emptyCell = ' '
        headerString = '#,Bowl Name,Favorite,Underdog,Spread'
        picksMap = {}
        for j in xrange(self._nTeams):
            picksMap[j] = []
            for i in xrange(self._nBowls):
                if int(round(self._picksArray[i][j])):
                    pick = self._favList[i]
                else:
                    pick = self._dogList[i]
                picksMap[j].append(pick)
            headerString += ',%s'%self._teamList[j]
        fout = open(outfilename, 'w')
        fout.write('%s\n'%headerString)
        fout.write('\n')
        for i in xrange(self._nBowls):
            fout.write('%s,%s,%s,%s,%s'%(i+1, self._bowlList[i],
                                         self._favList[i],
                                         self._dogList[i],
                                         self._spreadList[i]))
            for j in xrange(self._nTeams):
                if self._stbArray[i][j]:
                    pick = picksMap[j][i] + '*'
                else:
                    pick = picksMap[j][i]
                fout.write(',%s'%pick)
            fout.write('\n')

        for i in xrange(self._nBonus):
            fout.write('%s,%s,%s,%s,%s'%(self._bonusIDList[i], self._bonusList[i],
                                         emptyCell, emptyCell, emptyCell))
            for j in xrange(self._nTeams):
                fout.write(',%s'%self._bonusPicksArray[i][j])
            fout.write('\n')
            
        fout.write('\n')
        fout.close()

    def writeResultsTable(self):
        outfilename=os.path.join(self._output_dir, 'results.txt')
        emptyCell = ' '
        headerString = '"ID", "Bowl Name", "Favorite", "Underdog", "Spread"'
        for j in xrange(self._nTeams):
            headerString += ', %s'%self._teamList[j]
        fout = open(outfilename, 'w')
        fout.write('.. csv-table:: \n')
        fout.write('   :header: %s\n'%headerString)
        fout.write('\n')
        for i in xrange(self._nResults):
            fout.write('   "%s", "%s", "%s", "%s", "%s"'%(i+1, self._bowlList[i],
                                                          self._favList[i],
                                                          self._dogList[i],
                                                          self._spreadList[i]))
            for j in xrange(self._nTeams):
                fout.write(', "%s"'%self._scoreArray[i][j])
            fout.write('\n')

        for i in xrange(self._nBonus):
            fout.write('   "%s", "%s", "%s", "%s", "%s"'%(self._bonusIDList[i], self._bonusList[i],
                                                          emptyCell, emptyCell, emptyCell))
            for j in xrange(self._nTeams):
                fout.write(', "%s"'%self._bonusScoreArray[i][j])
            fout.write('\n')
            
        fout.write('   "%s", "%s", "%s", "%s", "%s"'%('**Totals**', emptyCell,
                                                      emptyCell,
                                                      emptyCell,
                                                      emptyCell))
        for j in xrange(self._nTeams):
            fout.write(', "**%s**"'%self._scoreTotals[j])
        fout.write('\n')
        
        fout.close()

    def writeResultsCSVFile(self):
        outfilename=os.path.join(self._output_dir, 'results.csv')
        emptyCell = ' '
        headerString = '#,Bowl Name,Favorite,Underdog,Spread'
        for j in xrange(self._nTeams):
            headerString += ',%s'%self._teamList[j]
        fout = open(outfilename, 'w')
        fout.write('%s\n'%headerString)
        for i in xrange(self._nResults):
            fout.write('%s,%s,%s,%s,%s'%(i+1, self._bowlList[i],
                                         self._favList[i],
                                         self._dogList[i],
                                         self._spreadList[i]))
            for j in xrange(self._nTeams):
                fout.write(',%s'%self._scoreArray[i][j])
            fout.write('\n')
    
        for i in xrange(self._nBonus):
            fout.write('%s,%s,%s,%s,%s'%(self._bonusIDList[i], self._bonusList[i],
                                         emptyCell, emptyCell, emptyCell))
            for j in xrange(self._nTeams):
                fout.write(',%s'%self._bonusScoreArray[i][j])
            fout.write('\n')
            
        fout.write('%s,%s,%s,%s,%s'%('Totals', emptyCell,
                                     emptyCell,
                                     emptyCell,
                                     emptyCell))
        for j in xrange(self._nTeams):
            fout.write(',%s'%self._scoreTotals[j])
        fout.write('\n')
        
        fout.close()

    # ---- end file I/O ------------------------------------------------

    # ---- utilities ---------------------------------------------------
    
    def _getTeamIndex(self, teamName):
        return self._teamList.index(teamName)

    def listBowlData(self):
        """Print out all the bowl info.

        """
        print 'ID, Name, Spread, Favorite, Dog, Result'
        print '~'*40
        for i in xrange(self._nBowls):
            print i, self._bowlList[i], self._spreadList[i], self._favList[i], \
                self._dogList[i], self._resultsList[i]

    def printPicks(self, teamName, printResults=True):
        """
        Print the picks for a given team.

        """
        j = self._getTeamIndex(teamName)

        nameStr = teamName
        if printResults: nameStr += '  (%s)'%self._scoreTotals[j]
        print nameStr
        print '~'*20

        for i in xrange(self._nBowls):
            teamstr = ''
            if int(round(self._picksArray[i][j])):
                teamstr += '(STB) ' if int(round(self._stbArray[i][j])) else ''
                teamstr += self._favList[i]
            else:
                teamstr += '(STB) ' if int(round(self._stbArray[i][j])) else ''
                teamstr += self._dogList[i]
            if self._resultsVector[i] >=0 and printResults:
                teamstr += '  (%s)'%str(self._scoreArray[i][j])
            print '%s.'%i, teamstr

        for i in xrange(self._nBonus):
            bonusstr = '%s %s'%(self._bonusList[i],
                                self._bonusPicksArray[i][j])
            if self._bonusResultsList[i] != 'None' and printResults:
                bonusstr += '  (%s)'%str(self._bonusScoreArray[i][j])
            print 'B%s.'%i, bonusstr

    def checkSTBowls(self):
        """
        Print out any teams that don't have three sure thing bowls.

        """
        stbSums = self._stbArray.sum(axis=0)
        if (stbSums != 3.0).any():
            print 'The following teams do not have 3 sure thing bowls:'
            for i in np.where(stbSums != 3.0)[0]:
                print i, self._teamList[i], stbSums[i]

    # ---- end utilities -------------------------------------------------

    # ---- plots and analysis -------------------------------------------------

    def plotScoresHistogram(self, nbins=30):
        """
        Plot the distribution of team scores.

        """
        # TODO:  add points and for a list of teams
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(self._scoreTotals,bins=nbins)
        ax.set_xlabel('Total Points')
        ax.set_ylabel('Number of Teams')
        fig.savefig(os.path.join(self._output_dir,'scoresHistogram.png'))

    def plotTrajectories(self, teamList=[]):
        """
        Plot the trajectory of teams' points and rankings over the bowl games.
    
        """
                
        pointsTrajectories = np.zeros((self._nResults, self._nTeams))
        rankingsTrajectories = np.zeros((self._nResults, self._nTeams))
        self._getTrajectories(pointsTrajectories, rankingsTrajectories)

        teamIndexes = [self._getTeamIndex(x) for x in teamList]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.arange(self._nResults)
        for index in teamIndexes:
            ax.plot(x, pointsTrajectories[:,index])
        ax.set_xlabel('Bowl Game Number')
        ax.set_ylabel('Total Points')
        fig.savefig(os.path.join(self._output_dir,'pointsTrajectories.png'))
        fig.clf()
    
        # TODO:  add labels and stuff to these plots
    
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.arange(self._nResults)
        for i, index in enumerate(teamIndexes):
            teamName = teamList[i]
            ax.plot(x, rankingsTrajectories[:,index])
        ax.set_xlabel('Bowl Game Number')
        ax.set_ylabel('Ranking')
        fig.gca().invert_yaxis()
        fig.savefig(os.path.join(self._output_dir,'rankingsTrajectories.png'))
        fig.clf()
    
    # ---- end plots and analysis ---------------------------------------------

    
if __name__ == "__main__":

    input_dir = 'input/2014-2015'
    bowlPoolName = '2014-2015'
    srvdir = 'srv/test'
    output_dir = os.path.join(srvdir, bowlPoolName)
    highlightList = ['#Mama Bear', 'Admiral Akbar', 'A Real Quandre', 'Coin Toss',
                     'D-Bo', 'Eclipse', 'Gigi-Dawg', 'Mr. Gamblerer', 'Mrs. Gamblerer',
                     'Panda Bear', 'Mimi']
    B = BowlPool(input_dir, output_dir, highlightList)
    # B = BowlPool(input_dir, output_dir)
    B.computeResults()
    # B.writePicksTable()
    # B.writePicksCSVFile()
    # B.writeResultsTable()
    # B.writeResultsCSVFile()
    # B.writeScoreTotalsCSVFile()
    # B.plotTrajectories(highlightList)
    # B.listBowlData()
    B.printPicks('#blamejameis')
    # nbins = 10
    # B.plotScoresHistogram(nbins)
    B.checkSTBowls()

