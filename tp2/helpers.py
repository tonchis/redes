import requests
import re
import pprint

GEOLOCATION_ENDPOINT = "http://api.hostip.info/get_json.php"

def add(x, y):
        return x + y

def is_local_network(ip):
    return re.compile("^192\.168").match(ip) != None

def geolocate(ip):
    if ip == None:
        return "No answer"

    if is_local_network(ip):
        return "Local Network"

    res = requests.get(GEOLOCATION_ENDPOINT, params={"ip": ip, "position": "true"})
    json = res.json()

    if json["country_code"] == "XX":
        return "Couldn't geolocate ip {ip}".format(**locals())

    return { "country": json["country_name"], "city": json["city"], "position": {"latitude": json["lat"], "longitude": json["lng"]} }

def puts(data, name, print_type):
    if print_type == 1:
        print name
        print " = "
        pprint.pprint(data)
    else:
        print name
        print " = "
        print data

def map_with_two_decimals(ary):
    return map(lambda item: round(item, 3), ary)

def store(routers, src, rtt_i):
    routers.ips.append(src)
    routers.rtt.append(rtt_i)
