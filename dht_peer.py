import argparse
import socket
import sys
import thread
import hashlib

parser = argparse.ArgumentParser(usage='./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>',
                                 description='DHT Peer Application',add_help=False)
parser._add_action(argparse._HelpAction(
    option_strings=['-H', '--help'],
    help='Gives you the help documentation and details about optional arguments'
))
parser.add_argument('-m','--peertype', type = int, help='Specify 1 if the peer is root and 0 otherwise')
parser.add_argument('-p','--own_port', type = int, help='Specify the port for the peer')
parser.add_argument('-h','--own_hostname',help='Specify the hostname of the peer')
parser.add_argument('-r','--root_port', type = int, help='Specify the port of the root')
parser.add_argument('-R','--root_hostname',help='Specify the hostname of the root')
args = parser.parse_args()

# Default is normal peer if the type is not specified.
if args.peertype is None:
    args.peertype = 0

peertype = args.peertype
ownport = args.own_port
ownhost = args.own_hostname
rootport = args.root_port
roothost = args.root_hostname

class node:
	def __init__(self,phname,phport,nname,nport,shname,shport):
		self.pn = phname
		self.pp = phport
		self.nn = nname
		self.np = nport
		self.sn = shname
		self.sp = shport
	def listensocket(self):
		global sock		
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
			print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
			sys.exit();
		try:
			sock.bind((self.nn, self.np))
		except socket.error , msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		sock.listen(10)
		
		return sock
	def printchord(self):
		print "Updated node position\n_____________"
		print "Predecessor:",self.pn,":",self.pp
		print "This node:",self.nn,":",self.np
		print "Successor:",self.sn,":",self.sp

	


def rootjoin(indata, nodeval):
	# 1. Update the predecessor of the current successor
	sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket Created for updating the predecessor of current successor'
	remote_ip = socket.gethostbyname( nodeval.sn )
	print 'Ip address of current successor %s is %s' %(nodeval.sn, remote_ip)
	#Connect to current successor of root
	sock2.connect((remote_ip , int(nodeval.sp)))
	print 'Socket Connected to %s on port %d'  %(nodeval.sn,int(nodeval.sp))
	#Sending the UPDATE request"
	predupdata = "UPDATE|PRED|"+ indata[1]+"|"+indata[2]
	#Send the whole string
	sock2.sendall(predupdata)
	sock2.close()
	print 'Message sent successfully \n %s to %s on %d'  %(predupdata,nodeval.sn,int(nodeval.sp))
	# 2. Update the successor of the joining node
#	sucupdate = "UPDATE|SUCC|"+nodeval.sn+"|"+str(nodeval.sp)
#	sock2.connect	
#	conn.sendall(sucupdate)
	# 3. Update the successor of the root node 
	nodeval.sn = indata[1]
	nodeval.sp = indata[2]
	nodeval.printchord()

def predup(indata,nodeval,conn):
	# Handling predecessor update requests
	nodeval.pn = indata[2]
	nodeval.pp = indata[3]
	nodeval.printchord()
	conn.close()

def succup(indata,nodeval,conn):
	# Handling predecessor update requests
	nodeval.sn = indata[2]
	nodeval.sp = indata[3]
	nodeval.printchord()
	conn.close()

def nodejoin(rh,rp,oh,op):
	# Sending JOIN request to root node
	sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket Created for updating the predecessor of current successor'
	rootip = socket.gethostbyname( rh )
	print 'Ip address of root %s is %s' %(rh, rootip)
	sock3.connect((rootip , rp))
	print 'Socket Connected to %s on port %d'  %(roothost,rootport)
	joindata ="JOIN|"+ownhost+"|"+str(ownport)
	print joindata
	#Send the whole string
	sock3.sendall(joindata)
	print 'Message sent successfully \n %s to %s on %d'  %(joindata,roothost,rootport)
	data = sock3.recv(1024)
	datadelim = data.split('|')
	return datadelim


# If m = 1, the node initiated is considered as the root node. 
if peertype == 1:
	# Initiating root node
	rootnode = node(ownhost,ownport,ownhost,ownport,ownhost,ownport)
	rootnode.printchord()
	# Creating a socket for root node
	sock_root = rootnode.listensocket()	
	print 'Root node listening'

	while 1:
		conn, addr = sock_root.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		req = conn.recv(1024)	
		reqpro = req.split('|')
		if not req:
			break	
		elif reqpro[0] == "JOIN":
			sucupdate = "UPDATE|SUCC|"+rootnode.sn+"|"+str(rootnode.sp)
			conn.sendall(sucupdate)
			print sucupdate
			rootjoin(reqpro,rootnode)

		elif (reqpro[0] == 'UPDATE') and (reqpro[1] == 'PRED'):
			predup(reqpro,rootnode,conn)
		else:
			print "invalid request type"
			print reqpro
			sys.exit()
		conn.close()	



elif peertype == 0:
	#Initiate a normal node with predecessor as root and successor as empty
	normalnode = node(roothost,rootport,ownhost,ownport,'',0)
	print "Current state of CHORD on the node %s:%d" %(ownhost,ownport)	
	normalnode.printchord()

	# Sending JOIN request to root node
	joinhandle = nodejoin(roothost,rootport,ownhost,ownport)
	normalnode.sn = joinhandle[2]
	normalnode.sp = int(joinhandle[3])
	# Creating a socket for normal node
	sock_normal = normalnode.listensocket()
	print 'Socket now listening'

	while 1:
		conn, addr = sock_normal.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		# Handling the incoming requests received
		nreq = conn.recv(1024)
		nreqpro = nreq.split('|')
		if not nreq:
			break
		# If the request is a join request
		elif (nreqpro[0] == 'UPDATE') and (nreqpro[1] == 'SUCC'):
			print nreqpro
			succup(nreqpro,normalnode,conn)
		elif (nreqpro[0] == 'UPDATE') and (nreqpro[1] == 'PRED'):
			predup(nreqpro,normalnode,conn)
		else:
			print "invalid request type"
			sys.exit()




	

else:
	print "Invalid peertype"
	sys.exit()



	
