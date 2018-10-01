"""
Arko Sharma
01.10.2018


Program depicting Value iteration and Policy iteration in a grid world environment.
Here the reward is a function of the current state only ie a constant reward is assumed to
be obtained upon reaching a state.
"""

import numpy as np

class State:
      
    def __init__(r,c):
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

    
    def __init__(self,dimension):
        self.n = dimension
        self.P = {}
        self.R = {}
        self.actions = ["u","d","l","r"]
        self.states = []
        for i in range self.n:
            for j in range self.n:
                self.states.append(state(i,j))
                
        self.generate_random_probabilityTransitionMatrix(self.states,self.actions)
        self.generate_random_RewardMatrix(self.states,self.actions)
        
    def generate_random_RewardMatrix(self,states,actions):
        #Function used to generate R
        #Here, R is only a function of state ie each state has a fixed incoming reward.
        for s in states:
            R[s] = np.random.randint(-100,100)
        print "Rewards:"
        print "R {} = {}".format(s,R[s])
         
        
    def generate_random_probTransitionMatrix(self,states,actions):
        #Function used to generated P.
        for s in states:
            
            #up
            success = np.random.randfloat(0.7,1.0)
            remaining = 1.0 - success
            fail = remaining/3
            self.P[("u",s,state(self.r - 1, self.c)) ] = success
            self.P[("u",s,state(self.r + 1, self.c)) ] = fail
            self.P[("u",s,state(self.r , self.c - 1))] = fail
            self.P[("u",s,state(self.r , self.c + 1))] = fail
            
            #down
            success = np.random.randfloat(0.7,1.0)
            remaining = 1.0 - success
            fail = remaining/3
            self.P[("d",s,state(self.r - 1, self.c)) ] = fail
            self.P[("d",s,state(self.r + 1, self.c)) ] = success
            self.P[("d",s,state(self.r , self.c - 1))] = fail
            self.P[("d",s,state(self.r , self.c + 1))] = fail
            
            #left
            success = np.random.randfloat(0.7,1.0)
            remaining = 1.0 - success
            fail = remaining/3
            self.P[("l",s,state(self.r - 1, self.c)) ] = fail
            self.P[("l",s,state(self.r + 1, self.c)) ] = fail
            self.P[("l",s,state(self.r , self.c - 1))] = success
            self.P[("l",s,state(self.r , self.c + 1))] = fail
            
            #right        
            success = np.random.randfloat(0.7,1.0)
            remaining = 1.0 - success
            fail = remaining/3
            self.P[("r",s,state(self.r - 1, self.c)) ] = fail
            self.P[("r",s,state(self.r + 1, self.c)) ] = fail
            self.P[("r",s,state(self.r , self.c - 1))] = fail
            self.P[("r",s,state(self.r , self.c + 1))] = success
               
        
        
class SolveMDP:
    
    """
    Solver Class to solve MDP and return optimal policy.
    Method : Value Iteration and Policy Iteration.
    """

    def ValueIteration(self,mdp_instance):
        
        for s in self.states:
            Values = []        
            for a in self.actions:
                
    
