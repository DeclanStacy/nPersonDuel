#!/usr/bin/env python3.9

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.lines import Line2D
import functools
import truelGeneralization3 as truel

# Computes the equilibria and outputs graph of player's chance of winning
def main(p, k, times = 100, start = 0):
    x = []
    y = []
    colors = []
    for i in range(1,times+1):
        p[k] = i/times
        x.append(p[k])
        y.append(truel.f(tuple(p))[k][start])
        colors.append(truel.targs(tuple(p))[k]+1)
        # Reset
        truel.f.cache_clear()
        truel.targs.cache_clear()

    labels = [i for i in list(set(colors))]
    cols = np.array(colors)
    viridis = cm.get_cmap('viridis', len(p))
    cols = viridis(cols)
    
    for i in range(times-1):
        plt.plot(x[i:(i+2)],y[i:(i+2)], c=cols[i])
    lines = [Line2D([0], [0], color=cols[colors.index(c)], linewidth=3, linestyle='--') for c in labels]
    plt.legend(lines, labels)
    plt.xlabel(f'Accuracy of player {k+1}')
    plt.ylabel(f'Probability of player {k+1} winning')
    plt.show()
    

# Receives input from user
def getProbs():
    n = int(input('How many players are there? '))
    k = int(input(f'Which player\'s probability do you want to change? (1-{n}) '))
    probs = []
    for i in range(1,n+1):
        if i != k:
            x = input('Enter the probability of player %s hitting their shot as a decimal: ' % i)
            probs.append(float(x))
        else:
            probs.append(0)
    return probs, k-1

probs, k = getProbs()
main(probs,k)
