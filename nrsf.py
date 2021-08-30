#!/usr/bin/env python3

from pkgutil import iter_modules
from socket import setdefaulttimeout, socket

from lib.generators import generate_addresses
from lib.processors import Processor


def scan(addr, _, modules):
    ip, port = addr
    with socket() as s:
        if s.connect_ex(addr) == 0:
            for module in modules:
                if module.PORT == port:
                    return module.handle(s)


def stalk(count, workers):
    modules = []
    ports = set()

    proc = Processor()

    for _, m, _ in iter_modules(['modules']):
        if m.startswith('_'):
            continue
        c_name = ''.join(p[0].upper()+p[1:] for p in m.split('_'))
        module = getattr(getattr(__import__(f'modules.{m}'), m), c_name)(proc.print_lock)
        modules.append(module)
        ports.add(module.PORT)
        print(m, module.PORT)

    print('Stalking...', end='\n\n')

    proc.process_each(scan, generate_addresses(count, ports), workers, modules)


if __name__ == '__main__':
    setdefaulttimeout(0.75)
    stalk(1000000, 512)

