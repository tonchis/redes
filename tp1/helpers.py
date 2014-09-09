import scapy.layers.l2

ARP = scapy.layers.l2.ARP

def who_has(package):
    if package.haslayer(ARP):
        arp = package.getlayer(ARP)
        return arp.op == arp.who_has
    return False

def arp_source_destination_print(package):
    return package.sprintf("%ARP.psrc%,%ARP.pdst%")
