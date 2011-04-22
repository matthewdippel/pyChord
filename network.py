#Guillaume Ardaud <gardaud@cct.lsu.edu>
#Part of the PyChord project, written for academic purpose at Louisiana State University, 2010


import hashlib #necessary for sha1
import random, sys, time
import node


#main Network class holding the node circle
class Network:
	NUM_NODES= 1000 #number of nodes in the network
	NUM_KEYS= 50000 #number of keys to have

	nodes= {} #the node circle

	requestsIssued= False

	#class constructor
	def __init__(self):
		#create the node circle
		for i in range(0, self.NUM_NODES):
			tmp_node=node.Node(i, self)
			self.nodes[i]=(tmp_node)
			
		for i in range(0, self.NUM_NODES):
			self.nodes[i].buildFingerTable()

		print "Circle created"

		#store random data in the nodes
		for i in range(0,self.NUM_KEYS):
			self.nodes[i%self.NUM_NODES].addKey(i)
		print "Keys assigned"
		
	#get a key from the node circle in a linear manner (required for part C)
	def getKey(self, key):
		for i in self.nodes:
			if self.nodes[i].hasKey(key):
				return node.id

	def failRandomNode(self):
		nId= random.randint(0,len(self.nodes.keys())-1)
		nId=self.nodes.keys()[nId]
		self.failNode(nId)
		print "Failing node ", nId

	#fails the specified node	(required for part B)
	def failNode(self, nodeID):
		for i in self.nodes.keys():
			if (self.nodes[i].nodeid==nodeID):
				del self.nodes[i]
				print "Del'd  node ", nodeID
				return 0

	#tick every node
	def tick(self):
		for i in self.nodes:
			self.nodes[i].tick()
		#PART A
		#uncomment this to perform just one request
#		if not self.requestsIssued:
#			self.randomRequest()
#			self.requestsIssued=True

		##PART A1
		#uncomment this to perform a given amount of requests simultaneously
		#if the requests have not been issued yet
#		numRequests=10
#		if not self.requestsIssued:
#			for i in range(0,numRequests): #then we issue a given amount of requests
#				self.randomRequest()
#			self.requestsIssued=True
		
		##PART B
		#uncomment this to fail a given amount of nodes, and then perform a single request
		if not self.requestsIssued: #first we fail the nodes
			NODES_TO_FAIL=1
			for i in range(0,NODES_TO_FAIL):
				self.failRandomNode()

		for i in self.nodes: #we stabilize the circle each tick; in practice, this can be done less frequently
			self.nodes[i].stabilize()

		if not self.requestsIssued: #then if it's not already done, we issue the requests
			for i in range(0,5): #issue 5 requests
				self.randomRequest()
			self.requestsIssued=True
		
		##PART C
		#uncomment this to perform a random naiveSearch
#		if not self.requestsIssued:
#			self.naiveSearch()
#			self.requestsIssued=True
		
						
	def randomRequest(self):
		#let's get a random node
		nId= random.randint(0,len(self.nodes.keys())-1)
		nId=self.nodes.keys()[nId]
		#let's get a random key
		key=random.randint(0,self.NUM_KEYS-1)

		print "Let's have a random node :", self.nodes[nId].nodeid, "looking for a random key: ", key 
		self.nodes[nId].searchKey(key)

		
	#returns id'th node in circle
	def getNode(self, id):
		idx=self.nodes.items()[id%len(self.nodes)][0]
		return self.nodes[idx]

	#return the position of the node with id in the circle
	def getNodeRank(self, id):
		for i in self.nodes.keys():
			if self.nodes[i].nodeid==id:
				return i
		return -1
	
	#returns the id of the nth successor of the node with given id
	def getNthSuccessor(self, id, n):
		index=(self.getNodeRank(id)+n)%(len(self.nodes))
		return self.nodes[self.nodes.items()[index][0]].nodeid

	#allows to send a message to a node with id 'dest' over the network	
	def sendMessage(self, message, dest):
		self.getNode(dest).addMessage(message)
		
		
	def naiveSearch(self):
			#let's get a random node
			node=random.randint(0,len(self.nodes)-1)
			#let's get a random key
			key=random.randint(0,self.NUM_KEYS-1)

			print "Let's have a random node :", self.nodes[node].nodeid, "looking for a random key: ", key, "- this is using the naive approach!"
			
			start=time.time()
			hops=0
			while not self.nodes[node].hasKey(key):
				node=(node+1)%len(self.nodes)
				hops+=1
					
			print "We found the key ", key, " in node ", node, ". Total time: ", time.time()-start + hops*0.010, "- hops: ", hops
			
			