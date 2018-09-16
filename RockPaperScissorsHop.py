#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:32:54 2018

@author: firman.taylor
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio

""" Game Conditions """

numHoops = 8
leftWinProb = 1.0/3.0
rightWinProb = 1.0/3.0
hopTime = 1
rpsTime = 1

""" Analytical Method """
""" Continues calculation until 99.9% of probability has completed """

probs = [1.0]
leftPositions = [-1 + np.floor((numHoops + 1)/2)]
rightPositions = [numHoops - np.floor((numHoops + 1)/2)]
totTimes = [np.floor((numHoops + 1)/2)*hopTime]
newProbs = []
newLeftPos = []
newRightPos = []
newTimes = []
while np.sum(np.array(probs)[np.any([np.array(leftPositions) == numHoops,np.array(rightPositions) == -1],axis=0)]) < 0.999:
    print('Prob Ended = ' + str(round(100*np.sum(np.array(probs)[np.any([np.array(leftPositions) == numHoops,np.array(rightPositions) == -1],axis=0)]),1)) + '%')
    pathInd1 = 0
    while pathInd1 < len(probs):
        sameInds = np.all([np.array(leftPositions) == leftPositions[pathInd1],\
        np.array(rightPositions) == rightPositions[pathInd1],np.array(totTimes) == totTimes[pathInd1]],axis=0)
        probs[pathInd1] = np.sum(np.array(probs)[sameInds])
        inds2keep = ~sameInds
        inds2keep[pathInd1] = True
        probs = np.array(probs)[inds2keep].tolist()
        leftPositions = np.array(leftPositions)[inds2keep].tolist()
        rightPositions = np.array(rightPositions)[inds2keep].tolist()
        totTimes = np.array(totTimes)[inds2keep].tolist()
        del inds2keep
        del sameInds
        pathInd1 += 1
    del pathInd1
    
    for pathInd in range(len(probs)):
        if leftPositions[pathInd] == numHoops or rightPositions[pathInd] == -1:
            newProbs.append(probs[pathInd])
            newLeftPos.append(leftPositions[pathInd])
            newRightPos.append(rightPositions[pathInd])
            newTimes.append(totTimes[pathInd])
            continue
        for outcome in range(3):
            if outcome == 0:
                newProbs.append(probs[pathInd]*(1 - leftWinProb - rightWinProb))
                newLeftPos.append(leftPositions[pathInd])
                newRightPos.append(rightPositions[pathInd])
                newTimes.append(totTimes[pathInd] + rpsTime)
            elif outcome == 1:
                newProbs.append(probs[pathInd]*leftWinProb)
                if leftPositions[pathInd] == numHoops - 1 and rightPositions[pathInd] == numHoops - 1:
                    newLeftPos.append(numHoops)
                    newRightPos.append(numHoops)
                    newTimes.append(totTimes[pathInd] + rpsTime + hopTime)
                else:
                    newLeftPos.append(leftPositions[pathInd] + np.floor((numHoops - leftPositions[pathInd])/2))
                    newRightPos.append(numHoops - np.floor((numHoops - leftPositions[pathInd])/2))
                    newTimes.append(totTimes[pathInd] + rpsTime + np.floor((numHoops - leftPositions[pathInd])/2)*hopTime)
            elif outcome == 2:
                newProbs.append(probs[pathInd]*rightWinProb)
                if leftPositions[pathInd] == 0 and rightPositions[pathInd] == 0:
                    newLeftPos.append(-1)
                    newRightPos.append(-1)
                    newTimes.append(totTimes[pathInd] + rpsTime + hopTime)
                else:
                    newLeftPos.append(-1 + np.floor((rightPositions[pathInd] + 1)/2))
                    newRightPos.append(rightPositions[pathInd] - np.floor((rightPositions[pathInd] + 1)/2))
                    newTimes.append(totTimes[pathInd] + rpsTime + np.floor((rightPositions[pathInd] + 1)/2)*hopTime)
        del outcome
    del pathInd
    probs = newProbs
    leftPositions = newLeftPos
    rightPositions = newRightPos
    totTimes = newTimes
    newProbs = []
    newLeftPos = []
    newRightPos = []
    newTimes = []
    
del newProbs
del newLeftPos
del newRightPos
del newTimes

""" Simulation Method """
""" Runs 10^6 simulations of the game """

timeVals = []
for numTry in range(1000000):
    if (numTry + 1)%1000 == 0:
        print('Try #' + str(numTry + 1))
    timeVals.append(hopTime)
    leftPos = 0
    rightPos = numHoops - 1
    while rightPos - leftPos > 1:
        timeVals[-1] += hopTime
        leftPos += 1
        rightPos -= 1
    while leftPos < numHoops and rightPos >= 0:
        timeVals[-1] += rpsTime
        rockPaperScissors = np.random.rand()
        while rockPaperScissors >= leftWinProb + rightWinProb:
            timeVals[-1] += rpsTime
            rockPaperScissors = np.random.rand()
        timeVals[-1] += hopTime
        if rockPaperScissors < leftWinProb:
            leftPos += 1
            rightPos = numHoops - 1
        elif rockPaperScissors < leftWinProb + rightWinProb:
            leftPos = 0
            rightPos -= 1
        while np.all([rightPos - leftPos > 1,leftPos < numHoops,rightPos >= 0]):
            timeVals[-1] += hopTime
            leftPos += 1
            rightPos -= 1
