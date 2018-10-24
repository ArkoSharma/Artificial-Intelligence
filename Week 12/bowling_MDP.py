# The batting team has 3 wickets and 10 overs.
# The bowling team has 5 bowlers, each of them have exactly 2 overs each.
# The (economy, strike) rates of bowler 1 to bowler 5 are given by
# {(3, 33), (3.5, 30), (4, 24), (4.5, 18), (5, 15)}, which means bowler 1 (on an average)
# takes a wicket every 33 balls bowled, and gives away 3 runs every over.


# At most 1 wicket per over - ie either a wicket falls or it doesn't fall and the prob of wicket falling is 6/strike_rate.

# Decide an optimal bowling strategy to handle a real-life match ,ie, given the required configuration ( no of overs remaining per bowler and the no of wickets in hand, decide the choice of the best bowler.)

from __future__ import print_function
import numpy as np
import copy

dp           = {} # Optimal value
dpa          = {} # Optimal action

over_left    = [2,2,2,2,2]
bowler_stats = [(3, 33), (3.5, 30), (4, 24), (4.5, 18), (5, 15)]
p_wk         = [6.0/x[1] for x in bowler_stats]

def gethash(balls_left):
    str = "" 
    for l in balls_left:
        if(l == 0):
            str += '0';
        if(l == 1):
            str += '1';
        if(l == 2):
            str += '2';
    return str

def DP(wk_left, b_oversleft):
    # The DP - state is defined by 
    #      a. The number of wickets remaining.
    #      b. The number of overs each bowler has remaining.
    # And the value is the minimum expected amount of runs .

    overs_left = sum(b_oversleft);    #overs left is the sum of overs left of all the bowlers
  
    #Base cases
    if  (overs_left == 0):
        return 0

    if  (wk_left == 0):
        return 0

    s = gethash(b_oversleft)

    #return precomputed sub-answers
    if  ((wk_left, s) in dp.keys()):
        return dp[(wk_left, s)]

    Q = []
    #choose the best bowler    
    for i in range(5):
        if  (b_oversleft[i] > 0): # if bowler has balls remaining
            b_new = copy.deepcopy(b_oversleft)
            b_new[i]     -= 1
            exp_runs      = bowler_stats[i][0] + ( p_wk[i] * DP(wk_left - 1, b_new) + (1 - p_wk[i]) * DP(wk_left, b_new))
            Q.append(exp_runs)
        else:
            Q.append(1000000000)
    
    dp[(wk_left, s)]  = np.min(Q)
    dpa[(wk_left, s)] = np.argmin(Q)
    return dp[(wk_left, s)]



#####       Simulation #######

DP(3, over_left)
print("Simulating a game::")
ol = [2,2,2,2,2] #initially
wk = 3
runs = 0.0
for i in range(10):
    if  (ol == [0,0,0,0,0] ):
        print("match finished")
        break
    print("overs = {}, wickets = {}".format(ol,wk))
    Q = []
    a     = dpa[(wk, gethash(ol))] #choose best bowler
    ol[a] -= 1 #reduce overs of the best bowler
    print("next optimal bowler is {} , runs given = {}".format(a,bowler_stats[a][0]))
    runs += bowler_stats[a][0]
    p = np.random.uniform(0,1) #prob of getting out in over i. Note these may not add up to 1(these should actually be estimates from real statistics of matches.)
    if  (p > p_wk[a]):         #only if p is greater than p_wk then assume wicket to fall.
        print("wicket falls")
        wk -= 1
        if(wk == 0):
            print("match finished")
            break
    else :
        print("wicket does not fall")
    print("\n\n")    
    
print("total runs = " , runs)
        
"""
# printing results of all states
for (a,b) in dp:
    if(a == 1):
        print("Wickets : {} , Overs Left : {} --- best run = {} , best action = {} ".format(a,b,dp[(a,b)], dpa[(a,b)]))
for (a,b) in dp:
    if(a == 2):
        print("Wickets : {} , Overs Left : {} --- best run = {} , best action = {} ".format(a,b,dp[(a,b)], dpa[(a,b)]))
for (a,b) in dp:
    if(a == 3):
        print("Wickets : {} , Overs Left : {} --- best run = {} , best action = {} ".format(a,b,dp[(a,b)], dpa[(a,b)]))
"""



