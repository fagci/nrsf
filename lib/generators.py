from ipaddress import IPv4Address, IPv4Network
from random import randrange


def generate_ips(count=1000000, netork_range = ''):
    if netork_range:
        for host in IPv4Network(netork_range, strict=False).hosts():
            yield str(host)
        return
    while count != 0: # negative values makes infinite generator
        ip = IPv4Address(randrange(0, 0xffffffff))
        if ip.is_link_local or ip.is_loopback or ip.is_multicast or ip.is_private or ip.is_reserved:
            continue
        count -= 1
        yield str(ip)
        continue
