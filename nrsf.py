#!/usr/bin/env python3

from argparse import ArgumentParser
from framework import NRSF
from socket import setdefaulttimeout




def stalk(limit, workers, modules_to_load, debug=False, iface=''):
    app = NRSF(modules_to_load,iface,debug,workers, limit)

    print('Stalking...', end='\n\n')
    app.run()


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

