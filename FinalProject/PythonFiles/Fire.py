# Fire.py
#
# Maria Katrantzi
# November 25, 2019
# This script contains the code for the simulation of fire spread by
# generating plots and a gif simulating fire spreading, the total burned, 
# and the percentage burned.

from __future__ import division
from random import random
from matplotlib.animation import PillowWriter
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# initialize constants for the grid values
EMPTY = 0       #  empty ground
TREE = 1        #  non-burning tree
BURNING = 2     #  burning tree
HALFBURNING = 3 #  half-burning tree

fig = plt.figure()  #  create the figure to animate
ims = []            #  list to save the image plots

# This function takes a 2D array as parameter, maps its data values with
# the boundaries of the colors, and saves it into an image.
def display_env(env):
    
    colors = ['yellow', 'green', 'darkorange', 'peru']
    bounds = [0,1,2,3,4]
    
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    im = plt.imshow(env,  interpolation='none', cmap=cmap, norm=norm)
    ims.append([im])
    
# This function returns an n - by - n grid of values (EMPTY, TREE, BURNING), 
# which represents the initial state of the forest. 
def initForest(n):
    probTree =  0.5    #  probability of grid site occupied by tree (i.e., tree density)
    probBurning = 0.5  #  probability that a tree is burning (i.e., fraction of burning trees)
                       
    forest = [[] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if random() < probTree:
                if random() < probBurning:
                    forest[i].append(BURNING)
                else:
                    forest[i].append(TREE)
            else:
                forest[i].append(EMPTY)    

    return forest

# This function is used to spread fire by the following rules:
#   At next time step, an empty site either remains empty or a tree grows on it.
#   Burning tree results in half-burning tree at next time step.
#   Half-burning tree results in empty cell at next time step.
#   Perhaps next time step tree with burning neighbor(s) and/or diagonal elemement(s) burns itself.
#   Perhaps tree is hit by lightning and burns next time step.
def spread(site, N, E, S, W, NE, SE, SW, NW):
    probImmune = 0.4       #  probability of immunity from catching fire 
    probLightning = 0.05   #  probability of lightning hitting a site
    probGrow = 0.2         #  probability of a tree growing instantaneously in an empty cell
    probFire = 0           #  probability of a tree catching fire that is proportional to the number
                           #  of neighboring and/or diagonal trees that are on fire 
    count = 0              #  count for number of neighboring and/or diagonal trees that are on fire
    if (site == EMPTY):
        if random() < probGrow:
            returnValue = TREE
        else:
            returnValue = EMPTY
    elif (site == BURNING):  
        returnValue = HALFBURNING  
    elif (site == HALFBURNING):
        returnValue = EMPTY
    elif (site == TREE):
        if (N == BURNING):
           count += 1
        if (E == BURNING):
            count += 1                
        if (S == BURNING):
            count += 1
        if (W == BURNING):
            count += 1
        if (NE == BURNING):
           count += 1
        if (SE == BURNING):
            count += 1                
        if (SW == BURNING):
            count += 1
        if (NW == BURNING):
            count += 1
        probFire = count / 8 
        if probFire > probImmune:
                returnValue = BURNING
        elif (random() < probLightning*(1 - probImmune)):
                returnValue = BURNING
        else:
            returnValue = TREE
    else:
        returnValue = TREE
        
    return returnValue

# This function returns an (n + 2) - by - (n + 2) matrix with periodic 
# boundaries for mat, an n - by - n matrix.
def extendLat(mat):
    n = len(mat)
    matNS = [mat[n - 1]]
    matNS = matNS + mat
    matNS.append(mat[0])
    matExt = [[] for i in range(n + 2)]
    for i in range(n + 2):
        matExt[i] = [matNS[i][n - 1]] + matNS[i] + [matNS[i][0]]
    return matExt
        
# This function displays the values in a matrix.
def displayMat(mat):
    for row in mat:
        print row

# This function returns the internal lattice of mat, with spread applied 
# to each site.
def applyExtended(mat):
    copy = copyInsideMat(mat)
    n = len(copy)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            site = mat[i][j]
            N = mat[i - 1][j]
            E = mat[i][j + 1]
            S = mat[i + 1][j]
            W = mat[i][j - 1]
            NE = mat[i - 1][j + 1]
            SE = mat[i + 1][j + 1]
            SW = mat[i + 1][j - 1]
            NW = mat[i - 1][j - 1]
            copy[i - 1][j - 1] = spread(site, N, E, S, W, NE, SE, SW, NW) 
    return copy

# This function returns a copy of the inside of a square matrix.
def copyInsideMat(mat):
    m = len(mat) - 2
    copy = [[] for i in range(m)]
    
    for i in range(m):
        for j in range(m):
            copy[i].append(mat[i + 1][j + 1])

    return copy

# This function is the main function to create and test a fire simulation.
def main():
    t = 100  # number of time steps
    n = 20  # size of forest
    
    forest = initForest(n)
    display_env(forest)

    for i in range(t):
        forestExtended = extendLat(forest)
        forest = applyExtended(forestExtended)
        display_env(forest)

   #  create animation (GIF) based on the image generated at every time step    
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=500)
    
    # save the GIF
    writer = PillowWriter(fps=20)
    ani.save("fire.gif", writer=writer)

main()