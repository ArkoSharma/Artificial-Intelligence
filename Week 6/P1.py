"""

Arko Sharma
111601002

Lab 6 :
03-09-2018
         
"""
import numpy as np
import Queue
class Environment:
      
      """ 

      The environment is initially in a state in which starting position is in the lower left corner.
      The goal cell is the upper right corner.
      The environment records the number of steps taken to search the goal.

      There is an explored list which keeps track of the explored NODES of the program graph (denoted by the cell which is being explored currently ).
      """
 

      def __init__(self,dimension):
          
          self.dimension = dimension
          self.grid = np.zeros([dimension,dimension])
          self.goal_r = 0
          self.goal_c = dimension - 1
	
          #create diagonal blockages
          for i in range (self.dimension) : 
              for j in range (self.dimension) :
                  if( i == j ):
                      self.grid[i][j] = 1
           	      if  ( j < dimension - 1) : 
                          self.grid[i][j+1] = 1

          self.grid[0][0] = 0
          self.grid[0][1] = 0
          for i in range(dimension):
	      print self.grid[i]          


      """ 
      Function to indicate whether a given action is valid, given the starting position
      """
      def is_valid(self,curr_r,curr_c,act_r,act_c):
          new_r = curr_r + act_r
          new_c = curr_c + act_c
          if  ( new_r >= 0 and new_r < self.dimension and new_c >= 0 and new_c < self.dimension and self.grid[new_r][new_c] != 1):
              return True
          else:
              return False


      """
      The environment implements a  cost function which returns 1 for each action that moves
      to a non-goal cell and 0 for those which do not.
      """
      def cost(self,curr_r,curr_c,act_r,act_c):
          new_r = curr_r + act_r
          new_c = curr_c + act_c
          if  ( new_r == self.goal_r and new_c == self.goal_c):
              return 0
          else:
              return 1

      """ 
      Runs a BFS with 4 moves possible along the four directions : up,down,left,right.
      Returns the number of steps required to search the goal cell.
      """

      def BFS_4(self):
 
          dx = [1,0,-1,0]
          dy = [0,-1,0,1]
          explored_list = []
          start = (self.dimension - 1,0)
          Q = Queue.Queue()
          Q.put(start)
          while(not (Q.empty())):
              
	      s = Q.get()
              explored = False

              #check if the goal state has been reached
              if (self.cost(s[0],s[1],0,0) == 0):
                  explored_list.append(s)
                  break    	                 

	      # Expand if current cell has not already been explored
              # This check is necessary because multiple instances of this cell could have been pushed when it was not explored
              if  (s not in explored_list):
                  for i in range(4):
	              if ( self.is_valid(s[0],s[1],dx[i],dy[i])):
                         #note that if the child is invalid OR EXPLORED BEFORE, then it is not pushed in the Queue
                         if  ( (s[0] + dx[i], s[1] + dy[i]) not in explored_list ):
         	             Q.put((s[0]+dx[i],s[1]+dy[i]))   	   

                  #after expanding all the children , mark the node as explored
                  explored_list.append(s)
              
	  print("\nWith 4 Actions,Exploration takes place as follows : ")
          temp = np.zeros([self.dimension,self.dimension])
          for i in range(len(explored_list)):
              current = explored_list[i]
              temp[current[0]][current[1]] = 1
              print("Visiting {}".format(current))
              print temp
              print("########################")    

          return ("For BFS with 4 actions, Goal reached in {} steps.".format(len(explored_list)))


      """ 
      Modified BFS with diagonal moves possible alongwith the four cardinal directions.
      Returns the number of steps required to search the goal cell.
      """
      def BFS_8(self):
 
          dx = [1,0,-1,0,1,1,-1,-1]
          dy = [0,-1,0,1,1,-1,1,-1]
          explored_list = []
          #starting location pushed into queue
          start = (self.dimension - 1,0)
          Q = Queue.Queue()
          Q.put(start)
	  count = 0
          while(not (Q.empty())):
              
	      s = Q.get()
              explored = False

              #check if the goal state has been reached
              if (self.cost(s[0],s[1],0,0) == 0):
                  explored_list.append(s)
                  break    	                 
             
              # Expand if current cell has not already been explored
              # This check is necessary because multiple instances of this cell could have been pushed when it was not explored
              if  (s not in explored_list):
                  for i in range(8):
	              if ( self.is_valid(s[0],s[1],dx[i],dy[i])):
                         #note that if the child is invalid OR EXPLORED BEFORE, then it is not pushed in the Queue
                         if  ( (s[0] + dx[i], s[1] + dy[i]) not in explored_list ):
         	             Q.put((s[0]+dx[i],s[1]+dy[i]))   	   

                  #after expanding all the children , mark the node as explored
                  explored_list.append(s)
              
	  print("\nWith 8 Actions, Exploration takes place as follows : ")
          temp = np.zeros([self.dimension,self.dimension])
          for i in range(len(explored_list)):
              current = explored_list[i]
              temp[current[0]][current[1]] = 1
              print("Visiting {}".format(current))
              print temp
              print("########################")    

          return ("For BFS with 8 actions, Goal reached in {} steps.".format(len(explored_list)))


myenv = Environment(15)
msg4_ = (myenv.BFS_4())
msg8_ = (myenv.BFS_8())
print msg4_
print msg8_
