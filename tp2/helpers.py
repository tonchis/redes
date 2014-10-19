import requests
import re
import pprint

GEOLOCATION_ENDPOINT = "http://api.hostip.info/get_json.php"

def add(x, y):
        return x + y

def is_local_network(ip):
    return re.compile("^192\.168").match(ip) != None

def geolocate(ip):
    if is_local_network(ip):
        return "Local Network"

    res = requests.get(GEOLOCATION_ENDPOINT, params={"ip": ip, "position": "true"})
    return res.json()

def zrtt_i(array, avg_rtt, standard_deviation_rtt):
    return map(lambda rtt_i: round((rtt_i - avg_rtt)/standard_deviation_rtt, 3), array)

def puts(data, name, print_type):
    if print_type == 1:
        print name
        print " = "
        pprint.pprint(data)
    else:
        print name
        print " = "
        print data
