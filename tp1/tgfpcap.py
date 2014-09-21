#!/usr/bin/evn python
import sys
import scapy.utils
# the input expected in this script for each line:
# Who has dstIP Tell srcIP 
#


if len(sys.argv)<1:
	sys.exit("python tgfpcap.py path")

# nodes  = list of ips in the network. since i need the order i can't use sets
nodes = list()
#edges = string "src dst"
edges = list()

#f = open(sys.argv[1],'r')

sys.path.append("tp1")
packages = scapy.utils.rdpcap("facultad46arp.pcap")

for package in packages:
	if not (package.psrc in nodes):	
		nodes.append(package.psrc)
	if not (package.pdst in nodes):
		nodes.append(package.pdst)
	
	#adding edges 
	edge = str(nodes.index(package.psrc)+1)+" "+str(nodes.index(package.pdst)+1)
	if not (edge in edges):
		edges.append(edge)

#print in tgf format 
for i in range(len(nodes)):
	print str(i+1)+" "+ nodes[i]

print "#"

for j in range(len(edges)):
	print edges[j]

#f.close()

