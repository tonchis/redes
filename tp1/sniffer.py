#! /usr/bin/env python
from scapy.all import *

def monitor_callback(package):
    print package.summary()

if __name__ == "__main__":
    sniffed = sniff(prn = monitor_callback, filter = "arp", store = 2)

