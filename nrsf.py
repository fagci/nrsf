#!/usr/bin/env python3

from argparse import ArgumentParser

from framework import NRSF

if __name__ == '__main__':
    parser = ArgumentParser(description='Netrandom stalking framework')

    parser.add_argument('modules', type=str, nargs='+', default=[])
    parser.add_argument('--timeout', type=float, default=0.75)
    parser.add_argument('--limit', type=int, default=1000000)
    parser.add_argument('--workers', type=int, default=512)
    parser.add_argument('--debug', type=bool, default=False)
    parser.add_argument('--iface', type=str, default='')

    args = parser.parse_args()

    app = NRSF(args.modules, args.iface, args.debug, args.timeout, args.workers, args.limit)

    print('Stalking...', end='\n\n')
    app.run()
