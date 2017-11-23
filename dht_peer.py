import argparse
import socket
import sys

import hashlib

# DHT peer application.
# Usage: ./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>

parser = argparse.ArgumentParser(usage='./dht_peer <-m type> <-p own_port <-h own_hostname> <-r root_port> <-R root_hostname>',
                                 description='DHT Peer Application',add_help=False)
parser._add_action(argparse._HelpAction(
    option_strings=['-H', '--help'],
    help='Gives you the help documentation and details about optional arguments'
))
parser.add_argument('-m','--peertype',type=int,help='Specify 1 if the peer is root and 0 otherwise')
parser.add_argument('-p','--own_port',help='Specify the port for the peer')
parser.add_argument('-h','--own_hostname',help='Specify the hostname of the peer')
parser.add_argument('-r','--root_port',help='Specify the port of the root')
parser.add_argument('-R','--root_hostname',help='Specify the hostname of the root')
args = parser.parse_args()

# Default is normal peer of the type is not specified.
if args.peertype is None:
    args.peertype = 0

# if args.peertype == 0:
#     print "Starting as normal peer"
# elif args.peertype == 1:
#     print "Starting as root"
# else:
#     print "Invalid peer type given. Please give 1 for root and 0 otherwise."


peertype = args.peertype
ownport = args.own_port
ownhost = args.own_hostname
rootport = args.root_port
roothost = args.root_hostname

# This c;ass may be useful in handling the ring position effectively. Initialises  as root. 
class nodeposition(self, nodenum = 0, preaddr = ownhost, preport = ownport, sucaddr = ownhost,sucport = ownport):
	self.nodenum = nodenum
	self.preaddr = preaddr
	self.preport = preport
	self.sucaddr = sucaddr
	self.sucport = sucport
#Initialize root node
successor = ownhost + ":" + ownportimport argparse
predecessor = ownhost + ":" + ownport

root_socket = (ownhost, ownport)
print >>sys.stderr, 'starting root node on %s port %s' % root_socket
sock.bind(root_socket)
sock.listen(10) # Maximum 10 connections

conn, addr = sock.accept()
print "A Client has connected at ", addr
conn.send("ROOT HELLO ") # This should pass the node position information to the clients.
predecessor = addr + ":" + clientport
conn.close() 
