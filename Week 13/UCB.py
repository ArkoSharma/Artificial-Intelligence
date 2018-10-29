from __future__ import print_function
import numpy as np 

class UCB():
    
    """
    Upper - confidence bound algorithm implementation.
    """

    def __init__(self,K,T):
        self.K = K
        self.T = T

        self.means = []  # stores the means of the reward distributions for each action (Arm)
        for i in range K:

        	self.means.append(np.random.uniform(0,1))
        	self.R = np.random.binomial(1, mean[i], T)

        	
