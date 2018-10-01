"""
Arko Sharma
01.10.2018
Program depicting Value iteration and Policy iteration in a grid world environment.
Here the reward is a function of the current state only ie a constant reward is assumed to
be obtained upon reaching a state.
"""
from __future__ import print_function
import numpy as np

class state:
      
    def __init__(self,r,c):
        self.r = r
        self.c = c
          
          
class MDP_grid():
    
    """
    This is a grid environment for a MDP problem.
    The state is defined by the location of the agent in the grid.
    For each state, 4 actions are allowed - movement in the 4 directions.
    Also for each state is associated a 4x4 matrix A ; where Aij is the probability
    of moving in direction "j" upon having selected direction "i".This depicts the randomness
    of a real - world scenario.
    """

    
    def __init__(self,dimension,gamma):
        self.dimension = dimension
        self.gamma = gamma
        self.T = {}
        self.R = {}
        self.actions = ["u","d","l","r"]
        self.states = []
        for i in range (self.dimension):
            for j in range (self.dimension):
                self.states.append(state(i,j))
                
        self.generate_random_TransitionProbabilityMatrix(self.states,self.actions)
        self.generate_random_RewardMatrix(self.states,self.actions)
        
    def generate_random_RewardMatrix(self,states,actions):
        #Function used to generate R
        #Here, R is only a function of state ie each state has a fixed incoming reward.
        
        for s in states:
            self.R[s] = np.random.randint(-100,100)
        print ("Rewards:")
        k = 0
        for s in states:
            print (self.R[s],end = ' ')
            k += 1
            if (k + 1 % 4 == 0):
                print("")
                k = 0
        
    def generate_random_TransitionProbabilityMatrix(self,states,actions):
        # Function used to generated P.
        # Assumed that the agent moves only to the 4 adjoining cells with non zero probability.
        # Movement to any state that is does not share a side with current is 0.
        for s in states:
            
            #up
            success = np.random.uniform(0.7,1.0)
            if (s.r == 0):
                success = 0             
            remaining = 1.0 - success
            fail = remaining/3
            self.T[("u",s) ] = []
            self.T[("u",s) ].append((state(s.r - 1, s.c),success))
            self.T[("u",s) ].append((state(s.r + 1, s.c),fail))
            self.T[("u",s) ].append((state(s.r , s.c - 1),fail))
            self.T[("u",s) ].append((state(s.r , s.c - 1),fail))

            #down
            success = np.random.uniform(0.7,1.0)
            if (s.r == self.dimension - 1): 
                success = 0             
            remaining = 1.0 - success
            fail = remaining/3
            self.T[("d",s) ] = []
            self.T[("d",s) ].append((state(s.r - 1, s.c),fail))
            self.T[("d",s) ].append((state(s.r + 1, s.c),success))
            self.T[("d",s) ].append((state(s.r , s.c - 1),fail))
            self.T[("d",s) ].append((state(s.r , s.c - 1),fail))
            
            #left
            success = np.random.uniform(0.7,1.0)
            if (s.c == 0): 
                success = 0             
            remaining = 1.0 - success
            fail = remaining/3
            self.T[("l",s) ] = []
            self.T[("l",s) ].append((state(s.r - 1, s.c),fail))
            self.T[("l",s) ].append((state(s.r + 1, s.c),fail))
            self.T[("l",s) ].append((state(s.r , s.c - 1),success))
            self.T[("l",s) ].append((state(s.r , s.c - 1),fail))
            
            #right        
            success = np.random.uniform(0.7,1.0)
            if (s.c == self.dimension - 1): 
                success = 0             
            success = np.random.uniform(0.7,1.0)
            remaining = 1.0 - success
            fail = remaining/3
            self.T[("r",s) ] = []
            self.T[("r",s) ].append((state(s.r - 1, s.c),fail))
            self.T[("r",s) ].append((state(s.r + 1, s.c),fail))
            self.T[("r",s) ].append((state(s.r , s.c - 1),fail))
            self.T[("r",s) ].append((state(s.r , s.c - 1),success))
               
        
        
class SolveMDP:
    
    """
    Solver Class to solve MDP and return optimal policy.
    Method : Value Iteration and Policy Iteration.
    """
    def __init__(self):
        pass
  
    def value_iteration(self,mdp_grid):
        """Solving an MDP by value iteration. [Figure 17.4]"""

        #define random Values	
        V = {}
        policy = {}
        T,R,gamma = mdp_grid.T,mdp_grid.R,mdp_grid.gamma

        for s in mdp_grid.states:
            V[s] = np.random.randint(-1000,1001)
       
        while(True):
            V_copy = V.copy()
            delta = 0
            for s in mdp_grid.states:
                Q = []
                
                for a in mdp_grid.actions:
                    for (next_state, prob) in T[(a,s)])
                        sum += gamma * (prob * V_copy[next_state]))
                    Q.append(R[s] + sum, 
                V[s] = np.max(Q)
                policy[s] = np.argmax[Q] 
                
            delta = max(delta, np.abs(V[s] - V_copy[s]))
            if  delta <= epsilon*(1 - gamma)/gamma:
                return policy

grid     = MDP_grid(4,0.9)
solver   = SolveMDP()
print(solver.value_iteration(grid))
