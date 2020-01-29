#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:52:20 2019

@author: eelhm

Script to plot 2 cones, each with a dip angle of 45 degrees.
Dome 1 has a height of 100m, dome 2 has a height of 300m.
Each dome is plotted using a wireframe. 
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#%%

ang1 = np.radians(45) # Dip angle of cone
npoints = 360
p_int = np.radians(np.true_divide(360,npoints)) # Points plotted at 1 degree intervals
xtop = 0 # x coordinate of peak of dome
ytop = 0 # y coordinate of peak of dome
ang2 = np.arange(0,2*np.pi,p_int)
ax={}

fig=plt.figure(figsize=[15,5])
plt.rcParams['font.size']=13

h = [100,300] # Heights of domes to be plotted

# Creating subplots with 3d axes.
ax[h[0]] = fig.add_subplot(121,projection='3d') 
ax[h[1]] = fig.add_subplot(122,projection='3d')

for n in h: # 1 cone plotted for each loop
    # Coordinates to plot, x, y, z
    x = []
    y = []
    z = []
    ztop = n # Top of cone
    for i in ang2: # Looping through angles, 1 degree increment
        for j in range(ztop): # Looping through from 0 to cone height minus 1
            k=ztop-j # Now looping through from 300 to 1, counting down.
            r = np.true_divide(k,np.tan(ang1)) # Horizontal distance from centre of cone
            x.append(np.multiply(r,np.sin(i))) # X coordinate to plot
            y.append(np.multiply(r,np.cos(i))) # Y coordinate to plot
            z.append(j) # Z coordinate to plot
    x.append(xtop) # Appending final point to array, top of cone.
    y.append(ytop)
    z.append(n)

    # Plot limits
    ax[n].set_xlim([-450,450])
    ax[n].set_ylim([-450,450])
    ax[n].set_zlim([0,400])
    # Plotting cone using wireframe
    ax[n].plot_wireframe(x,y,z,rstride=10,cstride=10, color='r', alpha=0.5)
    # Setting tick marks
    ax[n].set_xticks(np.arange(-400,401,200))
    ax[n].set_yticks(np.arange(-400,401,200))
    ax[n].set_zticks(np.arange(0,401,200))
    ax[n].set_xlabel('\nx (m)')
    ax[n].set_ylabel('\ny (m)')
    ax[n].set_zlabel('\nz (m)')
    ax[n].set_title('Dome height = '+str(n)+' m\n')

plt.savefig('/nfs/student42/eelhm/My_Documents/Data/Python_Scripts/time_dep/dome_cone.jpeg', dpi=300)
plt.show()