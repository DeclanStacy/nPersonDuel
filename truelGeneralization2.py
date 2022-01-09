import random
import numpy as np
# winning[q][who][start] is probablity of player who+1 winning
# when player start+1 starts and the list of probabilities of hitting shots is q
winning = {}

# targs[q] is a list of each player's target
# ex. targs[[1/3,2/3,1]] is [2,2,1] because player 1 targets player 3,
# player 2 targets player 3, and player 3 targets player 2
targs = {}

def f(p):
    q = tuple(p)
    n = len(p)
    # See if already computed
    if q in winning:
        return winning[q]
    # Base case (2 people)
    if n == 2:
        targs[q] = [1,0]
        answer = np.diag(p)@ np.array([[1,1-p[1]],[1-p[0],1]])
        answer /= (1 - (1-p[0])*(1-p[1]))
    else:
        # Set the targets
        if q in targs:
            targets = targs[q]
        else:
            targets = []
            # Loop through players
            for i in range(n):
                maxx = 0
                target = 0
                # Loop through potential targets
                for j in list(range(i)) + list(range(i+1,n)):
                    newP = p[:j]+p[j+1:]
                    newStart, newWho = getInputs(n, i, i, j)
                    newMaxx = f(newP)[newWho][newStart]
                    if newMaxx >= maxx:
                        maxx = newMaxx
                        target = j
                targets.append(target)
            targs[q] = targets
        # Construct matrix V
        V = np.zeros(shape = (n,n))
        for j in range(n):
            t = targets[j]
            newP = p[:t]+p[t+1:]
            for i in range(targets[j]):
                newStart, newWho = getInputs(n, j, i, t)
                V[i][j] = f(newP)[newWho][newStart]
            for i in range(targets[j]+1,n):
                newStart, newWho = getInputs(n, j, i, t)
                V[i][j] = f(newP)[newWho][newStart]
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
    winning[q] = answer
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

# Computes the equilibrium and outputs probabilities of each person winning + initial targets
def main(p, start = 0):
    for i in range(len(p)):
        print('Probability of player', i+1, 'winning:', f(p)[i][start])
    for i in range(len(p)):
        print('Player', i+1, 'targets player', targs[tuple(p)][i] + 1)

# Receives input from user
def getProbs():
    n = int(input('How many players are there? '))
    probs = []
    for i in range(1,n+1):
        x = input('Enter the probability of player %s hitting their shot as a decimal: ' % i)
        probs.append(float(x))
    return probs

main(getProbs())
input()

