#! /usr/bin/env python
from scapy.all import *

def callback(package):
    arp = package.getlayer(ARP)
    print str(arp.psrc) + " > " + str(arp.pdst)

config.sniff_promisc = True

if __name__ == "__main__":
    sniffed = sniff(prn = callback, filter = "arp", store = 0)

