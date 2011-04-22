#Guillaume Ardaud <gardaud@cct.lsu.edu>
#Part of the PyChord project, written for academic purpose at Louisiana State University, 2010

import sys, time
import message

#Class for the node object
class Node:
	NETWORK_LATENCY=0.010 #this is used to simulate network latency in the network (in seconds)

	#node's id; used to identify the node on the network. The max value for the id will depend on the machine running the python interpreter; 
	#however as Python uses long ints for integers, one can create a network of several hundred thousand nodes without fear of overflow.
	nodeid=0
	
	#reference to the network; used for sending messages to other nodes, checking if a node exists, etc.
	parent= None

	#the collection of keys that the node owns
	keys=[]

	#the node's fingertable; max size is below
	fingertable=[]
	#since we'll be using networks with ~1000 nodes, let's use log(1024)=10 as the max number of entries for the finger table
	maxfingertablesize=10

	#the list of messages to process
	messages= []
	

	#constructor for the node
	def __init__(self, nodeid, parent):
		self.nodeid=nodeid
		self.parent=parent
		self.keys=[]
		self.messages=[]
		self.fingertable=[]
	
	#adds the given key to the node's collection
	def addKey(self, key):
		self.keys.append(key)
		
	#returns true if the node has the given key, false otherwise
	def hasKey(self, key):
		if (self.keys.count(key)>0):
			return True
		return False
		
	#this function is executed once every step of the simulation
	def tick(self):
		#print "Node ", self.nodeid, " has ", len(self.messages), " messages to process!"
		for message in self.messages:
			self.processMessage(message)
			
	#processes all message in the queue
	def processMessage(self, message):
		if (message.messageType=="response"):
			print "Node ", self.nodeid, " has received a response! Requested key num. ", message.requestedKey, " is owned by node ", message.owner, ". This was achieved in ", message.hops, " hops for a total time of ", time.time()-message.birth + message.hops * self.NETWORK_LATENCY , " seconds"
		elif (message.messageType=="request"):
			print "Node ", self.nodeid, " has received a request for key num ", message.requestedKey

			if self.hasKey(message.requestedKey):#send value to requestor and discard message
				print "The node has this key, so we reply to the requestor with the key value"
				message.messageType="response"
				message.owner=self.nodeid
				self.parent.sendMessage(message,message.requestor)

			else:
				print "The node doesn't have the key... we forward the message to the next node in our finger table."
				print self.fingertable
				dest=self.closestPrecedingFinger(message.requestedKey%self.parent.NUM_NODES)
				print "Dest is ", dest
				message.hops+=1
				self.parent.sendMessage(message,dest)

		self.messages.remove(message)
		
	#builds the finger table for the node
	def buildFingerTable(self):
		self.fingertable=[]
		for i in range(0,self.maxfingertablesize):
			tempNode=self.parent.getNthSuccessor(self.nodeid,2**(i)%self.parent.NUM_NODES)
			self.fingertable.append(tempNode)
		self.fingertable.sort()
	
	#this initiates the node's search for the given key		
	def searchKey(self, key):
		if self.hasKey(key):
			print "This node is the owner of key ", key, " !"
		else:
			print "Sending a message asking for key ", key
			msg= message.Message(key, self.nodeid, "request")
			self.messages.append(msg)
	
	#this is called by the network; it is used to add a message to the current node's queue		
	def addMessage(self, message):
		self.messages.append(message)
		
	#returns the id of the node in the finger table that is closest preceding to the given target
	def closestPrecedingFinger(self, target):
		for i in range(self.maxfingertablesize-1,-1,-1):
			#print self.fingertable[i], "<=", target, "?"
			if self.fingertable[i]<=target:
				return self.fingertable[i]
		return self.fingertable[self.maxfingertablesize-1]

	#stabilizes the finger table
	def stabilize(self):
		self.buildFingerTable()
		