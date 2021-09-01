from pathlib import Path
from pkgutil import iter_modules
from socket import setdefaulttimeout
import sys

from lib.generators import generate_ips
from lib.processors import Processor

OUTPUT_PATH = Path(__file__).resolve().parent / 'out'


class NRSF:
    def __init__(self, modules_to_load, iface, debug, timeout, workers, limit):
        self.handlers = []
        self.proc = Processor()
        self.workers = workers
        self.limit = limit
        setdefaulttimeout(timeout)

        for _, m, _ in iter_modules(['handlers']):
            if m.startswith('_') or (m.lower() not in modules_to_load):
                continue
            module = getattr(__import__(f'handlers.{m}'), m)
            handler = getattr(module, 'Handler')
            handler.set_iface(iface)
            handler.set_print_lock(self.proc.print_lock)
            handler.set_output_path(OUTPUT_PATH)
            if debug:
                handler.DEBUG = True
            self.handlers.append(handler)

        if self.handlers:
            print('Loaded handlers:')
            for h in self.handlers:
                print('-', h.get_name(), f'({h.PORT} port)')
        else:
            print('No handlers loaded, exiting.')
            sys.exit()

    def scan(self, ip_address, _):
        for handler_class in self.handlers:
            ip = str(ip_address)

            with handler_class(ip) as handler:
                handler.handle()

    def run(self):
        self.proc.process_each(self.scan, generate_ips(self.limit),
                               self.workers)
