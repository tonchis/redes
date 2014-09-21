#! /usr/bin/env python

from __future__ import print_function
import sys; sys.path.append("tp1")
import scapy.all
import helpers
import logging
import optparse

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

option_parser = optparse.OptionParser()
option_parser.add_option("-f", "--file", dest="file", default="tmp/arp.pcap")
option_parser.add_option("-c", "--count", dest="count", default="-1", type="int")
option_parser.add_option("-o", "--output", dest="output", default=sys.stdout)
option_parser.add_option("--ip", dest="ip")

options, reminder = option_parser.parse_args()

def edges_in_sample(arp_file, count=None, ip=None):
    arp_sample = helpers.load_sample(arp_file, count)

    accum = []

    if ip != None:
        sample = filter_by_ip(arp_sample, ip)
    else:
        sample = arp_sample

    for index in range(len(sample.src)):
        accum.append("  {0};".format(from_to(sample.src[index], sample.dst[index])))

    return "\n".join(accum)

def from_to(src, dst):
    return "\"{0}\" -> \"{1}\"".format(src, dst)

def render_dot_file(sample):
    return "\n".join(["digraph {", sample, "}"])

def filter_by_ip(arp_sample, ip):
    filtered_sample = helpers.ARPSample(src=[], dst=[])

    for index in range(len(arp_sample.src)):
        if arp_sample.src[index] == ip or arp_sample.dst[index] == ip:
            filtered_sample.src.append(arp_sample.src[index])
            filtered_sample.dst.append(arp_sample.dst[index])

    return filtered_sample

edges = edges_in_sample(options.file, options.count, ip=options.ip)

if options.output == sys.stdout:
    output = sys.stdout
else:
    output = open(options.output, "w")

print(render_dot_file(edges), file=output)

if options.output != sys.stdout:
    output.close()
