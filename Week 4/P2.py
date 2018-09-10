"""

Arko Sharma
111601002

Lab 4 :: P2 : Grid with blockages.
         
"""
import numpy as np
import Queue
class Environment:
      """ 
      This environment is a grid containing randomly selected start and goal cells.
      There are certain blockages ( sub-grids containing 1) which are generated randomly and
      cannot be traversed.
      It is ensured that there exists at least one path between start and goal cells.
      """
      


      """ 
      Function to indicate whether a given action is valid, given the starting position and action
      """
      def is_valid(self,curr_r,curr_c,act_r,act_c):
          new_r = curr_r + act_r
          new_c = curr_c + act_c
          if  ( new_r >= 0 and new_r < self.dimension and new_c >= 0 and new_c < self.dimension ):
              return True
          else:
              return False



      """
      Runs a  BFS from start to goal ignoring the blockages and makes all cells in the path = 0
      It basically ensures the existence of a path from start to goal.
      """
      def BFS(self):

          path = [] 
          parent = [ [ (-1,-1) for x in range (self.dimension)]  for y in range (self.dimension)]
          dx = [1,0,-1,0]
          dy = [0,-1,0,1]
          explored_list = []
          start = (self.start_r,self.start_c)
          parent[start[0]][start[1]] = start
          Q = Queue.Queue()
          Q.put(start)
          while(not (Q.empty())):
              
	      s = Q.get()
              explored = False

              #check if the goal state has been reached
              if (self.goal_r == s[0] and self.goal_c == s[1]):
                  break    	                 

	      # Expand if current cell has not already been explored
              # This check is necessary because multiple instances of this cell could have been pushed when it was not explored
              if  (s not in explored_list):
                  for i in range(4):
	              if ( self.is_valid(s[0],s[1],dx[i],dy[i])):
                         #note that if the child is invalid OR its parent has been set, then it is not pushed in the Queue
                         if  ( parent[s[0]+dx[i]][s[1]+dy[i]] == (-1,-1)  ):
                             parent[s[0] + dx[i]][s[1] + dy[i]] = s
         	             Q.put((s[0]+dx[i],s[1]+dy[i]))

                  #after expanding all the children , mark the node as explored
                  explored_list.append(s)

          #Constructing the path
          current = (self.goal_r,self.goal_c)
          while(not (current == parent[current[0]][current[1]])):
              
              self.grid[current[0]][current[1]] = 0
              path.append(current) 
              current = parent[current[0]][current[1]]
         
          self.grid[current[0]][current[1]] = 0
          path.append(current)
          path = path[::-1]
          return path             

     
      def __init__(self,dimension):
          
          self.dimension = dimension
          self.grid = np.zeros([dimension,dimension])
          
          # creating start and goal cells
          while(True):
              self.start_r = np.random.randint(self.dimension)
              self.start_c = np.random.randint(self.dimension)
              self.goal_r =  np.random.randint(self.dimension)
              self.goal_c =  np.random.randint(self.dimension)
              if  (not(self.start_r == self.goal_r and self.start_c == self.goal_c)): 
                  break
          
          # creating blockages
          for i in range (2):
              centre = np.random.randint(self.dimension)
              size = np.random.randint(self.dimension)
              for j in range(centre - size, centre + size + 1):
                  for k in range(centre - size, centre + size + 1):
                      if  (self.is_valid(j,k,0,0)):
                          self.grid[j][k] = 1

          print ("Start = {}".format((self.start_r,self.start_c)))
          print ("Goal = {}".format((self.goal_r,self.goal_c)))
        
          
          #ensuring path from start to goal
          path = self.BFS()
           
          print ("Grid ::")
          for i in range(dimension):
	      print self.grid[i]          
          
          print ("Path is as follows :: ")
          print path

#creating an instance of the environment ::
myenv = Environment(100)
