#!/usr/bin/env python

import scapy.all
import logging
import optparse
import requests # pip install requests
import re
import time
import collections

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

option_parser = optparse.OptionParser()
option_parser.add_option("-m", "--max-ttl", dest="max_ttl", default="64", type="int")
option_parser.add_option("-u", "--url", dest="url", default="www.google.com")
option_parser.add_option("-t", "--tiemout", dest="timeout", default="1", type="int")
option_parser.add_option("-v", "--verbose", dest="verbose", default="0", type="int")
option_parser.add_option("-g", "--geolocation", dest="geolocation", default="1", type="int")

options, reminder = option_parser.parse_args()

# Router#ips: [List[String]] holds the router ip.
# Router#rtt: [List[Float]] holds the round trip time it took to comunicate with the router.
Router = collections.namedtuple("Router", ["ips", "rtt"])

ECHO_REPLY = 0
TIME_EXCEEDED = 11
GEOLOCATION_ENDPOINT = "http://api.hostip.info/get_json.php"

routers = Router(ips=[], rtt=[])
for ttl in range(1, options.max_ttl + 1):
    print "TTL:", ttl
    itime = time.time()    
    (res, rtt) = (scapy.sendrecv.sr1(scapy.layers.inet.IP(dst=options.url, ttl=ttl) / scapy.layers.inet.ICMP(), timeout=options.timeout, verbose=options.verbose), time.time()-itime)
    if res:
        icmp = res.getlayer(scapy.layers.inet.ICMP)
        ip = res.getlayer(scapy.layers.inet.IP)
        src = ip.src
        print "  from", src
        if icmp.type == ECHO_REPLY:
            routers.ips.append(src)
            routers.rtt.append(rtt)
            break
        elif icmp.type == TIME_EXCEEDED:
            routers.ips.append(src)
            routers.rtt.append(rtt)
        #maybe we should take into consideration the icmp packages with other types. just sayin' 
    else:
        print "  no answer"

print routers.ips
print routers.rtt

def is_local_network(ip):
    return re.compile("^192\.168").match(ip) != None

def geolocate(ip):
    if is_local_network(ip):
        return "Local Network"

    res = requests.get(GEOLOCATION_ENDPOINT, params={"ip": ip, "position": "true"})
    return res.json()

if(options.geolocation == 1):	
	print map(geolocate, routers.ips)
