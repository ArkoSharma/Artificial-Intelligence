"""
Arko Sharma
05.10.2018
Program depicting Value iteration and Policy iteration in a grid world MDP environment.
Here the reward is a function of the current state and action only ie a constant reward is 
obtained upon taking an action from a state; which can be assumed to be the expected
reward over all states reachable from that state, on that action.
There are two solver methods for solving in the infinite horizon setting
                            
                               : Policy - iteration and Value - iteration which start with 
                                 random pseudovalue initial answers and iteratively 
                                 converge towards the actual answers depicting an 
                                 infinite horizon with discounted rewards.
                                 
There is also a general method using DP , which solves the finite horizon case
                               
                               : Using simple dynamic programming, starting with a given 
                                 start state and given number of steps (FINITE horizon), we
                                 use the optimality principle  to get the best possible value out of the grid.
"""

from __future__ import print_function
import numpy as np
import copy
import random

class state:
      
    def __init__(self, r, c):
        self.r = r
        self.c = c
          
          
class MDP_grid():
    
    """
    This is a grid environment for a MDP problem.
    The state is defined by the location of the agent in the grid.
    For each state, 4 actions are allowed - movement in the 4 directions.
    
    There is a transition-probability matrix "T" which gives a list of states
    reachable on a particular action at a particular state , alongwith the probability of
    of this transition.        
    This depicts the randomness of a real - world scenario.
    There is a reward matrix "R" which stores the reward obtained upon taking an action at
    a given state. This value represents the expected reward over all states reachable from 
    that state on that action.
  
    There is also an Actions matrix representing the set of allowed actions. 
    """

    
    def __init__(self, dimension, gamma):
        self.dimension = dimension
        self.gamma = gamma
        self.T = {}
        self.R = {}
        self.actions  = ["u", "d", "l", "r"]
        self.dxdy_act = {}
        self.dxdy_act["u"] = (-1, 0)
        self.dxdy_act["d"] = (1, 0)
        self.dxdy_act["l"] = (0, -1)
        self.dxdy_act["r"] = (0, 1)
        self.states = []
        for i in range (self.dimension):
            for j in range (self.dimension):
                self.states.append(state(i, j))
                
        self.generate_random_TransitionProbabilityMatrix(self.states, self.actions)
        self.generate_random_RewardMatrix(self.states, self.actions)
        

    def inside_board(self, state):
        r, c = state.r, state.c
        if(r >= 0 and r < self.dimension and c >=0 and c < self.dimension):
            return True
        else: 
            return False

    def get_state(self, some_state):
        """
        Function to return that state of the MDP which has the given values of the state variables
        """
        for s in self.states:
            if (s.r == some_state.r and s.c == some_state.c):
                return s
        
    def generate_random_RewardMatrix(self, states, actions):
        
        """
        Function used to generate R
        Here, R is only a function of state and action ie each state has a fixed reward for
        every action - which can be assumed to be the expected reward over all states reachable
        from a state upon applying the given action.
        """
        
        for s in states:
            for a in actions:
                self.R[(s,a)] = np.random.randint(-5 , 10)



    def generate_random_TransitionProbabilityMatrix(self, states, actions):
        
        """
        Function used to generate T.
        Assumed that the agent moves only to the 4 adjoining cells with non zero probability.
        Movement to any state(cell) that does not share a side with current is impossible.
        """
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        

        for s in states:
            for a in actions:
                valid_neighbours = []

                success     = np.random.uniform(0.7, 1.0)
                succ_neigh  = state(self.dxdy_act[a][0] + s.r , self.dxdy_act[a][1] + s.c)
                if(not(self.inside_board(succ_neigh))):
                    success = 0
          
                for x in dx:
                    for y in dy:
                        neighbour = state(s.r + x, s.c + y)
                        if (self.inside_board(neighbour) and neighbour != succ_neigh):
                            valid_neighbours.append(self.get_state(neighbour))
               
                fail           = (1 - success)/len(valid_neighbours)
                self.T[(a, s)] = []
                for val_neigh in valid_neighbours:
                    self.T[(a, s)].append((val_neigh, fail))
                
                if (success != 0):
                    self.T[(a, s)].append((self.get_state(succ_neigh), success))                 
                                                     
        
