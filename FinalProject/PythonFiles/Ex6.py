# Ex6.py
#
# Maria Katrantzi
# November 25, 2019
# This script contains the code to show the graphic representing lattice g,
# as described in Exercise 6 in the pdf. 

from __future__ import division
import matplotlib.pyplot as plt
import matplotlib as mpl
from random import random

# initialize constants for the grid values
EMPTY = 0
TREE1 = 1
TREE2 = 2
TREE3 = 3
TREE4 = 4
BURNING1 = 5
BURNING2 = 6

# This function takes a 2D array as parameter, maps its data values with
# the boundaries of the colors, and saves it into an image.
def display_envg(env):
    colors = ['yellow', 'lightgreen', 'mediumseagreen', 'forestgreen', 'green', 'lightcoral', 'red']
    bounds = [0,1,2,3,4,5,6,7]
    
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    plt.imshow(env,  interpolation='none', cmap=cmap, norm=norm)
    
# This function displays the values in a matrix.
def displayMat(mat):
    for row in mat:
        print row
        
# This function returns an n - by - n grid of values, which represents lattice g. 
def latticeg(n):
    g = [[] for i in range(n)]

    for i in range(n):
        for j in range(n):
            x = random()
            if x < 0.1:
                g[i].append(TREE1)
            elif x < 0.2:
                g[i].append(TREE2)
            elif x < 0.3:
                g[i].append(TREE3)
            elif x < 0.4:
                g[i].append(TREE4)
            elif x < 0.5:
                g[i].append(BURNING1)
            elif x < 0.6:
                g[i].append(BURNING2)
            else:
                g[i].append(EMPTY)
                
    return g

# This function is the main function to create lattice g.
def main():
    n = 10  # size of grid
    
    grid = latticeg(n)
    display_envg(grid)
    displayMat(grid)
    
main()