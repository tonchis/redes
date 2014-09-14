from __future__ import division
import scapy.utils
import collections
import math

# Sample of ARP packages.
#
# ARPSample#src: [List[String]] holds all the source ips in the sample.
# ARPSample#dst: [List[String]] holds all the destination ips in the sample.
ARPSample = collections.namedtuple("ARPSample", ["src", "dst"])

# Count the relative frequency of each ip in the ARPSample.
#
# IPFrequency#src: [List[Float]] the relative frequency of each ip in the sample as a source address.
# IPFrequency#dst: [List[Float]] the relative frequency of each ip in the sample as a destination address.
IPFrequency = collections.namedtuple("IPFrequency", ["src", "dst"])

# Sotres entropy of the ARPSample.
#
# ARPSampleEntropy#src: [Int] entropy of source.
# ARPSampleEntropy#dst: [Int] entropy of destination.
ARPSampleEntropy = collections.namedtuple("ARPSampleEntropy", ["src", "dst"])

# Turn a ARP sample pcap file into a Tuple of ips.
# For each ARP package in the sample, we extract the source and destination ips.
#
# pcap_file: [String] relative path to the ARP pcap file.
#
# return: [ARPSample]
def load_sample(pcap_file):
    arp_packages = scapy.utils.rdpcap(pcap_file)

    arp_sample = ARPSample(src=[], dst=[])

    for package in arp_packages:
        arp_sample.src.append(package.psrc)
        arp_sample.dst.append(package.pdst)

    return arp_sample

# All the ips seen in a given sample, both as source and destination.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [Set[String]] all the ips.
def ips_in_sample(arp_sample):
    return set(arp_sample.src).union(set(arp_sample.dst))

# Count the relative frequency of each ip in the sample.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [IPFrequency]
def frequency_of_occurrence(arp_sample):
    ips = ips_in_sample(arp_sample)
    sample_size = len(arp_sample.src) # dst is the same length.

    src_frequency = map(lambda ip: arp_sample.src.count(ip) / sample_size, ips)
    dst_frequency = map(lambda ip: arp_sample.dst.count(ip) / sample_size, ips)

    return IPFrequency(src=src_frequency, dst=dst_frequency)

# Calculates the entropy of the sample.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [ARPSampleEntropy] the Tuple representing the entropy.
def entropy(arp_sample):
    frequency = frequency_of_occurrence(arp_sample)

    weighted_information = lambda x: math.log(x, 2) * x

    src_weighted_information = map(weighted_information, frequency.src)
    dst_weighted_information = map(weighted_information, frequency.dst)

    add = lambda x, y: x + y

    return ARPSampleEntropy(src=reduce(add, src_weighted_information), dst=reduce(add, dst_weighted_information))