del numTry

""" Graph comparing both methods' probability distributions of game times """

trueHist,trueInds = np.histogram(totTimes,np.arange(max(totTimes)),weights=probs)
trueHist = trueHist/np.sum(trueHist)
simHist,simInds = np.histogram(timeVals,np.arange(max(timeVals)))
simHist = simHist/np.sum(simHist)
plt.figure()
plt.plot(trueInds[:-1],trueHist,simInds[:-1],simHist)
plt.axis([0,200,0,0.04])
plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('Probability')
plt.legend(['Predicted','Simulation'])
plt.savefig('RockPaperScissorsHop_MethodComparison.pdf')

""" Gif demonstrating a simulated example of the game """

def plot_game(leftPos,rightPos,numHoops,leftWin,rightWin,tie,timePoint):
    fig, ax = plt.subplots(figsize=(6,2))
    plt.gca().set_position([0, 0, 1, 0.8])
    ax.plot(-1 + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),'g',linewidth=4)
    ax.plot(numHoops + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),'g',linewidth=4)
    for ind in range(numHoops):
        ax.plot(ind + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),'k')
    if leftWin:
        ax.plot(leftPos + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),'b',linewidth=4)
    elif rightWin:
        ax.plot(rightPos + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),'r',linewidth=4)
    elif tie:
        ax.plot(leftPos + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),color=(0.5,0.5,0.5),linewidth=4)
        ax.plot(rightPos + 0.5*np.cos(np.arange(0,2*3.141593,0.01)),0.5*np.sin(np.arange(0,2*3.141593,0.01)),color=(0.5,0.5,0.5),linewidth=4)
    if leftPos == rightPos:
        ax.fill(leftPos + 0.25*np.cos(np.arange(3.141593/2,3*3.141593/2,0.01)),0.25*np.sin(np.arange(3.141593/2,3*3.141593/2,0.01)),'b')
        ax.fill(rightPos + 0.25*np.cos(np.arange(-3.141593/2,3.141593/2,0.01)),0.25*np.sin(np.arange(-3.141593/2,3.141593/2,0.01)),'r')
    elif leftPos == numHoops:
        ax.fill(leftPos + 0.25*np.cos(np.arange(0,2*3.141593,0.01)),0.25*np.sin(np.arange(0,2*3.141593,0.01)),'b')
        ax.text(leftPos - 0.5,0.6,'Winner!!!')
    elif rightPos == -1:
        ax.fill(rightPos + 0.25*np.cos(np.arange(0,2*3.141593,0.01)),0.25*np.sin(np.arange(0,2*3.141593,0.01)),'r')
        ax.text(rightPos - 0.5,0.6,'Winner!!!')
    else:
        ax.fill(leftPos + 0.25*np.cos(np.arange(0,2*3.141593,0.01)),0.25*np.sin(np.arange(0,2*3.141593,0.01)),'b')
        ax.fill(rightPos + 0.25*np.cos(np.arange(0,2*3.141593,0.01)),0.25*np.sin(np.arange(0,2*3.141593,0.01)),'r')
    ax.set_xlim(-4,numHoops)
    ax.axis('equal')
    ax.axis('off')
    plt.title('t = ' + str(timePoint) + ' seconds')
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image

time = hopTime
leftPos = 0
rightPos = numHoops - 1
gifFrames = [plot_game(-1,numHoops,numHoops,False,False,False,0),\
             plot_game(leftPos,rightPos,numHoops,False,False,False,time)]
while rightPos - leftPos > 1:
    time += hopTime
    leftPos += 1
    rightPos -= 1
    gifFrames.append(plot_game(leftPos,rightPos,numHoops,False,False,False,time))
while leftPos < numHoops and rightPos >= 0:
    time += rpsTime
    rockPaperScissors = np.random.rand()
    while rockPaperScissors >= leftWinProb + rightWinProb:
        gifFrames.append(plot_game(leftPos,rightPos,numHoops,False,False,True,time))
        time += rpsTime
        rockPaperScissors = np.random.rand()
    if rockPaperScissors < leftWinProb:
        rightPos = numHoops
        gifFrames.append(plot_game(leftPos,rightPos,numHoops,True,False,False,time))
        leftPos += 1
        rightPos -= 1
        gifFrames.append(plot_game(leftPos,rightPos,numHoops,False,False,False,time))
    elif rockPaperScissors < leftWinProb + rightWinProb:
        leftPos = -1
        gifFrames.append(plot_game(leftPos,rightPos,numHoops,False,True,False,time))
        leftPos += 1
        rightPos -= 1
        gifFrames.append(plot_game(leftPos,rightPos,numHoops,False,False,False,time))
    while np.all([rightPos - leftPos > 1,leftPos < numHoops,rightPos >= 0]):
        time += hopTime
        leftPos += 1
        rightPos -= 1
        gifFrames.append(plot_game(leftPos,rightPos,numHoops,False,False,False,time))

imageio.mimsave('./RockPaperScissorsHop.gif', gifFrames, fps=2)





