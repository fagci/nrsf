#!/usr/bin/env python3

from pkgutil import iter_modules
from random import random
from socket import setdefaulttimeout, socket, SOL_SOCKET, SO_LINGER
from struct import pack
from time import sleep

from lib.generators import generate_ips
from lib.processors import Processor

LINGER = pack('ii', 1, 0)

def scan(ip_address, _, handlers):
    for handler in handlers:
        with socket() as s:
            s.setsockopt(SOL_SOCKET, SO_LINGER, LINGER)
            if s.connect_ex((str(ip_address), handler.PORT)) == 0:
                handler.handle(s)
        sleep(1 + random()/2)


def stalk(count, workers):
    handlers = []

    proc = Processor()

    for _, m, _ in iter_modules(['modules']):
        if m.startswith('_'):
            continue
        c_name = ''.join(p[0].upper()+p[1:] for p in m.split('_'))
        module = getattr(__import__(f'modules.{m}'), m)
        handler = getattr(module, c_name)(proc.print_lock)
        handlers.append(handler)
        print(m, handler.PORT)

    print('Stalking...', end='\n\n')

    proc.process_each(scan, generate_ips(count), workers, handlers)


if __name__ == '__main__':
    setdefaulttimeout(0.75)
    stalk(1000000, 512)

