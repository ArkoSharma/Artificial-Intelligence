"""
Arko Sharma
111601002
Test1 :: ( n-squared minus 2 puzzle ) - Solution using Astar with Sum of two blanks' Manhattan Distance as heuristic.
                                        
Both the squares are moved.
Any configuration is considered to be solved as long as 1 to n^2 - 2 are in sorted order in the board
and the two blanks appear in the last two spaces.

Observations ::
 
1. For simple Manhattan distance as heuristic, the correct solution is obtained in all cases.
   But with n = 4 and ( 9 -> 8 , 12 -> 11 ) case, the search takes too much time.

2. When the heuristic is changed to (1.5x or 2x or 3x or 4x) times the Manhattan Distance, few solutions are found
   very quickly.
   But these are not guaranteed to be optimal solutions because the heuristic may be inadmissible.
   The best solution for the above case was found with doubling the Manhattan distance, in 26 steps

3. The time is seen to reduce exponentially with respect to the factor by which the heuristic distance is multiplied.
 
         
"""

import numpy as np
import Queue
import copy
from scipy.spatial import distance
INF = 1000000000
class N2Puzzle:
      """ 
      Initialise the environment with a state which 8 random steps away from the goal destination.
      Run BFS to check whether the search halts.
      
      """
      
      def get_random_2D_direction(self):
          #generate and return randomly permuted numbers from 1 to n-sq
          return np.random.randint(0,4); 
       

      def get_random_permutation(self):
          #generate and return randomly permuted numbers from 1 to n-sq
          return np.random.permutation([x for x in range(1,self.n*self.n+1) ]) 


      def __init__(self,n):
          # populates the board with randomly permuted numbers less than n-squared.
          # the number n-squared denotes the empty square whose location is tracked in the environment.

          self.n = n
          self.n = int(raw_input())
      self.board = np.array([x for x in range(self.n * self.n)]).reshape(self.n,self.n)
      k = 1
      for i in range(self.n):
          for j in range(self.n):
              self.board[i][j] = int(raw_input())
              k += 1
             
      for i in range (self.n):
              for j in range(self.n):
                  if( self.board[i][j] == self.n*self.n ) :
                      self.empty_i = i
                      self.empty_j = j
                  if(self.board[i][j] == self.n*self.n - 1):
                      self.empty2_i = i
                      self.empty2_j = j
          print self.board


      def is_solved(self):
          #function to check if the current state represents the goal state ie a solved board.
          #for doing this, just check if the board is sorted while traversing in row-major order.         
          k = 1          
          for i in range(self.n):
              for j in range(self.n):
                  if  (self.board[i][j] != k ):
                      return False
                  if  k == self.n*self.n - 2 : 
                      break
                  k += 1
          return True          

 

      def move_empty_squares(self,num_square,move_string):
      if(move_string == "up" and num_square == self.n*self.n):
              if(self.empty_i == 0):
                   return
              else :
                   temp = self.board[self.empty_i-1][self.empty_j]
                   self.board[self.empty_i - 1][self.empty_j] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_i -= 1

          if(move_string == "left" and num_square == self.n*self.n):
              if(self.empty_j == 0):
                   return
              else :
                   temp = self.board[self.empty_i][self.empty_j - 1]
                   self.board[self.empty_i][self.empty_j - 1] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_j -= 1

          if(move_string == "down" and num_square == self.n*self.n):
              if(self.empty_i == self.n-1):
                   return
              else :
                   temp = self.board[self.empty_i+1][self.empty_j]
                   self.board[self.empty_i + 1][self.empty_j] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_i += 1

          if(move_string == "right" and num_square == self.n*self.n):
              if(self.empty_j == self.n-1):
                   return
              else :
                   temp = self.board[self.empty_i][self.empty_j + 1]
                   self.board[self.empty_i ][self.empty_j + 1] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_j += 1

          if(move_string == "up" and num_square == self.n*self.n -1 ):
              if(self.empty2_i == 0):
                   return
              else :
                   temp = self.board[self.empty2_i-1][self.empty2_j]
                   self.board[self.empty2_i - 1][self.empty2_j] = self.n * self.n-1
                   self.board[self.empty2_i][self.empty2_j] = temp
                   self.empty2_i -= 1

          if(move_string == "left" and num_square == self.n*self.n -1 ):
              if(self.empty2_j == 0):
                   return
              else :
                   temp = self.board[self.empty2_i][self.empty2_j - 1]
                   self.board[self.empty2_i][self.empty2_j - 1] = self.n * self.n-1
                   self.board[self.empty2_i][self.empty2_j] = temp
                   self.empty2_j -= 1

          if(move_string == "down" and num_square == self.n*self.n -1 ):
              if(self.empty2_i == self.n-1):
                   return
              else :
                   temp = self.board[self.empty2_i+1][self.empty2_j]
                   self.board[self.empty2_i + 1][self.empty2_j] = self.n * self.n-1
                   self.board[self.empty2_i][self.empty2_j] = temp
                   self.empty2_i += 1

          if(move_string == "right" and num_square == self.n*self.n -1):
              if(self.empty2_j == self.n-1):
                   return
              else :
                   temp = self.board[self.empty2_i][self.empty2_j + 1]
                   self.board[self.empty2_i ][self.empty2_j + 1] = self.n * self.n -1
                   self.board[self.empty2_i][self.empty2_j] = temp
                   self.empty2_j += 1
          #update the values of the locations of the two blanks.
      for i in range (self.n):
              for j in range(self.n):
                  if( self.board[i][j] == self.n*self.n ) :
                      self.empty_i = i
                      self.empty_j = j
                  if(self.board[i][j] == self.n*self.n - 1):
                      self.empty2_i = i
                      self.empty2_j = j
                   


      def gen_xstep_board(self,x_steps):
      #generates a board that is at most "x_steps" moves away from the destination
          direction = ["up", "down", "left", "right"]
          for i in range(x_steps):
              d = np.random.randint(4)
              self.move_empty_square(direction[d])
      print("{}".format(self.board)) 


      def show_parity(self):
          #function to calculate and show the parity as defined in the question.
      #bottom right is in location(n-1,n-1)
          d_s = (self.n-1-self.empty_i) + (self.n - 1 - self.empty_j)
          counter = 0
      for i in range(0,self.n):
              for j in range(0,self.n):
                  for k in range(0,self.n):
                      for l in range(0,self.n):
  
                          if( k>i or (k==i and l>j)):
                              if(self.board[k][l] < self.board[i][j]):
                                 counter += 1
                  
     
          return ((d_s + counter)%2)
          #print("Empty location = ({},{})".format(self.empty_i,self.empty_j))
          #print("{}".format(self.board)) 

      def Manhattan_sum(self):
          #function to calculate and show the parity as defined in the question.
      #bottom right is in location(n-1,n-1)
          d_s1 = (self.n-1-self.empty_i) + (self.n - 1 - self.empty_j)
          d_s2 = (self.n-1-self.empty2_i) + (self.n - 2 - self.empty2_j)
          
          count = 0
      for i in range(0,self.n):
              for j in range(0,self.n):
                  if(self.board[i][j] != self.n*self.n and self.board[i][j] != self.n*self.n - 1):
                      r = (self.board[i][j] - 1) // self.n 
                      c = (self.board[i][j] - 1) % self.n
                  else:
                      r = self.n - 1
                      c = self.n - 2                      
                  count += (abs(r-i) + abs(c-j))*2
                  #count += distance.euclidean((i,j),(r,c))*2
          return (count)
        
      
      def ensure_solvable(self):
          #calculates parity and if parity is odd, then it flips the numbers at the two blank spaces
          if(self.show_parity() % 2 == 1):
              print "Ensuring Solvability by swapping blanks"
              for i in range(self.n):
                  for j in range(self.n):
                      if(self.board[i][j] == self.n*self.n - 1):
                          self.board[i][j] = self.n*self.n
                          ti = i
                          tj = j
                          break

              self.board[self.empty_i][self.empty_j] = self.n*self.n - 1
              self.empty_i = ti
              self.empty_j = tj
              

      def get_hash(self):
          #function to hash the board; ie create a string that uniquely determines the state of the board
          str = ""
          for i in range(self.n):
              for j in range(self.n):
                str += chr(ord('a') + self.board[i][j] - 1)
          return str
                 
