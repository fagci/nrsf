from pkgutil import iter_modules

from lib.generators import generate_ips
from lib.processors import Processor



class NRSF:
    def __init__(self, modules_to_load, iface, debug, timeout, output_path):
        self.proc = Processor()

        print('Loading handlers...')

        for _, m, _ in iter_modules(['handlers']):
            if m.startswith('_') or (m.lower() not in modules_to_load):
                continue
            module = getattr(__import__(f'handlers.{m}'), m)
            handler = getattr(module, 'Handler')

            handler.set_iface(iface)
            handler.set_timeout(timeout)
            handler.set_output_path(output_path)

            if debug:
                handler.DEBUG = True

            self.proc.add_handler(handler)

    def run(self, limit, workers):
        self.proc.process(generate_ips(limit), workers)
