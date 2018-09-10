"""

Arko Sharma
111601002

Lab 6 :
10-09-2018
         
"""
import numpy as np
from scipy.spatial import distance
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
          print "Grid :: "
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
      Returns Euclidean Distance of a point from goal
      """
      def EuclideanDistance(self,i,j): 
          goal_loc = (0,self.dimension - 1)
          return distance.euclidean((i,j),goal_loc)

      """
      Returns Manhattan Distance of a point from goal
      """
      def ManhattanDistance(self,i,j): 
          goal_loc = (0,self.dimension - 1)
          return (abs(i-goal_loc[0])+ abs(j-goal_loc[1]))


      """ 
      Runs A-star search algorithm with 4 movements where heuristic value is Euclidean distance 
      """
      def A_star_4EuclideanHeuristic(self):
 
          dx = [1,0,-1,0]
          dy = [0,-1,0,1]
          explored_list = []
          start = (self.dimension - 1,0)
          Q = Queue.PriorityQueue()
          #g - actual distance till now
          INF = 1000000000
          g = [ [ INF for x in range (self.dimension)]  for y in range (self.dimension)] 

          parent = [ [ (-1,-1) for x in range (self.dimension)]  for y in range (self.dimension)] 

          # For the start state, g + h value is 0
          # Push the source into the priority queue alongwith the g + h value
          Q.put((0 + self.EuclideanDistance(start[0],start[1]),start))
          parent[start[0]][start[1]] = start
          g[start[0]][start[1]] = 0
          

          # Dijkstra's algorithm run...
          while(not (Q.empty())):

              path = []
	      pop = Q.get()
              s = pop[1]
              # the real distance of the popped vertex is stored in dist_s
              dist_s = g[s[0]][s[1]] 
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
                             
                             #child's g-value is parent's distance plus 1
                             g_child = dist_s + 1
                             h_child = self.EuclideanDistance(s[0] + dx[i],s[1] + dy[i])
                             
                             # Add this child to the fringe if the new (g + h) value is less than earlier (g + h) value
                             # Since h value is fixed, comparing only g-values
                             if( g_child  < g[s[0]+dx[i]][s[1]+dy[i]] ):
                                 parent[s[0] + dx[i]][s[1] + dy[i]] = s
                                 # update the g-value (real distance)
                                 g[s[0]+dx[i]][s[1]+dy[i]] = dist_s + 1                          
                                 # push the child with g + h - value
         	                 Q.put((g_child + h_child,(s[0]+dx[i],s[1]+dy[i])))   	   

                  #after expanding all the children , mark the node as explored
                  explored_list.append(s)
                  
          current = (self.goal_r,self.goal_c)
          while(not (current == parent[current[0]][current[1]])):
              
              path.append(current) 
              current = parent[current[0]][current[1]]
         
          path.append(current)
          path = path[::-1]
          print ("\nFor A-star with 4 actions and Euclidean dist. as heuristic, Goal reached in {} steps( defined as length of explored list).".format(len(explored_list)))
          print (" Path :: ")
          print path
          print ("length of path = {}".format(len(path)))



      """ 
      Runs A-star search algorithm with 8 movements where heuristic value is Euclidean distance 
      """
      def A_star_8EuclideanHeuristic(self):
 
          dx = [1,0,-1,0,1,1,-1,-1]
          dy = [0,-1,0,1,1,-1,1,-1]
          explored_list = []
          start = (self.dimension - 1,0)
          Q = Queue.PriorityQueue()
          #g - actual distance till now
          INF = 1000000000
          g = [ [ INF for x in range (self.dimension)]  for y in range (self.dimension)] 

          parent = [ [ (-1,-1) for x in range (self.dimension)]  for y in range (self.dimension)] 

          # For the start state, g + h value is 0
          # Push the source into the priority queue alongwith the g + h value
          Q.put((0 + self.EuclideanDistance(start[0],start[1]),start))
          parent[start[0]][start[1]] = start
          g[start[0]][start[1]] = 0
          

          # Dijkstra's algorithm run...
          while(not (Q.empty())):

              path = []
	      pop = Q.get()
              s = pop[1]
              # the real distance of the popped vertex is stored in dist_s
              dist_s = g[s[0]][s[1]] 
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
                             
                             #child's g-value is parent's distance plus 1
                             g_child = dist_s + 1
                             h_child = self.EuclideanDistance(s[0] + dx[i],s[1] + dy[i])
                             
                             # Add this child to the fringe if the new (g + h) value is less than earlier (g + h) value
                             # Since h value is fixed, comparing only g-values
                             if( g_child  < g[s[0]+dx[i]][s[1]+dy[i]] ):
                                 parent[s[0] + dx[i]][s[1] + dy[i]] = s
                                 # update the g-value (real distance)
                                 g[s[0]+dx[i]][s[1]+dy[i]] = dist_s + 1                          
                                 # push the child with g + h - value
         	                 Q.put((g_child + h_child,(s[0]+dx[i],s[1]+dy[i])))   	   

                  #after expanding all the children , mark the node as explored
                  explored_list.append(s)
                  
          current = (self.goal_r,self.goal_c)
          while(not (current == parent[current[0]][current[1]])):
              
              path.append(current) 
              current = parent[current[0]][current[1]]
         
          path.append(current)
          path = path[::-1]
          print ("\nFor A-star with 8 actions and Euclidean dist. as heuristic, Goal reached in {} steps( defined as length of explored list).".format(len(explored_list)))
          print (" Path :: ")
          print path
          print ("length of path = {}".format(len(path)))



      """ 
      Runs A-star search algorithm with 4 movements where heuristic value is Manhattan distance 
      """
      def A_star_4ManhattanHeuristic(self):
 
          dx = [1,0,-1,0]
          dy = [0,-1,0,1]
          explored_list = []
          start = (self.dimension - 1,0)
          Q = Queue.PriorityQueue()
          #g - actual distance till now
          INF = 1000000000
          g = [ [ INF for x in range (self.dimension)]  for y in range (self.dimension)] 

          parent = [ [ (-1,-1) for x in range (self.dimension)]  for y in range (self.dimension)] 

          # For the start state, g + h value is 0
          # Push the source into the priority queue alongwith the g + h value
          Q.put((0 + self.ManhattanDistance(start[0],start[1]),start))
          parent[start[0]][start[1]] = start
          g[start[0]][start[1]] = 0
          

          # Dijkstra's algorithm run...
          while(not (Q.empty())):

              path = []
	      pop = Q.get()
              s = pop[1]
              # the real distance of the popped vertex is stored in dist_s
              dist_s = g[s[0]][s[1]] 
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
                             
                             #child's g-value is parent's distance plus 1
                             g_child = dist_s + 1
                             h_child = self.ManhattanDistance(s[0] + dx[i],s[1] + dy[i])
                             
                             # Add this child to the fringe if the new (g + h) value is less than earlier (g + h) value
                             # Since h value is fixed, comparing only g-values
                             if( g_child  < g[s[0]+dx[i]][s[1]+dy[i]] ):
                                 parent[s[0] + dx[i]][s[1] + dy[i]] = s
                                 # update the g-value (real distance)
                                 g[s[0]+dx[i]][s[1]+dy[i]] = dist_s + 1                          
                                 # push the child with g + h - value
         	                 Q.put((g_child + h_child,(s[0]+dx[i],s[1]+dy[i])))   	   

                  #after expanding all the children , mark the node as explored
                  explored_list.append(s)
                  
          current = (self.goal_r,self.goal_c)
          while(not (current == parent[current[0]][current[1]])):
              
              path.append(current) 
              current = parent[current[0]][current[1]]
         
          path.append(current)
          path = path[::-1]
          print ("\nFor A-star with 4 actions and Manhattan dist. as heuristic, Goal reached in {} steps( defined as length of explored list).".format(len(explored_list)))
          print (" Path :: ")
          print path
          print ("length of path = {}".format(len(path)))



      """ 
      Runs A-star search algorithm with 8 movements where heuristic value is Manhattan distance.
      This may not return the optimal path because Manhattan distance is not admissible with diagonal moves allowed.
      """
      def A_star_8ManhattanHeuristic(self):
 
          dx = [1,0,-1,0,1,1,-1,-1]
          dy = [0,-1,0,1,1,-1,1,-1]


          # we can't use explored list since heuristic is not consitent.
          start = (self.dimension - 1,0)
          Q = Queue.PriorityQueue()
          #g - actual distance till now
          INF = 1000000000
          g = [ [ INF for x in range (self.dimension)]  for y in range (self.dimension)] 

          parent = [ [ (-1,-1) for x in range (self.dimension)]  for y in range (self.dimension)] 

          # For the start state, g + h value is 0
          # Push the source into the priority queue alongwith the g + h value
          Q.put((0 + self.ManhattanDistance(start[0],start[1]),start))
          parent[start[0]][start[1]] = start
          g[start[0]][start[1]] = 0
          steps = 0

          # Dijkstra's algorithm run...
          while(not (Q.empty())):
             
              steps += 1
              path = []
	      pop = Q.get()
              s = pop[1]
              # the real distance of the popped vertex is stored in dist_s
              dist_s = g[s[0]][s[1]]

 
              # We cannot stop if we reach the goal state. We need to continue till the queue(fringe) is empty.
              # If the ( g + h ) score of the popped node is greater than the distance of the goal, we just continue.
              # Otherwise we expand as there can be scope for improvement. 
              h_s = self.ManhattanDistance(s[0],s[1])
              if(dist_s + h_s >= g[self.goal_r][self.goal_c]):
                  continue

	                 
              for i in range(8):
	          if  ( self.is_valid(s[0],s[1],dx[i],dy[i])):
                      #child's g-value is parent's distance plus 1
                      g_child = dist_s + 1
                      h_child = self.ManhattanDistance(s[0] + dx[i],s[1] + dy[i])
                            
                      # Add this child to the fringe if the new (g + h) value is less than earlier (g + h) value
                      # Since h value is fixed, comparing only g-values
                      if  ( g_child  < g[s[0]+dx[i]][s[1]+dy[i]] ):
                          parent[s[0] + dx[i]][s[1] + dy[i]] = s
                          # update the g-value (real distance)
                          g[s[0]+dx[i]][s[1]+dy[i]] = dist_s + 1                          
                          # push the child with g + h - value
                          Q.put((g_child + h_child,(s[0]+dx[i],s[1]+dy[i])))   	   

                  
          current = (self.goal_r,self.goal_c)
          while(not (current == parent[current[0]][current[1]])):
              
              path.append(current) 
              current = parent[current[0]][current[1]]
         
          path.append(current)
          path = path[::-1]
          print ("\nFor A-star with 8 actions and Manhattan dist. as heuristic, Goal reached in {} steps( defined as number of runs of the while loop.).".format(steps))
          print (" Path :: ")
          print path
          print ("length of path = {}".format(len(path)))

myenv = Environment(40)
myenv.A_star_4EuclideanHeuristic()
myenv.A_star_8EuclideanHeuristic()
myenv.A_star_4ManhattanHeuristic()
myenv.A_star_8ManhattanHeuristic()
