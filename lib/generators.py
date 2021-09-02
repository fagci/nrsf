from ipaddress import IPv4Address
from random import randrange


def generate_ips(count=1000000):
    while count > 0:
        ip = IPv4Address(randrange(0, 0xffffffff))
        if ip.is_link_local or ip.is_loopback or ip.is_multicast or ip.is_private or ip.is_reserved:
            continue
        count -= 1
        yield str(ip)
        continue
