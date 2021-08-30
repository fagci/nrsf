#!/usr/bin/env python3

from argparse import ArgumentParser
from pkgutil import iter_modules
from random import random
from socket import (
    SHUT_RDWR,
    SOL_SOCKET,
    SO_LINGER,
    SO_REUSEADDR,
    setdefaulttimeout,
    socket,
)
from struct import pack
import sys
from time import sleep

from lib.generators import generate_ips
from lib.processors import Processor

LINGER = pack('ii', 1, 0)

def scan(ip_address, _, handlers):
    for handler_class in handlers:
        ip = str(ip_address)

        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.setsockopt(SOL_SOCKET, SO_LINGER, LINGER)

        handler = None
        
        if s.connect_ex((ip, handler_class.PORT)) == 0:
            handler = handler_class(s, ip)
            handler.handle()
            s.close()

        if handler:
            handler.post()

        if len(handlers) > 1:
            sleep(1 + random()/2)


def stalk(limit, workers, modules_to_load, debug=False):
    handlers = []

    proc = Processor()

    for _, m, _ in iter_modules(['handlers']):
        if m.startswith('_') or (m.lower() not in modules_to_load):
            continue
        module = getattr(__import__(f'handlers.{m}'), m)
        handler = getattr(module, 'Handler')
        handler.set_print_lock(proc.print_lock)
        if debug:
            handler.DEBUG = True
        handlers.append(handler)

    if handlers:
        print('Loaded handlers:')
        for h in handlers:
            print('-', h.__class__.__name__, f'({h.PORT} port)')
    else:
        print('No handlers loaded, exiting.')
        sys.exit()

    print('Stalking...', end='\n\n')

    proc.process_each(scan, generate_ips(limit), workers, handlers)


if __name__ == '__main__':
    parser = ArgumentParser(description='Netrandom stalking framework')
    parser.add_argument('modules', type=str, nargs='+', default=[])
    parser.add_argument('--timeout', type=float, default=0.75)
    parser.add_argument('--limit', type=int, default=1000000)
    parser.add_argument('--workers', type=int, default=512)
    parser.add_argument('--debug', type=bool, default=False)
    args = parser.parse_args()
    setdefaulttimeout(args.timeout)
    stalk(args.limit, args.workers, args.modules, args.debug)

