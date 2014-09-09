#! /usr/bin/env python
from scapy.all import *
import atexit, sys

sys.path.append("tp1")

import helpers

def write_pcap_file():
    print ""
    print "Building tmp/sniffed.pcap..."
    wrpcap("tmp/sniffed.pcap", sniffed)
    print "Done."

atexit.register(write_pcap_file)

config.sniff_promisc = True

if __name__ == "__main__":
    global sniffed
    sniffed = sniff()

