#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:19:58 2019

@author: tefirman
"""

import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import datetime

numSims = 1e8
avgScore = 0
inc = 0.00001
scores = np.arange(0.0,1.0 + inc,inc)
probs = np.zeros(scores.shape[0] - 1)

for sim in range(int(numSims)):
    if (sim + 1)%(numSims//100) == 0:
        print('Simulation #' + str(sim + 1) + ', ' + str(datetime.datetime.now()))
    rolls = np.floor(10*np.random.rand(100)).tolist()
    if rolls[0] == 0:
        probs[0] += 1
    else:
        ind = 1
        while ind < len(rolls):
            if rolls[ind] == 0:
                rolls = rolls[:ind]
                break
            if rolls[ind] > rolls[ind - 1]:
                rolls.pop(ind)
                ind -= 1
            ind += 1
        score = float('0.' + ''.join([str(int(val)) for val in rolls]))
        avgScore += score
        probs[(score >= scores[:-1]) & (score < scores[1:])] += 1

avgScore /= numSims
probs = 100*probs/np.sum(probs)
scores = scores[:-1]
simResults = pd.DataFrame({'Score':scores,'Probability (%)':probs})

fig = px.line(simResults, x="Score", y="Probability (%)")
fig.update_layout(title=go.layout.Title(text='10<sup>' + str(round(np.log10(numSims)))[:-2] + \
'</sup> Simulations, Average Score = ' + str(round(avgScore,6)),xref="paper",x=0))
plotly.offline.plot(fig,filename='Riddler_LowRoll_ScoreDistribution.html',auto_open=True)



