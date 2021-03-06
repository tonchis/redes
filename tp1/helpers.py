from __future__ import division
import scapy.utils
import collections
import math
import operator

# Sample of ARP packets.
#
# ARPSample#src: [List[String]] holds all the source ips in the sample.
# ARPSample#dst: [List[String]] holds all the destination ips in the sample.
ARPSample = collections.namedtuple("ARPSample", ["src", "dst"])

# Turn a ARP sample pcap file into a Tuple of ips.
# For each ARP package in the sample, we extract the source and destination ips.
#
# pcap_file: [String] relative path to the ARP pcap file.
#
# return: [ARPSample]
def load_sample(pcap_file, count=-1):
    arp_packets = scapy.utils.rdpcap(pcap_file, count)

    arp_sample = ARPSample(src=[], dst=[])

    for package in arp_packets:
        arp_sample.src.append(package.psrc)
        arp_sample.dst.append(package.pdst)

    return arp_sample

# All the ips seen in a given sample, both as source and destination, without repetition.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [Set[String]] all the ips.
def ips_in_sample(arp_sample):
    return set(arp_sample.src).union(set(arp_sample.dst))

# Holds the relative frequency of each ip in the ARPSample.
#
# IPFrequency#src: [List[Float]] the relative frequency of each ip in the sample as a source address.
# IPFrequency#dst: [List[Float]] the relative frequency of each ip in the sample as a destination address.
IPFrequency = collections.namedtuple("IPFrequency", ["src", "dst"])

# Calculate the relative frequency of each ip in the sample.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [IPFrequency] the Tuple representing the frequency.
def frequency_of_occurrence(arp_sample):
    ips = ips_in_sample(arp_sample)

    return IPFrequency(src=relative_frequency(ips, arp_sample.src), dst=relative_frequency(ips, arp_sample.dst))

def relative_frequency(ips, sample):
    return map(lambda ip: sample.count(ip) / len(sample), ips)

def ips_and_frequencies(arp_sample):
    ips = ips_in_sample(arp_sample)

    return IPFrequency(src=ip_freq_dict(ips, arp_sample.src), dst=ip_freq_dict(ips, arp_sample.dst))

def ip_freq_dict(ips, sample):
    dictionary = {}
    for ip in ips:
        dictionary[ip] = sample.count(ip) / len(sample)

    return dictionary

# Holds the entropy of the ARPSample.
#
# ARPSampleEntropy#src: [Float] entropy of source.
# ARPSampleEntropy#dst: [Float] entropy of destination.
ARPSampleEntropy = collections.namedtuple("ARPSampleEntropy", ["src", "dst"])

# Holds distinguished nodes
ARPSampleDistinguished = collections.namedtuple("ARPSampleDistinguished", ["src", "dst"])

# Calculates the entropy of the sample.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [ARPSampleEntropy] the Tuple representing the entropy.
def entropy(arp_sample):
    frequency = frequency_of_occurrence(arp_sample)

    return ARPSampleEntropy(src=map_reduce_entropy(frequency.src), dst=map_reduce_entropy(frequency.dst))

def add(x, y):
    return x + y

def information(frequency):
    return -math.log(frequency, 2)

def map_reduce_entropy(frequencies):
    weighted_information = lambda x: 0.0 if x == 0.0 else information(x) * x
    return reduce(add, map(weighted_information, frequencies))

def count_packets_between(arp_sample, src, dst):
    return reduce(add, list((1 if arp_sample.src[index] == src and arp_sample.dst[index] == dst else 0) for index in range(len(arp_sample.src))))

def distinguished_nodes(arp_sample):
    sample_entropy = entropy(arp_sample)
    ips = ips_and_frequencies(arp_sample)
    return ARPSampleDistinguished(src=select_distinguished_nodes(ips.src, sample_entropy.src),
                                  dst=select_distinguished_nodes(ips.dst, sample_entropy.dst))

def select_distinguished_nodes(ips, sample_entropy):
    distinguished_nodes = {}
    for ip in ips.viewkeys():
        freq = ips[ip]
        if freq > 0.0 and information(freq) < sample_entropy:
            distinguished_nodes[ip] = information(freq)

    return distinguished_nodes

def sort_by_info(ips):
    return sorted(ips.items(), key=operator.itemgetter(1))
