#!/usr/bin/env python

import scapy.all
import logging
import optparse

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

option_parser = optparse.OptionParser()
option_parser.add_option("-m", "--max-ttl", dest="max_ttl", default="64", type="int")
option_parser.add_option("-u", "--url", dest="url", default="www.google.com")
option_parser.add_option("-t", "--tiemout", dest="timeout", default="1", type="int")
option_parser.add_option("-v", "--verbose", dest="verbose", default="0", type="int")

options, reminder = option_parser.parse_args()

ECHO_REPLY = 0
TIME_EXCEEDED = 11

routers = []
for ttl in range(1, options.max_ttl + 1):
    print "TTL: %s" % ttl
    res = scapy.sendrecv.sr1(scapy.layers.inet.IP(dst=options.url, ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)
    if res:
        icmp_response = res.getlayer(scapy.layers.inet.ICMP)
        if icmp_response.type == ECHO_REPLY:
            routers.append(icmp_response.src)
            break
        elif icmp_response.type == TIME_EXCEEDED:
            routers.append(icmp_response.src)

print routers

