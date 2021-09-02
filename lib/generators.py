from ipaddress import IPv4Address
from random import randrange


def generate_ips(count=1000000):
    while count > 0:
        ip = IPv4Address(randrange(0, 0xffffffff))
        if ip.is_global:
            count -= 1
            yield str(ip)
            continue
