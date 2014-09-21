#!/usr/bin/evn python
import sys
import scapy.all


if len(sys.argv)<1:
	sys.exit("python tgfpcap.py path/to/pcapfile numberofpackagestoread")

# nodes  = list of ips in the network. since i need the order i can't use sets
nodes = list()
#edges = string "src dst"
edges = list()

#read pcap file
packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

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


