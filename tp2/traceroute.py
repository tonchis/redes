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

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

option_parser = optparse.OptionParser()
option_parser.add_option("-m", "--max-ttl", dest="max_ttl", default="64", type="int")
option_parser.add_option("-u", "--url", dest="url", default="www.google.com")
option_parser.add_option("-t", "--tiemout", dest="timeout", default="1", type="int")
option_parser.add_option("-v", "--verbose", dest="verbose", default="0", type="int")
option_parser.add_option("-g", "--geolocation", dest="geolocation", default="1", type="int")
option_parser.add_option("-T", "--times", dest="times", default="3", type="int")

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
        return scapy.sendrecv.sr1(scapy.layers.inet.IP(dst=options.url, ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)

    rtts = []
    for t in range(1, options.times + 1):
        (res, rtt) = measure_rtt(sr1)
        rtts.append((res, rtt))

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
    else:
        print "  no answer"

    print "  rtt_i:", avg_rtt_i

avg_rtt = numpy.mean(routers.rtt)
print "avg_rtt =", avg_rtt

standard_deviation_rtt = numpy.std(routers.rtt)
print "standard_deviation_rtt =", standard_deviation_rtt
print routers.ips
print routers.rtt

def is_local_network(ip):
    return re.compile("^192\.168").match(ip) != None

def geolocate(ip):
    if is_local_network(ip):
        return "Local Network"

    res = requests.get(GEOLOCATION_ENDPOINT, params={"ip": ip, "position": "true"})
    json = res.json()

    if json["country_code"] == "XX":
        return "Couldn't geolocate ip %ip%".format(**locals())

    return { "country": json["country_name"], "city": json["city"], "position": {"latitude": json["lat"], "longitude": json["lng"]} }

if options.geolocation == 1:
    print map(geolocate, routers.ips)

rtt_is = []
for i in range(2, len(routers.rtt)):
     rtt_is.append(routers.rtt[i] - routers.rtt[i - 1])

def zrtt_i(array):
    return map(lambda rtt_i: (rtt_i - avg_rtt) / standard_deviation_rtt, array)

print zrtt_i(rtt_is)
