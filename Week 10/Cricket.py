from __future__ import print_function
import numpy as np

dp = {}

for ball in range(0, 301):
    for player in range(0, 11): 
        dp[(player,ball)] = (-1, -1)
      




#actions contain all types of shots that can be played
shots  = [1,2,3,4,6]

#probability of a wicket falling corresponding to the selected shot
pw_min = [0.01, 0.02, 0.03, 0.1, 0.3]
pw_max = [0.1 , 0.2, 0.3, 0.5, 0.7]

#probability of scoring the number of runs given by the shot  
pr_min = 0.5
pr_max = 0.8


def get_probability(x, a):
    pw = pw_min[a] + (pw_max[a] - pw_min[a]) * (( x - 1) / 9) 
    pr = pr_min + (pr_max - pr_min) * (( x - 1) / 9) 
    return (pw, pr)


def solveDP(player, balls_left):
    """ 
    Returns the optimal action at the DP-state defined by the player's index and the no of remaining balls.
    """

    #Base cases
    if( balls_left == 0 ):
        return (0, -1)
    if( player     == 11):
        return (0, -1) 

    if (dp[(player, balls_left)][0] != -1):
        return dp[(player, balls_left)]  

    else:
        temp = -100
        Q    = []
        for a in range(len(shots)):
            p_run, p_out = get_probability(player,a)
            
            #assuming if the shot is unsuccesful then the player scores no runs.
            Q.append( p_out * solveDP( player + 1, balls_left - 1)[0] + p_run * (shots[a] + solveDP(player, balls_left - 1)[0]))
        
        best_run                 = np.max(Q)
        best_shot                = np.argmax(Q)
        dp[(player, balls_left)] = (best_run, best_shot)
        return dp[(player, balls_left)]


"""
Showing the results
"""


solveDP(1,300)

#np.savetxt("OptimalThings.txt", dp, delimiter = "\t", header = head, fmt = "%d")
for balls in range(1,301):
    for player in range(1,11):
        print("{} {} ".format(dp[(player, ball)]), end = "")
    print ("")


