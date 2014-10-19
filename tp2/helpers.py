def add(x, y):
        return x + y

def is_local_network(ip):
    return re.compile("^192\.168").match(ip) != None

def geolocate(ip):
    if is_local_network(ip):
        return "Local Network"

    res = requests.get(GEOLOCATION_ENDPOINT, params={"ip": ip, "position": "true"})
    return res.json()

def zrtt_i(array):
    return map(lambda rtt_i: (rtt_i - avg_rtt)/standard_deviation_rtt, array)

def puts(data, options, name=""):
    if options.puts == 0:
        print name
        print " = "
        pprint.pprint(data)
    else:
        print name
        print " = "
        print data
