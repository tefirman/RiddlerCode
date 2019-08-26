#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 16:05:10 2019

@author: tefirman
"""

import numpy as np
import matplotlib.pyplot as plt

def logFactorial(value):
    """ Returns the logarithm of the factorial of the value provided using Sterling's approximation """
    if all([value > 0,abs(round(value) - value) < 0.000001,value <= 34]):
        return float(sum(np.log(range(1,int(value) + 1))))
    elif all([value > 0,abs(round(value) - value) < 0.000001,value > 34]):
        return float(value)*np.log(float(value)) - float(value) + \
        0.5*np.log(2.0*np.pi*float(value)) - 1.0/(12.0*float(value))
    elif value == 0:
        return float(0)
    else:
        return float('nan')

detectionProb = 0.25
pctAnalyzed = 0.05
realBills = 25
numSims = 10000

probs = []
winnings = []
expected = []
sim_probs = []
sim_expected = []
for fakeBills in range(501):
    """ Analytical Solution """
    numAnalyzed = round(pctAnalyzed*(realBills + fakeBills))
    choose_k = [np.exp(logFactorial(fakeBills) \
    - logFactorial(fakesAnalyzed) \
    - logFactorial(fakeBills - fakesAnalyzed) \
    + logFactorial(realBills) \
    - logFactorial(numAnalyzed - fakesAnalyzed) \
    - logFactorial(realBills - numAnalyzed + fakesAnalyzed))
    for fakesAnalyzed in range(max(numAnalyzed - realBills,0),min(numAnalyzed,fakeBills) + 1)]
    choose_k = np.array(choose_k)/sum(choose_k)
    probs.append(sum([choose_k[ind]*(1 - detectionProb)**ind for ind in range(len(choose_k))]))
    winnings.append(100*(realBills + fakeBills))
    expected.append(winnings[-1]*probs[-1])
    """ Simulated Solution """
    bills = [False for ind in range(realBills)]
    bills.extend([True for ind in range(fakeBills)])
    sim_probs.append(0.0)
    for numSim in range(numSims):
        np.random.shuffle(bills)
        sim_probs[-1] += np.any((np.random.rand(numAnalyzed) < detectionProb) & bills[:numAnalyzed])
    del numSim
    sim_probs[-1] = 1 - sim_probs[-1]/numSims
    sim_expected.append(winnings[-1]*sim_probs[-1])
del fakeBills

import matplotlib as mpl
mpl.rc('font',family='Arial')
mpl.rc('font',size=12)
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
plt.rc('font',weight='bold')

plt.figure()
plt.plot(range(len(expected)),expected)
plt.plot(range(len(sim_expected)),sim_expected)
plt.xlabel('# of fake bills',fontsize=18,fontweight='bold')
plt.ylabel('Expected Return ($)',fontsize=18,fontweight='bold')
plt.legend(['Analytical','Simulation'])
plt.savefig('RiddlerCounterfeitGraph.png')

