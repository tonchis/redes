#!/usr/bin/evn python
import sys

# the input expected in this script for each line:
# Who has dstIP Tell srcIP 
#


if len(sys.argv)<1:
	sys.exit("python tgf.py path")

# nodes  = list of ips in the network. since i need the order i can't use sets
nodes = list()
#edges = string "src dst"
edges = list()

f = open(sys.argv[1],'r')

for line in f:
	#formatting the line so it can be read easily
	line = line.replace("Who has ","")
	line = line.replace("?","")
	line = line.replace("Tell","-")
	data = line.split("-")
	data[0] = (data[0].replace("\n","")).strip()
	
	#just in case the line doesn't have any data	
	if (data[0] == "Info" or data[0]==""):
		continue	
	#remove newline char and duplicate warnings			
	data[1] = (data[1].replace("\n","")).strip()
	index = (data[1].find('(')-1)
	if not (index ==-1):
		data[1] = data[1][0:index]	

	#adding nodes to the lists
	if not (data[0] in nodes):
		nodes.append(data[0])
	
	if not (data[1] in nodes):
		nodes.append(data[1])
	#adding edges 
	#data[1] represents the source ip
	#data[0] representS the destination ip	
	edge = str(nodes.index(data[1])+1)+" "+str(nodes.index(data[0])+1)
	if not (edge in edges):
		edges.append(edge)

#print in tgf format 
for i in range(len(nodes)):
	print str(i+1)+" "+ nodes[i]

print "#"

for j in range(len(edges)):
	print edges[j]

f.close()

