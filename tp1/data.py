#!/usr/bin/evn python
import sys
import scapy.all
import numpy as np
import matplotlib.pyplot as plt


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
label =""
if (int(sys.argv[3]) == 0):
	source = set(src)
	for s in source:
		if src.count(s) > int(sys.argv[4]):
			label = "fuente"
			ips.append(s)
			count.append(src.count(s))
else:
	destination = set(dst)
	for d in destination:
		if dst.count(d) > int(sys.argv[4]):
			label="destino"
			ips.append(d)
			count.append(dst.count(d))

pos = np.arange(len(ips))
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(ips, rotation=90, size=7.75)

plt.bar(pos, count, width, color='r')
plt.title(str(sys.argv[5]) + " - IPs "+ label+ " -  Mas de " +str(int(sys.argv[4])) + " apariciones")
plt.ylabel('Frecuencia')
plt.show()

