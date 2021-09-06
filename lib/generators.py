from ipaddress import IPV4LENGTH, IPv4Address, IPv4Network
from random import randrange

MAX_IPV4 = 1 << IPV4LENGTH

def generate_ips(count=1000000, netork_range = ''):
    if netork_range:
        for host in IPv4Network(netork_range, strict=False).hosts():
            yield str(host)
        return
    while count != 0: # negative values makes infinite generator
        ip = IPv4Address(randrange(0, MAX_IPV4))
        if ip.is_global and not ip.is_multicast:
            count -= 1
            yield str(ip)
