"""
Description
An underpowered car must climb a one-dimensional hill to reach a target.
The target is on top of a hill on the right-hand side of the car (0.6) . If the car reaches it or goes beyond 0.56, the episode terminates.
On the left-hand side, there is another hill. Climbing this hill can be used to gain potential energy and accelerate towards the target.
On top of this second hill, the car cannot go further than a position equal to -1.2 , as  if there was a wall. Hitting this limit does not generate 
a penalty (it might in a more challenging version).
Update equations :
v(t + 1) = v(t) + acc(t) * 0.001  + (cos( 3 * pos(t)) (-0.0025)
pos(t)   = pos(t) * vel(t)
acc      = (-1, 0 ,1)
gamma    = 0.99
v        = (-0.07, 0.07)
reward   = 1 if goal state is reached
         = 0 otherwise
The agenda is to find an optimum policy , ie given a position and a velocity, find the value of acceleration.
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
import math
import random

class state:
      
    #state defined by current position and current velocity
    def __init__(self, p, v):
        self.p = p
        self.v = v
          
          
class MDP_MountainCar():
    
    """
    This is the mountain-car environment for a MDP problem.
    The state is defined by the position and velocity of the car.
    For each state, 3 actions are allowed corresponding to 3 possible values of acceleration.
    
    There is a transition-probability matrix "T" which gives a list of states
    reachable on a particular action at a particular state , alongwith the probability of
    of this transition.        
  
    There are Reward and Actions matrices representing the MDP setting. 
    """

    
    def __init__(self):
        self.positions  = range(-12, 6)
        self.velocities = range(-7, 7)
        self.gamma = 0.99
        self.T = {}
        self.R = {}
        self.actions  = ["d", "m", "a","s"]
        # d - decelerate
        # m - maintain_speed
        # a - accelerate
        # s - stop
        self.dx_act = {}
        self.dx_act["d"]     = -1
        self.dx_act["m"]     =  0
        self.dx_act["a"]     =  1
        self.dx_act["s"]     =  0 #this value is irrelevant
        
        self.states = []
        
        #discretizing the values -- position : -120 to 60
        #                        -- velocity : -70  to 70
        for i in range (-12, 6):
            for j in range (-7, 7):
                self.states.append(state(i, j))

        self.generate_TransitionProbabilityMatrix(self.states, self.actions)
        self.generate_RewardMatrix(self.states, self.actions)

        


    def get_state(self, some_state):
        """
        Function to return that state of the MDP which has the given values of the state variables
        """
        for s in self.states:
            if (s.p == some_state.p and s.v == some_state.v):
                return s
        
    def generate_RewardMatrix(self, states, actions):
        
        """
        Function used to generate R.
        Here R is a function of the next state only.
        If the next state is goal state, then a reward of 1 is provided, else the reward is 0.
        """
        
        for s in states:
     
     
            for a in actions:
                #first put terminating condition 
                #once on top of the mountain, only maintain speed .
                if (s.p > 5.6):
                    if(a == "m"):
                        self.R[(s,a)] =     
                    
                    
                    self.R[(s,a)] = -1000000000000
                    continue
            
                    
                #if going from non-goal to goal-state, award 1                 
                if(self.T[(a,s)][0][0].p > 5.6) : 
                    self.R[(s, a)] = 1
                else:
                    self.R[(s, a)] = -1



    def generate_TransitionProbabilityMatrix(self, states, actions):
        
        """
        Function used to generate T.
        Here the transition on an action is deterministic.
        
        v(t + 1) = v(t) + acc(t) * 0.001  + cos( 3 * pos(t)) (-0.0025)
        pos(t)   = pos(t) * vel(t)
        The values are rounded up and discretized.
        """
        
        k = 0
        for s in states:
            for a in actions:
             
                k += 1
                print(k)
                v_next = round( ((s.v/100.0) + self.dx_act[a] * 0.001 + math.cos(3.0 * s.p / 100.0) * (-0.0025 ) )* 100) 
                
                if (v_next < -7):
                    v_next = -7
                if (v_next > 7):
                    v_next = 7
                p_next = round(s.p * v_next / 100.0)
                
                if (p_next < -12):
                    p_next = -12
                if (p_next > 6):
                    p_next = 6      
       
                v = int(v_next)
                p = int(p_next)
                success     = 1
                succ_neigh  = state(p, v)
                self.T[(a, s)] = [(self.get_state(succ_neigh), success)]
                                                            
        
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


            for i in  (mdp_grid.positions):
                for j in (mdp_grid.velocities):
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
            policy[s] = np.random.randint(0,3)


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

                





"""
"""

grid      = MDP_MountainCar()
print("hi")
solver    = SolveMDP()

#valueVI, policyVI = (solver.value_iteration(grid, 0.000001))
steps             = 800
#valueDP, policyDP = solver.DP_FiniteHorizon(grid, steps)



valuePI, policyPI = (solver.policy_iteration(grid))

print ("\nOptimal Value Matrix from PolicyIteration  vv\n")
print ("-------------------------------------------------------------------------\n")
for i in grid.positions:
    for j in grid.velocities:
        print("{} ".format(valuePI[ grid.get_state(state(i, j)) ] ), end = "")
    print("") 
print ("-------------------------------------------------------------------------\n")





print ("\nPolicy from policy iteration ::\n")
print ("-------------------------------------------------------------------------\n")
for i in grid.positions:
    for j in grid.velocities:
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
 
          
          
