#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:42:41 2018

@author: eelhm

Script to create a 3D contour plot
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#%%
#Loading data
with open('/nfs/a116/eelhm/Output_Files/Multiple_Params/FM93_h2oc_cp.txt', 'r') as data:
        lines = data.readlines() # Reading in data
        xl = len(lines) # Number of samples in x
        yl = len(lines[0].split()) - 2 # Number of samples in y
        zl = len(lines) # Number of samples in z
        zi=[]
        # Creating 1D array of z values to loop over later
        for line in lines:
            ls = line.split()
            zi.append(float(ls[1]))
        ps = np.arange(0,yl,1) # Number of samples for pressure (y)
        p = np.zeros((yl,xl)) # Initialising 2D arrays, Pressure
        z = np.zeros((yl,xl)) # Initialising 2D arrays, Depth
        h2o = np.zeros((yl,xl)) # Initialising 2D arrays, H2O content
        for i in range(yl): # Looping through y (and x in second loop) to store values at each location in 2D grid
            j=i+1
            prw = []
            h2o[i]=np.true_divide(ps[i],4) # Values for H2O content
            for line in lines:
                ls = line.split()
                prw.append(float(ls[j+1]))
            for k in range(xl): # Looping through x
                p[i,k]=prw[k] # Storing values in 2D grid, Pressure
                z[i,k]=zi[k]  # Depth
                
#%%                
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
plt.rcParams['axes.labelpad'] = 20
plt.rcParams['font.size'] = 18

ncont=15 # Number of contours
ax.contour(-1*z,h2o,p, ncont, colors='b', linewidths=3)
ax.set_ylabel('Initial H$_\mathrm{2}$O \n content (wt.%)')
ax.set_xlabel('Depth (m)')
ax.set_zlabel('Pressure (MPa)', rotation = 90)
ax.zaxis.set_rotate_label(False)
ax.set_xticks([0, 2500, 5000])
ax.set_yticks([0, 5, 10])
ax.set_zticks([0, 1e7, 2e7, 3e7])
ax.set_zticklabels([' 0',' 1e7',' 2e7', ' 3e7'])
plt.savefig('3d_contour_plot.jpeg', dpi=300, bbox_inches='tight')
plt.show()