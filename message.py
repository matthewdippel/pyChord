#Guillaume Ardaud <gardaud@cct.lsu.edu>
#Part of the PyChord project, written for academic purpose at Louisiana State University, 2010

#class for the message object exchanged between nodes
import time

class Message:
	requestedKey=0 #the key that is requested
	requestor=0 #the node that sent that message first
	birth=0 #the date of birth of the message
	hops=0 #the number of hops to completion
	owner=0
	
	messageType="" #the type of the message; either request or response

	def __init__(self, requestedKey, requestor, messageType):
		self.requestedKey=requestedKey #the key the message requests
		self.requestor=requestor
		
		self.birth=time.time() #set the birth of the message
		self.hops=0
		
		self.messageType=messageType