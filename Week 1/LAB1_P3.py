# Lab 1 Problem 3
# Arko Sharma
# 06.08.2018

 
"""
       Given a file, count the number of words in it using only f.read(1) command
"""


"""	
       In this solution the definition of word is just a group of english alphabets with no other alphabets in between.
       Any other character (including digits) serves as a delimiter """

class WordID:
        
	"""The WordID class is defined by one variable 
	   This variable indicates the last read character is a part of a word or not """
	
        status = "not_a_word"
         
        def check_character(self,char) :
            """ Examines a character and returns 1 if it is a starting of a word,
		else returns 0 """
	    
	    if(char.isalpha() == False):
	    	self.status = "not_a_word"
		return 0
 	    else :
	        if(self.status == "not_a_word"):
		   self.status = "word"
		   return 1
                else :
                   return 0
         
		

"""Take the file and count words in it """




print ("""\n\nIn this solution the definition of word is just a group
of english alphabets with no other alphabets in between.
Any other character (including digits) serves as a delimiter """)

print "Enter filename"
file_n = raw_input()
reader = open(file_n,"r")
num_words = 0
count_agent = WordID()
while(True):
      c = reader.read(1)
      if(c =='' ):
	    break  
      num_words += count_agent.check_character(c) 
                

print "Number of words in the file : "
print num_words

