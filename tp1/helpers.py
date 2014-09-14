import scapy.utils
import collections

# Sample of ARP packages.
#
# ARPSample#src: [List[String]] holds all the source ips in the sample.
# ARPSample#dst: [List[String]] holds all the destination ips in the sample.
ARPSample = collections.namedtuple("ARPSample", ["src", "dst"])

# Count the occurrances of each ip in an ARPSample.
#
# IPOccurrence#src: [Int] the times a given ip was seen in a sample as a source address.
# IPOccurrence#dst: [Int] the times a given ip was seen in a sample as a destination address.
IPOccurrence = collections.namedtuple("IPOccurrence", ["src", "dst"])

# Turn a ARP sample pcap file into a Tuple of ips.
# For each ARP package in the sample, we extract the source and destination ips.
#
# pcap_file: [String] relative path to the ARP pcap file.
#
# return: [ARPSample]
def load_sources(pcap_file):
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

# Count how many times each ip in the sample was seen as source and destination.
#
# arp_sample: [ARPSample] the Tuple representing the sample.
#
# return: [Dict[String][IPOccurrence]] keys are ips and values are occurrences.
def count_occurrences(arp_sample):
    ips = ips_in_sample(arp_sample)
    occurrences = {}

    for ip in ips:
        occurrences[ip] = IPOccurrence(src=arp_sample.src.count(ip), dst=arp_sample.dst.count(ip))

    return occurrences

