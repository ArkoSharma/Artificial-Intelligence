# AILab 1 Problem 2
# Arko Sharma
# 06.08.2018
"""
	Imagine a 2-dimensional world with each location described as l = (x, y), where x, y are integers.
	There is dirt in a location l=(X,Y) and the vaccum robot has to start from location ls = (xs,ys).
	Come up a python implementation of a) environment b) wise-vr agent which picks the dirt.
	

"""
class environment:
    """ Environment is defined by 4 state variables :
	loc_x , loc_y     : static location of dirty block
	agent_x , agent_y : location of agent """

    
    

    def __init__(self,initial_agent_x,initial_agent_y,dirt_x,dirt_y):
	self.agent_x = initial_agent_x
	self.agent_y = initial_agent_y
	self.dirt_locx = dirt_x
	self.dirt_locy = dirt_y
	self.steps = 0
    

    def percept(self,x_steps,y_steps):
	

        self.agent_x += x_steps
        self.agent_y += y_steps
	self.steps = self.steps+1
	print ("{}\t{}\t{}\n".format(self.steps,self.agent_x,self.agent_y))	        
	# returns true if the location is dirty 
        return (self.dirt_locx == self.agent_x and self.dirt_locy == self.agent_y )

       
class agent:
    """Class that defines agent

       The agent has 2 states : 
	
	  x_steps : no of x moves to make
	  y_steps : no of y moves to make  """
   
    
    x_steps = 0
    y_steps = 0
    
    def move_left(self):
        """Perform action moves left"""
	x_steps = -1
        y_steps = 0
	return grid.percept(x_steps,y_steps)
    def move_right(self):
        """Perform action moves right"""
	x_steps = 1
        y_steps = 0
	return  grid.percept(x_steps,y_steps)

    def move_down(self):
        """Perform action moves down"""
	x_steps = 0
        y_steps = -1
	return  grid.percept(x_steps,y_steps)
    
    def move_up(self):
        """Perform action moves up"""
	x_steps = 0
        y_steps = 1
	return  grid.percept(x_steps,y_steps)
    
    


def get_next_moves(curr_square):
    """ Forms the list of movements for paving the next bigger square , given current square length.
    	Starting from middle of top side of current square and going clockwise"""


    moves = []
    # firstly move up by one 
    moves += 'u'
    # then complete the right half of the top side of new square 
    for i in range (1,(curr_square+2)/2 +1) :
        moves += 'r'
    # go down along right side of the new square
    for i in range (1,(curr_square+2)) :
        moves += 'd'
    # go left along the lower side of the new square
    for i in range (1,(curr_square+2)) :
        moves += 'l'
    # move up along the left side
    for i in range (1,(curr_square+2)) :
        moves += 'u'
    # finally complete the left half of top side
    for i in range (1,(curr_square+2)/2 +1) :
        moves += 'r'
    return moves


""" define a new agent """
my_agent = agent()
print ("steps   ag_x    ag_y\n")


""" description of movement ::
	1. The agent moves along the perimeter of a square to look for the destination.
	   The length of a square is measured by the number of blocks( grids ) per side.
	2. Once a cycle is complete, the length of square is incremented by 2 blocks.
	   The newly formed square just bounds the earlier square.
	3. Initial length ( no of grids along the side ) of the square is 1.
	   It starts at the initial location of the cleaner agent.
      	   It is a complete cycle by itself.
"""
curr_square = 1

# create a grid (environment) object :: agentx,agenty,dirtx,dirty 
grid = environment(100,100,0,0)
found_dest = grid.percept(0,0)
if(found_dest) : print "reached destination"
else :
    while(found_dest!=True) : 
	"""getting the next sequence of moves""" 
	next_movements = get_next_moves(curr_square)
	for i in next_movements:
            if(i == 'u' ) :
        	if(my_agent.move_up()) :    
    	            print "reached destination"
    	            found_dest= True
		    break 
            elif(i == 'd') :
        	if(my_agent.move_down()) :    
    	            print "reached destination"
    	            found_dest= True
		    break
    
            elif(i == 'l') :
                if(my_agent.move_left()) :    
    	            print "reached destination"
    	            found_dest= True
		    break
    
            elif(i == 'r') :
       	        if(my_agent.move_right()) :    
    	            print "reached destination"
    	            found_dest= True
		    break
	""" increment square size """
	curr_square = curr_square + 2
print("Reached Destination in {} steps".format(grid.steps))

