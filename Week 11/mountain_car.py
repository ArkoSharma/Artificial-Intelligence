"""
Description
An underpowered car must climb a one-dimensional hill to reach a target.
Unlike MountainCar v0, the action (engine force applied) is allowed to be a continuous value.

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

"""

from __future__ import print_function
import numpy as np
import copy
import random

class state:
      
    #here the rows represent position and columns represent velocity.
    def __init__(self, p, v):
        self.r = r
        self.c = c
          
          
                                                     
        