class SolveMDP:
    
    """
    Solver Class to solve MDP and return optimal policy.
    Method : Value Iteration and Policy Iteration.
    """
    def __init__(self):
        pass
  
    def value_iteration(self, mdp_grid, epsilon):
        """
        Solving a MDP to get optimal value using value - iteration.
        Starting with random V and iterating till convergence.
        """

        #define random Values    
        V = {}
        T, R, gamma = mdp_grid.T, mdp_grid.R, mdp_grid.gamma

        for s in mdp_grid.states:
            V[s] = np.random.randint(0, 11)
       
        while(True):
            V_copy = {}
            for s in mdp_grid.states:
                V_copy[s]  = V[s] 
            for s in mdp_grid.states:
                Q = []
                for a in mdp_grid.actions:
                    #first add the expected reward on taking this action (present)
                    acc = R[(s,a)] 
                    for (next_state, prob) in T[(a, s)]:
                        #then add the expected discounted reward of the future
                        acc += prob*( gamma * V_copy[next_state])
                    Q.append(acc) 
                V[s] = max(Q)


             for i in range (mdp_grid.dimension):
                 for j in range(mdp_grid.dimension):
                 
                     print ("{} ".format(V[mdp_grid.get_state(state(i, j))]), end = "")
                 print("")
             print("\n\n")

            delta = 0
            for s in mdp_grid.states:
                delta = max(delta, abs(V[s] - V_copy[s]))
            if  delta <= epsilon*(1 - gamma)/gamma:
                return (V, self.recover_policy(mdp_grid, V))

    def recover_policy(self, mdp_grid, V):
        """
        Function to recover optimal policy given the optimal values for each state.
        """
        policy = {}
        for s in mdp_grid.states:
            policy[s] = np.argmax ( [   mdp_grid.R[(s,a)] + mdp_grid.gamma * sum ( [ prob * V[next] for (next, prob) in mdp_grid.T[(a, s)] ] ) for a in mdp_grid.actions  ] )   
        return policy



    def DP_helper(self, mdp_grid, grid_state, steps_remaining):
        """
        Returns optimal value of a dp - state defined by the cell the agent is in and the no. of remaining steps to take.
        """
 
        cell = (grid_state.r, grid_state.c)
        #Base case
        if  (steps_remaining == 0):
            # since no more actions can be taken, this result will be 0
            self.dp[(cell, steps_remaining)] = 0
            return self.dp[(cell, steps_remaining)]
 
        if  (self.dp[(cell, steps_remaining)] != -100000000000000):
            #returning pre-solved subproblem answer
            return self.dp[(cell, steps_remaining)]
     
        else:
            temp = -100000000000000
            for a in mdp_grid.actions:
                #first add the current expected reward
                disc_exp_reward = mdp_grid.R[(grid_state, a)]
                for (next, prob) in mdp_grid.T[(a, grid_state)]:
                    # add the expected reward of the future
                    disc_exp_reward += prob * ( mdp_grid.gamma * self.DP_helper(mdp_grid, next, steps_remaining - 1))
                temp = np.max([temp, disc_exp_reward])
            self.dp[(cell, steps_remaining)] = temp
            return self.dp[(cell, steps_remaining)]

                
    def DP_FiniteHorizon(self, mdp_grid, num_steps):
        """
        Solving the MDP grid world for a finite horizon by DP.
        Function to optimise the cumulative sum of discounted expected rewards over a given finite horizon for every choice of starting state.
        """
        #here dp will store the optimal value of the state given the number of remaining steps.
        self.dp = {}
        V       = {}
 
        for s in mdp_grid.states:
            for steps in range(num_steps + 1):
                self.dp[((s.r, s.c), steps)] = -100000000000000

        for s in mdp_grid.states:
            V[s] = self.DP_helper(mdp_grid, s, num_steps)

        return (V, self.recover_policy(mdp_grid, V))
               
	
	
    def policy_iteration(self, mdp_grid):
        """
        Solving the MDP question by policy iteration.
        Actually, this is modified (depth limited) policy iteration which is more efficient.
        """

        V      = {}       
        policy = {}

        #choose a random policy
        for s in mdp_grid.states:
            V[s]      = 0
            policy[s] = np.random.randint(0,4)


        while True:
        
            V = self.policy_evaluation(policy, V, mdp_grid)
            unchanged = True
            recovered_policy = self.recover_policy(mdp_grid, V)
            for s in mdp_grid.states:
                if recovered_policy[s] != policy[s]:
                    policy[s] = recovered_policy[s]
                    unchanged = False
            if unchanged:
		V = self.policy_evaluation(policy, V, mdp_grid)           
                return (V, policy)



    def policy_evaluation(self, policy, V, mdp_grid):
        """
        Use depth - limited evaluation : update V only for a fixed number of steps.
        """
        V_copy = {}
        R, T, gamma = mdp_grid.R, mdp_grid.T, mdp_grid.gamma
        k = 0
         
        while True:
            k += 1
            V_copy = {}
            for s in mdp_grid.states:
                V_copy[s]  = V[s] 
            delta    = 0
            for s in mdp_grid.states:
                a    = mdp_grid.actions[ policy[s] ]
                acc  = R[(s,a)] 
                for (next_state, prob) in T[(a, s)]:
                    acc += prob*( gamma * V_copy[next_state])
                V[s] = acc

            if k == 20 :
                return V

                
        return V




