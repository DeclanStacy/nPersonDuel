#!/usr/bin/env python3.9

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.lines import Line2D
import random, functools

@functools.cache
def targs(q):
    p = list(q)
    n = len(p)
    targets = []
    # Loop through players
    for i in range(n):
        maxx = 0
        target = 0
        # Loop through potential targets
        for j in list(range(i)) + list(range(i+1,n)):
            newP = tuple(p[:j]+p[j+1:])
            newStart, newWho = getInputs(n, i, i, j)
            newMaxx = f(newP)[newWho][newStart]
            if newMaxx >= maxx:
                maxx = newMaxx
                target = j
        targets.append(target)
    return targets

@functools.cache
def f(q):
    p = list(q)
    n = len(p)
    # Base case (2 people)
    if n == 2:
        answer = np.diag(p)@ np.array([[1,1-p[1]],[1-p[0],1]])
        answer /= (1 - (1-p[0])*(1-p[1]))
    else:
        # Set the targets
        targets = targs(q)
        # Construct matrix V
        V = np.zeros(shape = (n,n))
        for j in range(n):
            t = targets[j]
            newP = tuple(p[:t]+p[t+1:])
            temp = f(newP)
            for i in range(targets[j]):
                newStart, newWho = getInputs(n, j, i, t)
                V[i][j] = temp[newWho][newStart]
            for i in range(targets[j]+1,n):
                newStart, newWho = getInputs(n, j, i, t)
                V[i][j] = temp[newWho][newStart]
        # Construct matrix P
        P = np.diag(p)
        # Construct matrix Q
        Q = np.zeros(shape = (n,n))
        mult = 1
        # Loop over who is first player
        for j in range(n):
            if j == 0:
                # Loop over who is first to hit their target
                for i in range(n):
                    Q[i][0] = mult
                    mult *= 1-p[i]
            else:
                for i in range(n):
                    Q[i][j] = Q[i][j-1] / (1 - p[j-1])
                Q[j-1][j] = mult / (1 - p[j-1])
        answer = V@P@Q
        answer /= (1 - mult)
    return answer
    

# If player start+1 kills player kill+1, returns indices of
# the new start player and new "who" (person we are concerned with)
def getInputs(n, start, who, kill):
    if kill > start:
        newStart = (start + 1) % (n-1)
    else:
        newStart = start % (n-1)
    if who < kill:
        newWho = who
    else:
        newWho = who - 1
    return newStart, newWho

# Computes the equilibria and outputs graph of player's chance of winning
def main(p, k, times = 100, start = 0):
    x = []
    y = []
    colors = []
    for i in range(1,times+1):
        p[k] = i/times
        x.append(p[k])
        y.append(f(tuple(p))[k][start])
        colors.append(targs(tuple(p))[k]+1)
        # Reset
        f.cache_clear()
        targs.cache_clear()

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
