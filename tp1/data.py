#!/usr/bin/evn python
import sys
import scapy.all
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import math
import helpers

if len(sys.argv)<1:
	sys.exit("python tgfpcap.py path/to/pcapfile number_of_packages_to_read 0=src/1=dst min_apariciones title")

src = list()
dst = list()

#read pcap file
packages = scapy.utils.rdpcap(sys.argv[1], int(sys.argv[2]))

for package in packages:
	src.append(package.psrc)
	dst.append(package.pdst)
	
ips =[]
count=[]
pairs = []
freq = []
label =""
if (int(sys.argv[3]) == 0):
	source = set(src)
	for s in source:
		label = "fuente"
		ips.append(s)
		count.append(src.count(s))
		freq.append(float(src.count(s)) /float(len(src)))
		pairs.append((s, helpers.information(float(src.count(s)) /float(len(src)))))
else:
	destination = set(dst)
	for d in destination:
		label="destino"
		ips.append(d)
		count.append(dst.count(d))
		freq.append(float(dst.count(d)) /float(len(dst)))
		pairs.append((d, helpers.information(float(dst.count(d)) /float(len(dst)))))


#ordeno las ips por la informacion
pairs.sort(key=lambda tup: tup[1])

ipes = map(lambda pair: pair[0], pairs)
inf = map(lambda pair: pair[1], pairs)

pos = np.arange(len(ipes))
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(ipes, rotation=90, size=7.75)

i = 0
ent = []
entropy = helpers.map_reduce_entropy(freq)
while i< len(pos):
	ent.append(entropy)
	i = i+1


plt.bar(pos[0:int(sys.argv[4])], inf[0:int(sys.argv[4])], width, color='r')
plt.title(str(sys.argv[5]) + " - IPs "+ label+ " -  Mas de " +str(int(sys.argv[4])) + " apariciones")
plt.title('Informacion por IP - IPs ' + label + "- Muestra "+str(sys.argv[5]) )
plt.ylabel('Informacion (bits)')
plt.xlabel('IPs')
lala = plt.plot(pos[0:int(sys.argv[4])+1], ent[0:int(sys.argv[4])+1], label='Entropia de la fuente')
plt.legend(loc="upper left")
#blue_line = mlines.Line2D([], [], color='blue',
                          #markersize=15, label='Entropia')
#plt.legend(handles=[blue_line])

plt.show()



