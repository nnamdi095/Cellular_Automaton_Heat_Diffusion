#-------------CELLULAR AUTOMATON HEAT DIFFUSION SIMULATION--------------------------------#

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#FUNCTION TO APPLY HOT AND COLD SITES ON THE METAL BAR GRID
def applyHotCold(ambientBar, hotS, coldS):
    for coord in (hotS):
        ambientBar[coord[0], coord[1]] = HOT
    for coord in (coldS):
        ambientBar[coord[0], coord[1]] = COLD
    return ambientBar

#FUNCTION TO CREATE AN mxn GRID AS METAL BAR
def initBar(m,n,hotS, coldS):
    ambientBar = np.zeros((5,7))
    ambientBar.fill(25)
    return applyHotCold(ambientBar, hotS, coldS)

#FUNCTION TO APPLY DIFFUSION TO EACH CELL SITE TO DETERMINE TEMPERATURE
def diffusion(r, site, E, W, N, NE, NW, S, SE, SW):
    return (1-8*r)*site + r*(E + W + N + NE + NW + S + SE + SW)

#FUNCTION TO CREATE AN EXTENDED LATTICE WITH A REFLECTING BOUNDARY CONDITIONKK
def reflectingLat(Lat):
    refUp = np.copy(Lat[0,:]).reshape(1,n)
    refDown = np.copy(Lat[m-1,:]).reshape(1,n)
    refLat1 = np.concatenate((refUp, Lat, refDown), axis = 0)
    m2 = refLat1.shape[0]
    n2 = refLat1.shape[1]
    refLeft = np.copy(refLat1[:,0]).reshape(m2, 1)
    refRight= np.copy(refLat1[:, n2-1]).reshape(m2, 1)
    refLat = np.concatenate((refLeft, refLat1, refRight), axis = 1)
    return refLat

#FUNCTION TO APPLY DIFFUSION TO THE INNER CELLS OF THE EXTENDED LATTICE
def applydiffusionExt(r, barExt):
    for i in range(1, m+1):
        for j in range(1, n+1):
            site = barExt[i,j]
            E = barExt[i,j+1]
            W = barExt[i, j-1]
            N = barExt[i-1, j]
            NW = barExt[i-1, j-1]
            NE = barExt[i-1, j+1]
            S = barExt[i+1, j]
            SW = barExt[i+1, j-1]
            SE = barExt[i+1, j+1]
            new_site = diffusion(r, site, E, W, N, NE, NW, S, SE, SW)
            barExt[i,j] = new_site
    new_bar = barExt[1:m+1, 1:n+1]
    return new_bar
    
    
#FUNCTION TO RUN SIMULATION OF HEAT DIFFUSION
def diffusionSim(m,n, r, t):
    bar = initBar(m, n, hotS, coldS)
    grid = [bar]
    for i in range(t):
        barExt = reflectingLat(bar)
        bar = applydiffusionExt(r, barExt)
        grid.append(bar)  
    return grid


#DEFINE GLOBAL VARIABLES
HOT = 50
COLD = 0
AMBIENT = 25
#DEFINE COORDINATES FOR HOT AND COLD SITES
hotS = [(0,5), (2,0), (3,0)]
coldS = [(4,2), (4, 3)]
#DEFINE SIZE OF METAL BAR
m = 5
n = 7
#DEFINE DIFUSSION RATE CONSTANT r AND NUMBER OF STEPS t
r = 0.1
t = 11


#VISUALIZATION RESULTS
grid = diffusionSim(m,n, r, t)
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, sharex=True, sharey = True, figsize = (12,6))
axs = [ax1,ax2,ax3,ax4,ax5, ax6, ax7, ax8, ax9]

for n in range(0,len(axs)):
    sample = grid[n]
    g = sns.heatmap(sample,cmap="coolwarm",cbar=False,ax=axs[n])
    g.set_title('Grid at t={}'.format(n), fontsize = 8)
    if n==0:
        sample = grid[0]
        g = sns.heatmap(sample,cmap="coolwarm",ax=axs[0])
#plt.savefig('heat_diffusion.png')        
        