"""
Generating a grid and solving the MDP question.
"""
dimension = 4
gamma     = 0.9
grid      = MDP_grid(dimension, gamma)
solver    = SolveMDP()

valueVI, policyVI = (solver.value_iteration(grid, 0.000001))
steps             = 800
valueDP, policyDP = solver.DP_FiniteHorizon(grid, steps)


print("Above are the progressive value - matrices of Value Iteration.\n")

print ("Rewards:")
for s in grid.states:
    for a in grid.actions:
        print ("Reward of state {} and action {} is {} ".format((s.r, s.c), a, grid.R[(s,a)]) )

print ("\nOptimal Value Matrix from ValueIteration ::")
print ("-------------------------------------------------------------------------\n")

for i in range (dimension):
    for j in range(dimension):
        print("{} ".format(valueVI[ grid.get_state(state(i, j)) ] ), end = "")
    print("") 
print ("-------------------------------------------------------------------------\n")

print ("\nOptimal Value Matrix for finite horizon ( number of steps = {} )  vv\n".format(steps))
print ("-------------------------------------------------------------------------\n")
for i in range (dimension):
    for j in range(dimension):
        print("{} ".format(valueDP[ grid.get_state(state(i, j)) ] ), end = "")
    print("") 
print ("-------------------------------------------------------------------------\n")


valuePI, policyPI = (solver.policy_iteration(grid))

print ("\nOptimal Value Matrix from PolicyIteration  vv\n")
print ("-------------------------------------------------------------------------\n")
for i in range (dimension):
    for j in range(dimension):
        print("{} ".format(valuePI[ grid.get_state(state(i, j)) ] ), end = "")
    print("") 
print ("-------------------------------------------------------------------------\n")


print ("Policy from value iteration ::\n")
print ("-------------------------------------------------------------------------\n")
for i in range (dimension):
    for j in range(dimension):
        print("{} ".format(grid.actions[policyVI[grid.get_state(state(i, j))]]), end = "")
    print("") 
print ("-------------------------------------------------------------------------\n")


print ("Policy from DP with {} steps ::\n".format(steps))
print ("-------------------------------------------------------------------------\n")
for i in range (dimension):
    for j in range(dimension):
        print("{} ".format(grid.actions[policyDP[grid.get_state(state(i, j))]]), end = "")
    print("") 
print ("-------------------------------------------------------------------------\n")


print ("\nPolicy from policy iteration ::\n")
print ("-------------------------------------------------------------------------\n")
for i in range (dimension):
    for j in range(dimension):
        #pass
        print("{} ".format(grid.actions[policyPI[grid.get_state(state(i, j))]]), end = "")
    print("")
print ("-------------------------------------------------------------------------\n")


"""
stress = 0
for i in range(200):
    dimension = 4
    gamma     = 0.9
    grid      = MDP_grid(dimension, gamma)
    solver    = SolveMDP()

    valueVI, policyVI = (solver.value_iteration(grid, 0.000001))
    valuePI, policyPI = solver.policy_iteration(grid)
    for s in grid.states:
        stress = max((stress, abs(valueVI[s] - valuePI[s])) )
print (stress)
"""
