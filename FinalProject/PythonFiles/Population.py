# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random
# The follwoing 2 libraries are needed
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# This will create the figure to animate
fig = plt.figure()
ims = []

def display_env(env):
    # the image will be saved in a list of images
    im = plt.imshow(env)
    ims.append([im])

def rand_cell(env):
    row, col = env.shape
    r = random.randint(0, row - 1)
    c = random.randint(0, col - 1)
    return r, c

def rand_neighbor(env, r, c):
    rows, cols = env.shape
    nei = [(-1,0),(1,0),(0,1),(0,-1)]    
    i = nei[random.randint(0, 3)]
    n_r = (r + i[0])%rows
    n_c = (c + i[1])%cols

    return n_r, n_c

def initial_env(width, height, prop_prey, prop_pred):
   
    if (prop_pred + prop_prey) > 1:
        raise ValueError('Percentage prey plus percentage predators for initial ' +
                         'environment is greater than 100%!')
    else:
        arr = np.random.choice([0,1,2],size=(width,height),p=[1-(prop_prey+prop_pred),prop_prey,prop_pred])
        return arr

def reproduction(env,rP):
    r, c = rand_cell(env)
    
    if env[r][c] == 1:
        n_r, n_c = rand_neighbor(env,r,c)
        if env[n_r][n_c] == 0:
            if random.random() < rP:
                env[n_r][n_c] = 1

def predation(env,rP):
    r, c = rand_cell(env) 
    
    if env[r][c] == 2:
        n_r, n_c = rand_neighbor(env,r,c)
        if env[n_r][n_c] == 1 :
            if random.random() < rP:
                env[n_r][n_c] = 2
      
def starvation(env,rP):            
    r, c = rand_cell(env) 
    
    if env[r][c] == 2:
        n_r, n_c = rand_neighbor(env,r,c)
        if env[n_r][n_c] == 0 :
            if random.random() < rP:
                env[r][c] = 0
                               
def count_species(env,species):
    num = 0
    for r in range(len(env)):
        for c in range(len(env[r])):
            if env[r][c] == species:
                num += 1
    
    return num 
        
def predator_prey(n_gens,r,p,d, prop_prey, prop_pred, env_rows, env_cols):
    env = initial_env(env_rows, env_cols, prop_prey, prop_pred)

    prey_list = []
    prey_list.append(count_species(env,1))
    pred_list = []
    pred_list.append(count_species(env,2))  

    for gen in range(n_gens):
        for i in range((env_rows * env_cols)//3):
            reproduction(env,r)
            predation(env,p)
            starvation(env,d)
        prey_list.append(count_species(env,1))
        pred_list.append(count_species(env,2))
        
        # Display environment will save the resulting env into an image
        display_env(env)    

    # Will contain the animation (GIF) based on the image generated at every generation     
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=500)
    
    # Saves the GIF
    writer = PillowWriter(fps=20)
    ani.save("population.gif", writer=writer)

predator_prey(500,.6,.7,.9, .6, .2, 40, 40)


