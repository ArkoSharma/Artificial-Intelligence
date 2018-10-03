"""
Arko Sharma
01.10.2018
Program depicting Value iteration and Policy iteration in a grid world environment.
Here the reward is a function of the current state only ie a constant reward is assumed to
be obtained upon reaching a state.
ToDo :
       do policy iteration
       blocks
"""
from __future__ import print_function
import numpy as np
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
        #Function to return that state of the MDP which has the given values of the state variables
        for s in self.states:
            if (s.r == some_state.r and s.c == some_state.c):
                return s
        
    def generate_random_RewardMatrix(self, states, actions):
        #Function used to generate R
        #Here, R is only a function of state ie each state has a fixed reward.
        
        for s in states:
            self.R[s] = np.random.randint(-2, 0)
        print ("Rewards:")
        k = 0
        for s in states:
            print (self.R[s], end = ' ')
            k += 1
            if ((k) % 4 == 0):
                print("")
                k = 0

    def generate_random_TransitionProbabilityMatrix(self, states, actions):
        # Function used to generate T.
        # Assumed that the agent moves only to the 4 adjoining cells with non zero probability.
        # Movement to any state(cell) that does not share a side with current is impossible.

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
        Solving an MDP to get optimal value using value - iteration.
        Starting with random V and iterating till convergence.
        """

        #define random Values    
        V = {}
        T, R, gamma = mdp_grid.T, mdp_grid.R, mdp_grid.gamma

        for s in mdp_grid.states:
            V[s] = np.random.randint(-10, 11)
       
        while(True):
            V_copy = V.copy()
            delta = 0
            for s in mdp_grid.states:
                Q = []
                for a in mdp_grid.actions:
                    acc = 0
                    for (next_state, prob) in T[(a, s)]:
                        acc += prob*(mdp_grid.R[next_state] + gamma * V_copy[next_state])
                    Q.append(acc) 
                V[s] = np.max(Q)


                for i in range (mdp_grid.dimension):
                    for j in range(mdp_grid.dimension):
                        print ("{} ".format(V[mdp_grid.get_state(state(i, j))]), end = "")
                    print("")
                print("\n\n")


            delta = max(delta, np.abs(V[s] - V_copy[s]))
            if  delta <= epsilon*(1 - gamma)/gamma:
                return self.recover_policy(mdp_grid, V)
 

    def recover_policy(self, mdp_grid, V):
        """
        Function to recover optimal policy given the optimal values for each state.
        """
        policy = {}
        for s in mdp_grid.states:
            policy[s] = np.argmax ( [  sum ( [ prob * V[next] for (next, prob) in mdp_grid.T[(a, s)] ] ) for a in mdp_grid.actions  ] )   
        return policy


    def DP_helper(self, mdp_grid, grid_state, steps_remaining):
        """
        Returns optimal value of a dp - state defined by the cell the agent is in and the no. of remaining steps to take.
        """
 
        cell = (grid_state.r, grid_state.c)
        #Base case
        if  (steps_remaining == 0):
            self.dp[(cell, steps_remaining)] = -100000000000000
            return self.dp[(cell, steps_remaining)]
 
        if  (self.dp[(cell, steps_remaining)] != -100000000000000):
            return self.dp[(cell, steps_remaining)]
     
        else:
            temp = -100000000000000
            for a in mdp_grid.actions:
                disc_exp_reward = 0
                for (next, prob) in mdp_grid.T[(a, grid_state)]:
                    disc_exp_reward += prob * (mdp_grid.R[next] +  mdp_grid.gamma * self.DP_helper(mdp_grid, next, steps_remaining - 1))
                temp = np.max([temp, disc_exp_reward])
            self.dp[(cell, steps_remaining)] = temp
            return self.dp[(cell, steps_remaining)]

                
    def DP_FiniteHorizon(self, mdp_grid, num_steps):
        """
        Solving the MPD grid world for a finite horizon by DP.
        Function to optimise the cumulative sum of discounted expected rewards over a given finite horizon for every choice of starting state.
        """
        #here dp stores the optimal value of the states.
        self.dp = {}
        V       = {}
 
        for s in mdp_grid.states:
            for steps in range(num_steps + 1):
                self.dp[((s.r, s.c), steps)] = -100000000000000

        for s in mdp_grid.states:
            V[s] = self.DP_helper(mdp_grid, s, num_steps)

        return V
                
    def policy_iteration(self, mdp_grid):
        """
        Solve an MDP by policy iteration.
        """

        V      = {}       
        policy = {}

        #choose a random policy
        for s in mdp_grid.states:
            V[s]      = 0
            policy[s] = mdp_grid.actions[ np.random.randint(0,4) ]

        while True:
            V = self.policy_evaluation(policy, V, mdp_grid)
            unchanged = True
            recovered_policy = recover_policy(mdp_grid, V)
            for s in mdp_grid.states:
                if recovered_policy[s] != policy[s]:
                    policy[s] = recovered_policy[s]
                    unchanged = False
            if unchanged:
                return policy


    def policy_evaluation(self, policy, V, mdp_grid, k=20):
    
        R, T, gamma = mdp_grid.R, mdp_grid.T, mdp_grid.gamma
        for i in range(k):
            for s in mdp_grid.states:
                for (next, prob) in T[(s, policy[s])] :
                    V[s] += gamma * prob * V[next] 
                V[s] += R[s]
        return V


grid     = MDP_grid(4, 0.9)
solver = SolveMDP()

policy  = (solver.value_iteration(grid, 0.00001))
#policy2 = (solver.policy_iteration(grid))
steps = 800
value_matrix = solver.DP_FiniteHorizon(grid, steps)


print ("Above is the optimal value-matrix obtained from value iteration (Infinite Horizon) ^^\n")

print ("\nOptimal Value Matrix for finite horizon ( number of steps = {} )  vv\n".format(steps))
for i in range (4):
    for j in range(4):
        print("{} ".format(value_matrix[ grid.get_state(state(i, j)) ] ), end = "")
    print("") 
print("\n")


print ("Policy from value iteration ::\n")
for i in range (4):
    for j in range(4):
        print("{} ".format(grid.actions[policy[grid.get_state(state(i, j))]]), end = "")
    print("") 


print ("\nPolicy from policy iteration ::\n")
for i in range (4):
    for j in range(4):
       pass
       #print("{} ".format(grid.actions[policy2[grid.get_state(state(i, j))]]), end = "")
    print("") 
