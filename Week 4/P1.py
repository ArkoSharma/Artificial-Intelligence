"""

Arko Sharma
111601002

Lab 4 :: P1 : ( n-squared minus 1 puzzle )
         
"""

import numpy as np
class N2Puzzle:
      """ 
      Environment implementing the " n-squared - 1 " puzzle.
      
      """
      
      def get_random_permutation(self):
          #generate and return randomly permuted numbers from 1 to n-sq
          return np.random.permutation([x for x in range(1,self.n*self.n+1) ]) 


      def __init__(self,n):
          # populates the board with randomly permuted numbers less than n-squared.
          # the number n-squared denotes the empty square whose location is tracked in the environment.

          self.n = n
	  self.board = np.array(self.get_random_permutation()).reshape(self.n,self.n)
          
	  for i in range (n):
              for j in range(n):
                  if( self.board[i][j] == self.n*self.n ) :
                      self.empty_i = i
                      self.empty_j = j
 

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
              if(self.empty_i == n-1):
                   return
              else :
                   temp = self.board[self.empty_i+1][self.empty_j]
                   self.board[self.empty_i + 1][self.empty_j] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_i += 1

          if(move_string == "right" ):
              if(self.empty_j == n-1):
                   return
              else :
                   temp = self.board[self.empty_i][self.empty_j + 1]
                   self.board[self.empty_i ][self.empty_j + 1] = self.n * self.n
                   self.board[self.empty_i][self.empty_j] = temp
                   self.empty_j += 1
                   

      def show_parity(self):
          #function to calculate and show the parity as defined in the question
          
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
                           

new_puzzle = N2Puzzle(10)
new_puzzle.show_parity()
            
