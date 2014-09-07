#! /usr/bin/env python
from scapy.all import *

def callback(package):
    arp = package.getlayer(ARP)
    print str(arp.psrc) + " > " + str(arp.pdst)

def who_has(package):
    if package.haslayer(ARP):
        arp = package.getlayer(ARP)
        return arp.op == arp.who_has
    return False

config.sniff_promisc = True

if __name__ == "__main__":
    sniff(prn = callback, lfilter = who_has, store = 0)

