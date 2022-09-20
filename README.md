# nPersonDuel

The nPersonDuel problem is:

There are n people standing in a circle, each holding a gun. Each player has a p_i chance of hitting whatever they aim for. Each player takes a turn in order, and on each turn they choose someone to shoot at (they are not allowed to shoot the ground or themselves). If they hit their target, that person is eliminated. The question is to find an (subgame perfect) equilibrium for this game and the probabilities of each player winning.

The file called "truelGeneralization..." takes in the p_i's as inputs and outputs the probability of each person winning, along with their optimal strategy when everyone is still alive.

The file called "truelGeneralizationCompare..." lets you see how the probability of a player winning and their strategy changes as their accuracy (probability of hitting their target) changes.
