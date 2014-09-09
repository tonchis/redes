#! /usr/bin/env python

# Don't print warnings from scapy
import logging, sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

sys.path.append("tp1")
import helpers

if len(sys.argv) > 1:
  pcap_file = sys.argv[1]
else:
  pcap_file = "tmp/sniffed.pcap"

packages = rdpcap(pcap_file)

packages.summary(prn = helpers.arp_source_destination_print, lfilter = helpers.who_has)