""" 
Solver class.
Currently only one 'method' of solving : BFS.
"""
class N2Solver :

      def __init__(self):
          self.path = []
          

      def BFS(self,puzzle):
          
          
          #function to solve the given N^2 - 1 puzzle using BFS 
          directions = ["up", "right", "left", "down"]
          #npuz = InhN2Puzzle(puz)
          #define visited list,action-dict,parent-list and a Queue for BFS 
          vis = []
          action = {}
          Q = Queue.Queue()
          parent = {}          
          #Insert start state into the queue.
          #Set the parent of the start state to itself.
          Q.put(puzzle)
          parent[puzzle.get_hash()] = puzzle.get_hash()
          while Q:
          
              curr = Q.get()
              if  curr.is_solved():
                  #Upon reaching the goal, reconstruct the path and return it.
                  current = curr.get_hash()
                  while(parent[current] != current):
                      self.path.append(action[current])
                      current = parent[current]
                  self.path = self.path[::-1]
                  return self.path

              for Dir in directions:
                  #create a copy of the original puzzle, apply movement, and insert into Queue
                  childPuzzle = copy.deepcopy(curr)
                  childPuzzle.move_empty_square(Dir)
                  if  childPuzzle.get_hash() in vis:
                      continue
                  else:
                      vis.append(childPuzzle.get_hash())
                      parent[childPuzzle.get_hash()] = curr.get_hash()
                      action[childPuzzle.get_hash()] = Dir
                      Q.put(childPuzzle)

      """ 
      Runs A-star search algorithm with 4 movements where heuristic value is sum of double the Manhattan distances 
      """
      def AstarManhattan(self,puzzle):
 


          # first check if input puzzle is solvable by checking parity,
          # if not then swap the two blanks to ensure it is.
          #puzzle.ensure_solvable()
          directions = ["left", "right", "up", "down"]
          explored_list = []
          Q = Queue.PriorityQueue()
          distances = {}
              
          """ 
              For the start state, g-value is 0
              Push the source into the priority queue alongwith the g + h value and the list representing current path
          """
          distances[puzzle.get_hash()] = 0
          Q.put((0+puzzle.Manhattan_sum(),puzzle,[]))
          #parent[start[0]][start[1]] = start
          #g[start[0]][start[1]] = 0
          
          while(not (Q.empty())):

            pop = Q.get()
              s = pop[1]
              # the real distance of the popped vertex is stored in dist_s
              dist_s = distances[s.get_hash()]
              #check if the goal state has been reached
              if (s.is_solved()):
                  print s.board
                  #return the path
                  return pop[2]
          # Expand if current cell has not already been explored
              # This check is necessary because multiple instances of this cell could have been pushed when it was not explored
              if  (s.get_hash() not in explored_list):
                  for i in range(4):
                    for j in range(2):
                         #create copies to push into the queue
                         childPuzzle = copy.deepcopy(s)
                         
                         if(j == 1):
                             childPuzzle.move_empty_squares(childPuzzle.n*childPuzzle.n,directions[i])
                         else :
                             childPuzzle.move_empty_squares(childPuzzle.n*childPuzzle.n - 1,directions[i])
                         childhash = childPuzzle.get_hash()

                         if(childPuzzle.get_hash() not in distances.keys()):
                             distances[childPuzzle.get_hash()] = 1000000000 
                         
                         childDist = distances[childPuzzle.get_hash()] 
                         if  ( childPuzzle.get_hash() not in explored_list ):
                             #child's g-value is parent's distance plus 1
                             g_child = dist_s + 1
                             h_child = childPuzzle.Manhattan_sum()
                             # Add this child to the fringe if the new (g + h) value is less than earlier (g + h) value
                             # Since h value is fixed, comparing only g-values
                             if( g_child < childDist ):
                                 # update the g-value (real distance)
                                 # push the child with g + h - value
                                 distances[childPuzzle.get_hash()] = g_child
                              if(j == 1) :
                                     if(childPuzzle.is_solved()): 
                                         print childPuzzle.board
                                         return pop[2] + ["1-" + directions[i]]
                                     else : 
                                         Q.put((g_child + h_child,childPuzzle,pop[2] + ["1-" + directions[i]]))          
                                 else:
                                     if(childPuzzle.is_solved()): 
                                         print childPuzzle.board
                                         return pop[2] + ["2-" + directions[i]]
                                     else : 
                                          Q.put((g_child + h_child,childPuzzle,pop[2] + ["2-" + directions[i]]))          
                                 
                  #after expanding all the children , mark the node as explored
                  explored_list.append(s.get_hash())
                  

print("\nEnter the dimension(value of N) and hit enter")
print("Next,enter elements row-wise , hitting enter after each element")

new_puzzle = N2Puzzle(4)
#new_puzzle.gen_xstep_board(4)
new_solver = N2Solver()
print "\nSolution is:"
sol = new_solver.AstarManhattan(new_puzzle)
print sol
print len(sol)
print "movement of n-square - 1 cell is called \"2\" and that of n-square cell is \"1\"" 
