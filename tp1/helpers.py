import scapy.utils
import collections

ARPSources = collections.namedtuple("ARPSources", ["src", "dst"])
IPOccurrence = collections.namedtuple("IPOccurrence", ["src", "dst"])

def load_sources(pcap_file):
    arp_packages = scapy.utils.rdpcap(pcap_file)

    arp_sources = ARPSources(src=[], dst=[])

    for package in arp_packages:
        arp_sources.src.append(package.psrc)
        arp_sources.dst.append(package.pdst)

    return arp_sources

def ips_in_sample(arp_sources):
    return set(arp_sources.src).union(set(arp_sources.dst))

def count_occurrences(arp_sources):
    ips = ips_in_sample(arp_sources)
    occurrences = {}

    for ip in ips:
        occurrences[ip] = IPOccurrence(src=arp_sources.src.count(ip), dst=arp_sources.dst.count(ip))

    return occurrences

