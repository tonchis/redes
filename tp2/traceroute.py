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
option_parser.add_option("-s", "--save", dest="save", default="0", type="int")

options, reminder = option_parser.parse_args()

# Router#ips: [List[String]] holds the router ip.
# Router#rtt: [List[Float]] holds the round trip time it took to comunicate with the router.
Router = collections.namedtuple("Router", ["ips", "rtt"])

ECHO_REPLY = 0
TIME_EXCEEDED = 11

def measure_rtt(block):
    start = time.time()
    result = block()
    end = time.time()
    return (result, end - start)

def zrtt_i(array):
    return map(lambda rtt_i: round((rtt_i - avg_rtt)/standard_deviation_rtt, 3), array)

def z_score(array):
    return map(lambda rtt_i: (rtt_i - avg_rtt) / standard_deviation_rtt, array)

def normalize_rtt_i(rtts):
    normalized = [rtts[0]]
    for i in range(1, len(rtts)):
        normalized.append(rtts[i] - rtts[i - 1])

    return normalized

routers = Router(ips=[], rtt=[])
if (options.save) == 1:
    results = open(experiment_file_name(str(options.university)), 'w')
for ttl in range(1, options.max_ttl + 1):
    if (options.save) == 1:
        results.write("University: " + str(options.university) + "\n")

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
        rtts.append((res, round(rtt*1000, 3)))

    avg_rtt_i = round(numpy.mean(map(lambda pair: pair[1], rtts)), 3)
    print "  rtt_i:", avg_rtt_i

    if res:
        icmp = res.getlayer(scapy.layers.inet.ICMP)
        ip = res.getlayer(scapy.layers.inet.IP)
        src = ip.src
        print "  from", src
        if icmp.type == ECHO_REPLY:
            print "  ECHO REPLY"
            store(routers, src, avg_rtt_i)
            break
        elif icmp.type == TIME_EXCEEDED:
            print "  TIME EXCEEDED"
            store(routers, src, avg_rtt_i)
    else:
        print "  timeout - not storing"

normalized_rtt_i = normalize_rtt_i(routers.rtt)

puts(normalized_rtt_i, "RTTs", options.puts)
if (options.save) == 1:
    results.write("RTTs: " + str(normalized_rtt_i) + "\n")

avg_rtt = round(numpy.mean(normalized_rtt_i), 3)
print "avg_rtt:", avg_rtt
if (options.save) == 1:
    results.write("avg_rtt: " + str(avg_rtt) + "\n")

standard_deviation_rtt = round(numpy.std(normalized_rtt_i), 3)
print "standard_deviation_rtt:", standard_deviation_rtt
if (options.save) == 1:
    results.write("standard_deviation_rtt: " + str(standard_deviation_rtt) + "\n")

zscore = map(lambda item: round(item, 3), z_score(normalized_rtt_i))
print "zscore: ", zscore
if (options.save) == 1:
    results.write("z_score: " + str(zscore) + "\n")

if(options.geolocation == 1):
    geolocation = map(geolocate, routers.ips)
    puts(routers.ips, "IPs", options.puts)
    puts(geolocation, "Geolocation", options.puts)
    if (options.save) == 1:
        results.write("IPs: " + str(routers.ips) + "\n")
    if (options.save) == 1:
        results.write("Geolocation: " + str(geolocation) + "\n")
        results.close()
