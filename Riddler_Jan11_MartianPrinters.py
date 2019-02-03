#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 07:37:41 2019

@author: firman.taylor
"""

import numpy as np

printerLag = 1.0 # Number of days before a printer is ready to print again
numDays = 1825 # Number of days in your martian adventure
#printerRates = np.array([0.05,0.075,0.1]) # Probabilities of each printer breaking
printerRates = np.array([0.0,0.0,0.0]) # Probabilities of each printer breaking
vitalRate = 1.0 # Rate at which vital equipment breaks (measured in malfunctions per day)
numSims = 10000 # Number of simulations to run before averaging

times = []
for numSim in range(numSims):
    if (numSim + 1)%1000 == 0:
        print('Try #' + str(numSim + 1))
    time = 0.0
    printers = np.ones(len(printerRates)) # 1 if operational, 0 if broken
    lastPrint = -1*np.ones(len(printerRates)) # Time of each printer's last print job
    while time < numDays:
        probs = np.append(printerRates*printers,vitalRate)
        overallRate = sum(probs)
        randNum1 = np.random.rand(1)[0]
        time -= np.log(randNum1)/overallRate
        probs = probs/overallRate
        randNum2 = np.random.rand(1)[0]
        while np.any(printers == 0) and np.sum(np.all([printers == 1,time - lastPrint >= printerLag],axis=0)) > 0:
            fixInd = np.where(printers == 0)[0][-1]
            printInd = np.where(np.all([printers == 1,time - lastPrint >= printerLag],axis=0))[0][0]
            printers[fixInd] = 1
            lastPrint[printInd] += 1
            del fixInd
            del printInd
        ind = np.where([randNum2 <= sum(probs[:ind + 1]) for ind in range(len(probs))])[0][0]
        if ind < len(printers):
            printers[ind] = 0
            if np.sum(np.all([printers == 1,time - lastPrint >= printerLag],axis=0)) > 0:
                printInd = np.where(np.all([printers == 1,time - lastPrint >= printerLag],axis=0))[0][0]
                lastPrint[printInd] = time
                printers[ind] = 1
                del printInd
        else:
            if np.any(np.all([printers == 1,time - lastPrint >= printerLag],axis=0)):
                printInd = np.where(np.all([printers == 1,time - lastPrint >= printerLag],axis=0))[0][0]
                lastPrint[printInd] = time
                del printInd
            else:
                break
        del ind
    times.append(time)
del numSim

print('Average Survival Time = ' + str(round(np.average(times),1)) + \
' +/- ' + str(round(np.std(times),1)) + ' days')
print('Probability of Survival = ' + str(round(100*sum(np.array(times) >= numDays)/len(times),1)) + '%')

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font',family='Arial')
mpl.rc('font',size=12)
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
plt.rc('font',weight='bold')

vals,inds = np.histogram(times,np.arange(52) - 0.5)
inds = inds[:-1] + 0.5
vals = vals/np.sum(vals)
plt.figure(figsize=(6,5))
plt.plot(inds,100*vals,linewidth=2)
plt.axis([-2,52,-0.5,8.5])
plt.xticks(np.arange(0,51,10))
plt.yticks(np.arange(0,8.1,2))
plt.grid(True)
plt.xlabel('# of days',fontsize=18,fontweight='bold')
plt.ylabel('Probability of Survival',fontsize=18,fontweight='bold')
plt.tight_layout()
#plt.savefig('SurvivalProb.png')



