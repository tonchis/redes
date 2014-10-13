#!/usr/bin/env python

import sys
import time
from scapy.all import *

ECHO_REPLY = 0
TIME_EXCEEDED = 11

def ping(dest, ttl):
	packet = IP(dst=dest, ttl=ttl) / ICMP()
	itime = time.time()
	#sr1 is like sr except it returns the first answer
	return (sr1(packet, timeout=1, verbose=0), time.time()-itime)

def traceroute(dest, limit=100):
	ttl = 1
	responses = []
	done = False
	while ttl<=limit and not done :
		ip = '(unknown)'
		tipo = 'notype'
		(response, rtt) = ping(dest, ttl)
		if response:
			if response.type == ECHO_REPLY:
				ip = response.src
				done = True	
			if response.type == TIME_EXCEEDED:
				ip = response.src
		else:
			ip = '(no response)'
		responses.append((ip,rtt))	
		ttl = ttl+1
	return responses	 	

if __name__ == '__main__':
    
    responses = traceroute(sys.argv[1],int(sys.argv[2]))
    for (ip, rtt) in responses:
    	print(srt(ip)+"-"+str(rtt))