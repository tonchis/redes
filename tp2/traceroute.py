#!/usr/bin/env python

import scapy.all
import logging
import optparse
import requests # pip install requests
import re

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

option_parser = optparse.OptionParser()
option_parser.add_option("-m", "--max-ttl", dest="max_ttl", default="64", type="int")
option_parser.add_option("-u", "--url", dest="url", default="www.google.com")
option_parser.add_option("-t", "--tiemout", dest="timeout", default="1", type="int")
option_parser.add_option("-v", "--verbose", dest="verbose", default="0", type="int")

options, reminder = option_parser.parse_args()

ECHO_REPLY = 0
TIME_EXCEEDED = 11
GEOLOCATION_ENDPOINT = "http://api.hostip.info/get_json.php"

routers = []
for ttl in range(1, options.max_ttl + 1):
    print "TTL:", ttl
    res = scapy.sendrecv.sr1(scapy.layers.inet.IP(dst=options.url, ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose)
    if res:
        icmp_res = res.getlayer(scapy.layers.inet.ICMP)
        if icmp_res.type == ECHO_REPLY:
            routers.append(icmp_res.src)
            break
        elif icmp_res.type == TIME_EXCEEDED:
            routers.append(icmp_res.src)

print routers

def is_local_network(ip):
    return re.compile("^192\.168").match(ip) != None

def geolocate(ip):
    if is_local_network(ip):
        return "Local Network"

    res = requests.get(GEOLOCATION_ENDPOINT, params={"ip": ip, "position": "true"})
    return res.json()

print map(geolocate, routers)
