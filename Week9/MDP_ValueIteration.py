"""
Arko Sharma
01.10.2018
Program depicting Value iteration and Policy iteration in a grid world environment.
Here the reward is a function of the current state only ie a constant reward is assumed to
be obtained upon reaching a state.


issues :
       probabilities of illegal moves to be el.
       check value iteration and do viBottUP
       do policy iteration
       blocks
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
        self.actions  = ["u","d","l","r"]
        self.dxdy_act = {}
        self.dxdy_act["u"] = (-1,0)
        self.dxdy_act["d"] = (1,0)
        self.dxdy_act["l"] = (0,-1)
        self.dxdy_act["r"] = (0,1)
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
            self.R[s] = np.random.randint(-10,11)
        print ("Rewards:")
        k = 0
        for s in states:
            print (self.R[s],end = ' ')
            k += 1
            if (k + 1 % 4 == 0):
                print("")
                k = 0

    def inside_board(self,state):
        r,c = state.r,state.c
        if(r >= 0 and r < self.dimension and c >=0 and c < self.dimension):
            return True
        else: 
            return False

    def get_state(self,some_state):
        #Function to return that state of the MDP which has the given state values of the state variables
        for s in self.states:
            if (s.r == some_state.r and s.c == some_state.c):
                return s
        
    def generate_random_TransitionProbabilityMatrix(self,states,actions):
        # Function used to generate T.
        # Assumed that the agent moves only to the 4 adjoining cells with non zero probability.
        # Movement to any state(cell) that does not share a side with current is impossible.

        dx = [1,0,-1,0]
        dy = [0,1,0,-1]
        

        for s in states:
            for a in actions:
                valid_neighbours = []

                success     = np.random.uniform(0.7,1.0)
                succ_neigh  = state(self.dxdy_act[a][0] + s.r , self.dxdy_act[a][1] + s.c)
                if(not(self.inside_board(succ_neigh))):
                    success = 0
          
                for x in dx:
                    for y in dy:
                        neighbour = state(s.r + x, s.c + y)
                        if (self.inside_board(neighbour) and neighbour != succ_neigh):
                            valid_neighbours.append(self.get_state(neighbour))
               
                fail          = (1 - success)/len(valid_neighbours)
                self.T[(a,s)] = []
                for val_neigh in valid_neighbours:
                    self.T[(a,s)].append((val_neigh,fail))
                
                if (success != 0):
                    self.T[(a,s)].append((self.get_state(succ_neigh),success))                 
                                                     
        
class SolveMDP:
    
    """
    Solver Class to solve MDP and return optimal policy.
    Method : Value Iteration and Policy Iteration.
    """
    def __init__(self):
        pass
  
    def value_iteration(self,mdp_grid,epsilon):
        """Solving an MDP by value iteration.
           Starting with random V and iterating till convergence.
        """

        #define random Values	
        V = {}
        policy = {}
        T,R,gamma = mdp_grid.T,mdp_grid.R,mdp_grid.gamma

        for s in mdp_grid.states:
            V[s] = np.random.randint(-10,11)
       
        while(True):
            V_copy = V.copy()
            delta = 0
            for s in mdp_grid.states:
                Q = []
                for a in mdp_grid.actions:
                    acc = 0
                    for (next_state, prob) in T[(a,s)]:
                        acc += prob*V_copy[next_state]
                    Q.append(R[s] + gamma*acc) 
                V[s] = np.max(Q)
                policy[s] = np.argmax(Q) 


                for i in range (mdp_grid.dimension):
                    for j in range(mdp_grid.dimension):
                        print ("{} ".format(V[mdp_grid.get_state(state(i,j))]),end = "")
                    print("")
                print("\n\n")
                

            delta = max(delta, np.abs(V[s] - V_copy[s]))
            if  delta <= epsilon*(1 - gamma)/gamma:
                return policy


                
    def value_iterationBottomUp(self,mdp_grid,epsilon):
        """Solving an MDP by value iteration.
           Building table bottom up.
        """
        #Fill Table


grid     = MDP_grid(4,0.9)
solver   = SolveMDP()
policy   = (solver.value_iteration(grid,0.00001))
for i in range (4):
    for j in range(4):
        print("{} ".format(grid.actions[policy[grid.get_state(state(i,j))]]),end = "")
    print("")   

