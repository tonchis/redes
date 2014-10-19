#!/usr/bin/env python

import scapy.all
import logging
import optparse
import requests # pip install requests
import re
import time
import collections
import numpy #pip install numpy
import math
import pprint
from helpers import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

option_parser = optparse.OptionParser()
option_parser.add_option("-m", "--max-ttl", dest="max_ttl", default="64", type="int")
option_parser.add_option("-u", "--url", dest="url", default="www.google.com")
option_parser.add_option("-t", "--tiemout", dest="timeout", default="1", type="int")
option_parser.add_option("-v", "--verbose", dest="verbose", default="0", type="int")
option_parser.add_option("-g", "--geolocation", dest="geolocation", default="1", type="int")
option_parser.add_option("-T", "--times", dest="times", default="3", type="int")
option_parser.add_option("-p", "--puts", dest="puts", default="0", type="int")
option_parser.add_option("-U", "--university", dest="university")

options, reminder = option_parser.parse_args()

# Router#ips: [List[String]] holds the router ip.
# Router#rtt: [List[Float]] holds the round trip time it took to comunicate with the router.
Router = collections.namedtuple("Router", ["ips", "rtt"])

ECHO_REPLY = 0
TIME_EXCEEDED = 11
GEOLOCATION_ENDPOINT = "http://api.hostip.info/get_json.php"

def measure_rtt(block):
    start = time.time()
    result = block()
    end = time.time()
    return (result, end - start)

routers = Router(ips=[], rtt=[])
for ttl in range(1, options.max_ttl + 1):
    print "TTL:", ttl

    def sr1():
        if options.university == "tokyo":
            return scapy.sendrecv.sr1(scapy.layers.inet.IP(dst="www.u-tokyo.ac.jp", ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)
        elif options.university == "auckland":
            return scapy.sendrecv.sr1(scapy.layers.inet.IP(dst="www.auckland.ac.nz", ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)
        elif options.university == "oxford":
            return scapy.sendrecv.sr1(scapy.layers.inet.IP(dst="www.ox.ac.uk", ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)
        elif options.university == "uba":
            return scapy.sendrecv.sr1(scapy.layers.inet.IP(dst="www.dc.uba.ar", ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)
        else:
            return scapy.sendrecv.sr1(scapy.layers.inet.IP(dst=options.url, ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)

    rtts = []
    for t in range(1, options.times + 1):
        (res, rtt) = measure_rtt(sr1)
        rtts.append((res, rtt))

    def add(x, y):
        return x + y

    avg_rtt_i = numpy.mean(map(lambda pair: pair[1], rtts))
    
    if res:
        icmp = res.getlayer(scapy.layers.inet.ICMP)
        ip = res.getlayer(scapy.layers.inet.IP)
        src = ip.src
        print "  from", src
        if icmp.type == ECHO_REPLY:
            routers.ips.append(src)
            routers.rtt.append(avg_rtt_i)
            break
        elif icmp.type == TIME_EXCEEDED:
            routers.ips.append(src)
            routers.rtt.append(avg_rtt_i)
        #maybe we should take into consideration the icmp packages with other types. just sayin'
    else:
        print "  no answer"

avg_rtt = numpy.mean(routers.rtt)
print "avg_rtt =", avg_rtt

standard_deviation_rtt = numpy.std(routers.rtt)
print "standard_deviation_rtt =", standard_deviation_rtt
puts(routers.ips, "IPs", options.puts)
puts(routers.rtt, "RTTs", options.puts)


if(options.geolocation == 1):
    puts(map(geolocate, routers.ips), "Geolocation", options.puts)

rtt_is = []
for i in range(2, len(routers.rtt)):
     rtt_is.append(routers.rtt[i]-routers.rtt[i-1])

puts(zrtt_i(rtt_is, avg_rtt, standard_deviation_rtt), "ZRTT_i", options.puts)
