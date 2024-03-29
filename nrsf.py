#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path

from framework import NRSF

if __name__ == '__main__':
    parser = ArgumentParser(description='Netrandom stalking framework')

    parser.add_argument('modules', type=str, nargs='+', default=[])
    parser.add_argument('-t', '--timeout', type=float, default=1, help='connect timeout')
    parser.add_argument('-l', '--limit', type=int, default=1000000, help='max generated ips to check')
    parser.add_argument('-w', '--workers', type=int, default=512)
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('-i', '--iface', type=str, default='')
    parser.add_argument('-o', '--output_path', type=str, default='./out')
    parser.add_argument('--network', type=str, default='')

    args, unknown = parser.parse_known_args()

    output_path = Path(args.output_path).resolve()

    app = NRSF(args.modules, args.iface, args.debug, args.timeout, output_path, unknown)

    app.run(args.limit, args.workers, args.network)
