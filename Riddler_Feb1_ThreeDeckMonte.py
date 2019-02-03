#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:26:54 2019

@author: firman.taylor
"""

import numpy as np

numSims = 100000

red = np.array(4*[14] + 4*[9] + 4*[7])
blue = np.array(4*[13] + 4*[11] + 4*[6])
black = np.array(4*[12] + 4*[10] + 4*[8])

redWins = 0
blueWins = 0
for numSim in range(numSims):
    np.random.shuffle(red)
    np.random.shuffle(blue)
    ind = 1
    while np.sum(red[:ind] > blue[:ind]) < 5 and np.sum(blue[:ind] > red[:ind]) < 5:
        ind += 1
    if np.sum(red[:ind] > blue[:ind]) == 5:
        redWins += 1
    else:
        blueWins += 1
if redWins > blueWins:
    print('Red wins against Blue ' + str(round(100*redWins/numSims,1)) + '% of the time')
else:
    print('Blue wins against Red ' + str(round(100*blueWins/numSims,1)) + '% of the time')

blueWins = 0
blackWins = 0
for numSim in range(numSims):
    np.random.shuffle(blue)
    np.random.shuffle(black)
    ind = 1
    while np.sum(blue[:ind] > black[:ind]) < 5 and np.sum(black[:ind] > blue[:ind]) < 5:
        ind += 1
    if np.sum(blue[:ind] > black[:ind]) == 5:
        blueWins += 1
    else:
        blackWins += 1
if blueWins > blackWins:
    print('Blue wins against Black ' + str(round(100*blueWins/numSims,1)) + '% of the time')
else:
    print('Black wins against Blue ' + str(round(100*blackWins/numSims,1)) + '% of the time')

blackWins = 0
redWins = 0
for numSim in range(numSims):
    np.random.shuffle(black)
    np.random.shuffle(red)
    ind = 1
    while np.sum(black[:ind] > red[:ind]) < 5 and np.sum(red[:ind] > black[:ind]) < 5:
        ind += 1
    if np.sum(black[:ind] > red[:ind]) == 5:
        blackWins += 1
    else:
        redWins += 1
if blackWins > redWins:
    print('Black wins against Red ' + str(round(100*blackWins/numSims,1)) + '% of the time')
else:
    print('Red wins against Black ' + str(round(100*redWins/numSims,1)) + '% of the time')

