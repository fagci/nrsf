from pathlib import Path
from pkgutil import iter_modules
import sys

from lib.generators import generate_ips
from lib.processors import Processor

OUTPUT_PATH = Path(__file__).resolve().parent / 'out'


class NRSF:
    def __init__(self, modules_to_load, iface, debug, timeout, workers, limit):
        self.limit = limit
        self.workers = workers

        handlers = []

        print('Loading handlers...')

        for _, m, _ in iter_modules(['handlers']):
            if m.startswith('_') or (m.lower() not in modules_to_load):
                continue
            module = getattr(__import__(f'handlers.{m}'), m)
            handler = getattr(module, 'Handler')

            handler.set_iface(iface)
            handler.set_timeout(timeout)
            handler.set_output_path(OUTPUT_PATH)
            if debug:
                handler.DEBUG = True

            handlers.append(handler)

            print('-', handler.get_name(), f'({handler.PORT} port)')

        if not handlers:
            print('No handlers loaded, exiting.')
            sys.exit()

        self.proc = Processor(handlers)


    def run(self):
        self.proc.process(generate_ips(self.limit), self.workers)
