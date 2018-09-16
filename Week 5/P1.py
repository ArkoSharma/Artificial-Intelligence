"""
Arko Sharma
111601002
Lab 5 :: ( n-squared minus 1 puzzle ) - Solution using BFS
         
"""

import numpy as np
import Queue
import copy
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
	  self.board = np.array([x for x in range(self.n * self.n)]).reshape(self.n,self.n)
	  k = 1
	  for i in range(self.n):
	      for j in range(self.n):
	          self.board[i][j] = k
	          k += 1
          
	  for i in range (self.n):
              for j in range(self.n):
                  if( self.board[i][j] == self.n*self.n ) :
                      self.empty_i = i
                      self.empty_j = j
          

      def is_solved(self):
          #function to check if the current state represents the goal state ie a solved board.
          #for doing this, just check if the board is sorted while traversing in row-major order.         
          k = 1          
          for i in range(self.n):
              for j in range(self.n):
                  if  (self.board[i][j] != k):
                      return False
                  k += 1
          return True           


      def move_empty_square(self,move_string):
          #moves the empty square as per the passed direction
	  if(move_string == "up" ):
              if(self.empty_i == 0):
                   return
              else :
                   temp = self.board[self.empty_i-1][self.empty_j]
                   self.board[self.empty_i - 1][self.empty_j] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_i -= 1

          if(move_string == "left" ):
              if(self.empty_j == 0):
                   return
              else :
                   temp = self.board[self.empty_i][self.empty_j - 1]
                   self.board[self.empty_i][self.empty_j - 1] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_j -= 1

          if(move_string == "down" ):
              if(self.empty_i == self.n-1):
                   return
              else :
                   temp = self.board[self.empty_i+1][self.empty_j]
                   self.board[self.empty_i + 1][self.empty_j] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_i += 1

          if(move_string == "right" ):
              if(self.empty_j == self.n-1):
                   return
              else :
                   temp = self.board[self.empty_i][self.empty_j + 1]
                   self.board[self.empty_i ][self.empty_j + 1] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_j += 1
                   


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
     
          print("Parity = {}".format((d_s + counter)%2))
          print("Empty location = ({},{})".format(self.empty_i,self.empty_j))
          print("{}".format(self.board)) 



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
          

new_puzzle = N2Puzzle(4)
new_puzzle.gen_xstep_board(4)
new_solver = N2Solver()
print "\nSolution is:"
print new_solver.BFS(new_puzzle)
