"""

Arko Sharma
Roll No     -  11161002
Date        -  17/08/2018 


"""
from __future__ import print_function
import numpy as np
import math
import Queue
import pickle
class RoadNetwork:

      """     The road network needs to populate the list of events according to the given
	      conditions.

	      A network consisting of unidirectional roads is given as an adjacency matrix. Also, a list 
	      of vehicles is given and for each vehicle there is a sequence of vertices 
	      which specifies the route it is supposed to take.

	      In this setting an event takes place when a vehicle leaves a particular road
	      and enters a different road. The transition between roads is instantaneous.
      """

      def __init__ (self, road_lengths):
 
   	  self.road_lengths = road_lengths

      	  """ the environment has an load-matrix (Aij) which is :
      	  	   -1  : if there is no road between junction "i" and junction "j"
      	  	    x  : if there are currently x vehicles on the road from "i" to "j"
          """
          self.load_matrix = np.zeros(road_lengths.size).reshape(len(road_lengths),len(road_lengths[0]))
          for i in range(0,len(road_lengths)) :
          	  for j in range (0,len(road_lengths[i])) :
          	  	  if (road_lengths[i][j] == 0 ):
      		      	      self.load_matrix[i][j] = -1

          self.pq = Queue.PriorityQueue()


      """ The Event function executes the transition of vehicles from one road 
          to another. It chooses the vehicle on top of the min-PriorityQueue ie
          the vehicle whose departure time is the least and updates the data of the
          PriorityQueue,LoadMatrix as well as that of the vehicle.

          If the popped vehicle signals that it has reached it's destination then this 
          vehicle is not re-inserted in the priority queue.
      """
  	      
      def Event(self):

      	  #get the next vehicle
      	  popd_vehicle = self.pq.get()
          
      	  #reduce traffic on the road it has just finished
      	  if(popd_vehicle.roads_travelled > 0):
      	  

		  from_c = int(popd_vehicle.path[popd_vehicle.roads_travelled-1])
	          to_c   = int(popd_vehicle.path[popd_vehicle.roads_travelled])      	  	  
                  self.load_matrix[from_c][to_c] -= 1

	  #update the vehicle's details
	  signal = popd_vehicle.update_departure()
      	  if (signal != "Reached Destination"):
		 
		  from_c = int(popd_vehicle.path[popd_vehicle.roads_travelled-1])
	          to_c   = int(popd_vehicle.path[popd_vehicle.roads_travelled])      	  	  
                  
      	  	  #increase traffic on the following road
    	  	  (self.load_matrix[from_c][to_c]) += 1
    	  	  

      	  	  #update the PriorityQueue with the updated vehicle
      	  	  self.pq.put(popd_vehicle)

      	  




      
class Vehicle :
	"""
        Each vehicle has a numeric id, departure time, a count of the roads it has travelled and the
        sequence of vertices which constitutes its predefined path. 
        """

        def __init__(self,Id,path,dep_time):

     	    self.Id = Id
	    self.path = path
	    self.dep_time = dep_time
	    self.roads_travelled = 0
 	  

 	# comparator function for sorting by time 
        def __cmp__(self,other):
          return cmp(self.dep_time,other.dep_time)

      
        # function to update the details of vehicles after each Event
        def update_departure(self) :
          
            self.roads_travelled += 1
            if ( self.roads_travelled  <  5):
              
              from_c = int(self.path[self.roads_travelled-1])
              to_c   = int(self.path[self.roads_travelled])


              #traffic denotes num of vehicles in front
              traffic = network.load_matrix[from_c][to_c]
          	  
              #speed is a function of "traffic"
              speed = np.true_divide(((math.e ** (traffic/2)) + 15 ) , ((math.e ** (traffic/2)) + 1))
              
              distance = network.road_lengths[from_c][to_c]
              
	      time_to_cross = np.true_divide(distance,speed) * 60
	      self.dep_time = self.dep_time + time_to_cross
      	      outputs[self.Id][self.roads_travelled] = self.dep_time
      	      return ""

      	    else: return "Reached Destination"




#reading input files
RoadLengths  = np.zeros([10,10])
VehiclePaths = np.zeros([100,5])
RL  = np.array(open("road.txt","r").read().split()).reshape(10,10)
VP  = np.array(open("vehicle.txt","r").read().split()).reshape(100,5)
start_times = pickle.load(open("time","r"))	

for i in range(len(RoadLengths)):
    for j in range(len(RoadLengths[i])):
        RoadLengths[i][j]= int(RL[i][j])
    
for i in range(len(VP)):
    for j in range(len(VP[i])):
        VehiclePaths[i][j]= int(VP[i][j])
            
outputs   = np.zeros([100,5])

#creating the road network
network = RoadNetwork(RoadLengths)

#putting vehicles in the network
for i in range (0,len(VehiclePaths)):
	  
	  new_vehicle = Vehicle(i,VehiclePaths[i],start_times[i])
	  network.pq.put(new_vehicle)
	  outputs[i][0] = start_times[i]

while(network.pq.empty() == False):
	  network.Event()

writer = open("LAB2_output.csv","w")
writer.write("Site1,Site2,Site3,Site4,Site5\n")

for i in range(len(outputs)):
	  for j in range(len(outputs[i])):
	  	writer.write("{},".format(np.true_divide(outputs[i][j],60.0)))
	  writer.write("\n")
