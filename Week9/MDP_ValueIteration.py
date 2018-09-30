"""
Program depicting Value iteration and Policy iteration in a grid world environment.
Here the reward is a function of the current state only ie a constant reward is assumed to
be obtained upon .
"""

import numpy as np
class Environment:
    
    """
    This is a grid environment for a MDP problem.

    The state is defined by the location of the agent in the grid.

    For each state, 4 actions are allowed - movement in the 4 directions.
    Also for each state is associated a 4x4 matrix A ; where Aij is the probability
    of moving in direction "j" upon having selected direction "i".This depicts the randomness
    of a real - world scenario.
    """
