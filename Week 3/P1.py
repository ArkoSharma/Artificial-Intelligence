"""

Arko Sharma
111601002

Question Lab 3 :
         
"""

import numpy as np
class environment:
    """ Environment is defined by 6 state variables :
	dest_x , dest_y ,dest_z       : static location of destination block
	agent_x , agent_y ,agent_z    : location of agent """

    
    

    def __init__(self,initial_agent_x,initial_agent_y,initial_agent_z,dest_x,dest_y,dest_z):
    	self.agent_x = initial_agent_x
    	self.agent_y = initial_agent_y
    	self.agent_z = initial_agent_z
	self.destx = dest_x
    	self.desty = dest_y
    	self.destz = dest_z
    	self.steps = 0
    

    def reward(self,x_steps,y_steps,z_steps):
	
	"""check if the moves are legal and change the state """
        if(self.agent_x + x_steps <= L and self.agent_x + x_steps >=0):
            self.agent_x += x_steps
        if(self.agent_y + y_steps <= L and self.agent_y + y_steps >=0):
            self.agent_y += y_steps
        if(self.agent_z + z_steps <= L and self.agent_z + z_steps >=0):
            self.agent_z += z_steps
        
	self.steps = self.steps+1
	print ("{}\t{}\t{}\t{}\n".format(self.steps,self.agent_x,self.agent_y,self.agent_z))	        
    	# returns a reward of 1 if location is the destination 
        return (self.destx == self.agent_x and self.desty == self.agent_y and self.destz == self.agent_z )

       
class agent:
    
    """Class that defines agent
        
       The agent has 1 state consisting of 3 variables: 
	
    	  x_steps : next x move to make
    	  y_steps : next y moves to make  
      	  z_steps : next x move to make 
    """
   
    
    x_steps = 0
    y_steps = 0
    z_steps = 0
    
    def move(self,x,y,z):
	self.x_steps = x
        self.y_steps = y
        self.z_steps = z
        return grid.reward(self.x_steps,self.y_steps,self.z_steps)



def get_next_moves():
    """ Returns a random int from 1 to 6 
        This specifies one of the directions (top -crosssectional  view ) :
        1. North
        2. South 
        3. East
        4. West
        5. Up
        6. down
        
    """
    move = np.random.randint(1,7)
    return move


""" define a new agent """
my_agent = agent()
print ("steps   ag_x    ag_y    ag_z\n")


# create a grid (environment) object :: agentx,agenty,agentz being initial agent position and final location is as specified 
L = 10
#finding the solution 10 times 
result_steps = []
for i in range (0,10):
	
	grid = environment((L+1)//2,(L+1)//2,(L+1)//2,L,L,L)
	found_dest = grid.reward(0,0,0)
	if(found_dest) : print "reached destination"
	else :
	    while(found_dest!=True) : 
		"""getting the next  move""" 
		
	 	
		""" description of movement ::
		    
		     The agent moves randomly in one of the 6 directions:: 
		"""

		next_movement = get_next_moves()
		
		
		""" Here the directions are as follows ::
		 
		    x steps make east,west moves
		    y steps make north,south moves
		    z steps make up and down moves 
		"""
		if(next_movement == 1 ) :
		    if(my_agent.move(0,1,0)) :    
			    print "reached destination"
			    found_dest= True
			    break 
		elif(next_movement == 2):
		    if(my_agent.move(0,-1,0)) :    
			    print "reached destination"
			    found_dest= True
			    break
		elif(next_movement == 3):
		    if(my_agent.move(1,0,0)) :    
			    print "reached destination"
			    found_dest= True
			    break
		elif(next_movement == 4):
		    if(my_agent.move(-1,0,0)) :    
			    print "reached destination"
			    found_dest= True
			    break
		elif(next_movement == 5):
		    if(my_agent.move(0,0,1)) :    
			    print "reached destination"
			    found_dest= True
			    break
		elif(next_movement == 6):
		    if(my_agent.move(0,0,-1)) :    
			    print "reached destination"
			    found_dest= True
			    break


	print("Reached Destination in {} steps".format(grid.steps))
        result_steps.append(grid.steps)


print "The number of steps in 10 cases "
for i in result_steps :
     	print i
result = np.array(result_steps)
print ("mean = {}".format(np.mean(result)))
print ("variance = {}".format(np.var(result)))


