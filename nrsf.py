#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from pkgutil import iter_modules
from socket import SOL_SOCKET, SO_BINDTODEVICE, SO_LINGER, SO_REUSEADDR, setdefaulttimeout, socket
from struct import pack
import sys

from lib.generators import generate_ips
from lib.processors import Processor

OUTPUT_PATH = Path(__file__).resolve().parent / 'out'

LINGER = pack('ii', 1, 0)

def scan(ip_address, _, handlers, iface):
    for handler_class in handlers:
        ip = str(ip_address)

        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.setsockopt(SOL_SOCKET, SO_LINGER, LINGER)
        if iface:
            s.setsockopt(SOL_SOCKET, SO_BINDTODEVICE, iface.encode())

        
        status = s.connect_ex((ip, handler_class.PORT))

        if status == 0:
            handler = handler_class(s, ip)
            handler.handle()
            s.close()
            handler.post()


def stalk(limit, workers, modules_to_load, debug=False, iface=''):
    handlers = []

    proc = Processor()

    for _, m, _ in iter_modules(['handlers']):
        if m.startswith('_') or (m.lower() not in modules_to_load):
            continue
        module = getattr(__import__(f'handlers.{m}'), m)
        handler = getattr(module, 'Handler')
        handler.set_print_lock(proc.print_lock)
        handler.set_output_path(OUTPUT_PATH)
        if debug:
            handler.DEBUG = True
        handlers.append(handler)

    if handlers:
        print('Loaded handlers:')
        for h in handlers:
            print('-', h.name, f'({h.PORT} port)')
    else:
        print('No handlers loaded, exiting.')
        sys.exit()

    print('Stalking...', end='\n\n')

    proc.process_each(scan, generate_ips(limit), workers, handlers, iface)


if __name__ == '__main__':
    parser = ArgumentParser(description='Netrandom stalking framework')

    parser.add_argument('modules', type=str, nargs='+', default=[])
    parser.add_argument('--timeout', type=float, default=0.75)
    parser.add_argument('--limit', type=int, default=1000000)
    parser.add_argument('--workers', type=int, default=512)
    parser.add_argument('--debug', type=bool, default=False)
    parser.add_argument('--iface', type=str, default='')

    args = parser.parse_args()

    setdefaulttimeout(args.timeout)
    stalk(args.limit, args.workers, args.modules, args.debug, args.iface)

