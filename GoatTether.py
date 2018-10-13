#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 19:37:23 2018

@author: tefirman
"""

import numpy as np
from scipy.optimize import minimize
import imageio
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rc('font',family='Arial')
mpl.rc('font',size=12)
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
plt.rc('font',weight='bold')
textSize = 18
lineSize = 3
markerSize = 25

""" Finding tether length for target grazing of 50% """
""" Solves numerically using the Nelder-Mead simplex algorithm """

targetPortion = 0.5

def grazing_area(tether):
    global targetPortion
    ### Assuming field radius is 1 for ease of calculation ###
    theta = np.arccos(tether/2)
    area = (theta*(tether**2) + 2*((np.pi/2 - theta) - tether/2*np.sin(theta)))/np.pi
    return (area - targetPortion)**2

res = minimize(grazing_area,0.5,method='nelder-mead',tol=1e-6)
print(str(round(100*targetPortion,1))[:-2] + '% grazing at L = ' + str(round(res['x'][0],4)) + 'R')

""" Plotting grazing coverage as a function of tether length """

coverages = []
lengths = np.arange(0,2.01,0.01)
for tether in lengths:
    theta = np.arccos(tether/2)
    coverages.append(100*(theta*(tether**2) + 2*((np.pi/2 - theta) - tether/2*np.sin(theta)))/np.pi)
    del theta
del tether
plt.figure(figsize=(6,5))
plt.plot(lengths,coverages,linewidth=lineSize)
plt.plot(res['x'][0],50,'.r',markersize=markerSize)
plt.grid(True)
plt.xticks(np.arange(0,2.1,0.5))
plt.yticks(np.arange(0,101,25))
plt.xlabel('Tether Length (L/R)',fontsize=textSize,fontweight='bold')
plt.ylabel('Grazing Percentage',fontsize=textSize,fontweight='bold')
plt.title(str(round(100*targetPortion,1))[:-2] + '% grazing at L = ' + \
str(round(res['x'][0],4)) + 'R',fontsize=textSize,fontweight='bold')
plt.tight_layout()
plt.savefig('TetherLengthVsGrazing.png')

""" Gif demonstrating the area grazed by the goat """

def plot_goat(tether):
    fig, ax = plt.subplots(figsize=(6,6))
    plt.gca().set_position([0, 0, 1, 0.9])
    ax.fill(np.cos(np.arange(-np.pi,np.pi + 0.01,0.01)),np.sin(np.arange(-np.pi,np.pi + 0.01,0.01)),'g')
    xVals = tether*np.cos(np.arange(-np.pi,np.pi + 0.01,0.01)) - 1
    yVals = tether*np.sin(np.arange(-np.pi,np.pi + 0.01,0.01))
    inds2keep = (xVals**2 + yVals**2)**0.5 < 1
    xVals = xVals[inds2keep]
    yVals = yVals[inds2keep]
    xVals_temp = np.cos(np.arange(0,2*np.pi + 0.01,0.01))
    yVals_temp = np.sin(np.arange(0,2*np.pi + 0.01,0.01))
    inds2keep = ((xVals_temp + 1)**2 + yVals_temp**2)**0.5 < tether
    xVals = np.append(xVals,xVals_temp[inds2keep])
    yVals = np.append(yVals,yVals_temp[inds2keep])
    del xVals_temp
    del yVals_temp
    ax.fill(xVals,yVals,'xkcd:brown')
    ax.plot(tether - 1,0,'.w',markersize=25)
    ax.axis('equal')
    ax.axis('off')
    theta = np.arccos(tether/2)
    area = (theta*(tether**2) + 2*((np.pi/2 - theta) - tether/2*np.sin(theta)))/np.pi
    plt.title('L/R = ' + str(round(tether,1)) + ', A = ' + str(round(100*area,1)) + '%',fontsize=25,fontweight='bold')
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image

gifFrames = [plot_goat(radius) for radius in np.arange(0.2,2.01,0.2)]
imageio.mimsave('./GoatGrazing.gif', gifFrames, fps=2)




