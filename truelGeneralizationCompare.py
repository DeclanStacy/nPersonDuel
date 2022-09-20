#!/usr/bin/env python3.9

import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.lines import Line2D


# winning[q][(start,who)] is probablity of player who+1 winning
# when player start+1 starts and the list of probabilities of hitting shots is q
winning = {}

# targs[q] is a list of each player's target
# ex. targs[[1/3,2/3,1]] is [2,2,1] because player 1 targets player 3,
# player 2 targets player 3, and player 3 targets player 2
targs = {}

# If player start+1 kills player kill+1, returns indices of
# the new start player and new "who" (person we are concerned with)
def getInputs(p, start, who, kill):
    newP = p[:kill]+p[kill+1:]
    if kill > start:
        newStart = (start + 1) % len(newP)
    else:
        newStart = start % len(newP)
    if who < kill:
        newWho = who
    else:
        newWho = who - 1
    return newP, newStart, newWho
    
# Returns probability of player who+1 winning when player start+1 starts
def f(p, start, who):
    q = tuple(p)
    # See if already computed
    if q in winning and (start, who) in winning[q]:
        return winning[q][(start,who)]
    # Base case (2 people)
    if len(p) == 2:
        targs[q] = [1,0]
        if start == who:
            answer = p[who] / (1 - (1-p[0]) * (1-p[1]))
        else:
            answer = 1 - f(p, start, 1 - who)
    else:
        # Set the targets
        if q in targs:
            targets = targs[q]
        else:
            targets = []
            for i in range(len(p)):
                maxx = 0
                target = 0
                for j in list(range(i)) + list(range(i+1,len(p))):
                    newP, newStart, newWho = getInputs(p, i, i, j)
                    newMaxx = f(newP, newStart, newWho)
                    if newMaxx >= maxx:
                        maxx = newMaxx
                        target = j
                targets.append(target)
            targs[q] = targets
        # Go through every possibility of people making their shots
        mult = 1
        answer = 0
        for i in list(range(start, len(p))) + list(range(start)):
            if targets[i] != who:
                newP, newStart, newWho = getInputs(p, i, who, targets[i])
                answer += p[i] * mult * f(newP,newStart,newWho)
            mult *= (1 - p[i])
        answer /= (1 - mult)
    # Keep memory of what has been computed       
    if q in winning:
        winning[q][(start,who)] = answer
    else:
        winning[q] = {(start,who) : answer}
    return answer

# Computes the equilibria and outputs graph of player's chance of winning
def main(p, k, times = 100, start = 0):
    global targs
    global winning
    x = []
    y = []
    colors = []
    for i in range(1,times+1):
        p[k] = i/times
        x.append(p[k])
        y.append(f(p, start, k))
        colors.append(targs[tuple(p)][k]+1)
        # Reset
        winning = {}
        targs = {}

    labels = [i for i in list(set(colors))]
    cols = np.array(colors)
    viridis = cm.get_cmap('viridis', len(p))
    cols = viridis(cols)
    
    # plt.scatter(x, y, c = colors)
    # plt.plot(x,y)
    for i in range(times-1):
        plt.plot(x[i:(i+2)],y[i:(i+2)], c=cols[i])
    # plt.show()
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
# input()
##import time
##t = time.time()
##f([.05*i for i in range(1,17)],0,0)
##print(time.time()-t)
