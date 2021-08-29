#!/usr/bin/env python3

from pkgutil import iter_modules
from socket import setdefaulttimeout, socket, timeout

from lib.generators import generate_addresses
from lib.processors import Processor


# ports = (
#     # 11, # systat (active users list)
#     # 87, # talk (chat)
#     119, # nntp (news)
#     # 123, # ntp (time)
#     # 113, # statistics
# )


def scan(addr, _, modules):
    with socket() as s:
        r = s.connect_ex(addr)
        if r == 0:
            ip, port = addr
            try:
                for module in modules.values():
                    if module.PORT == port:
                        return module._process(s, ip)
            except KeyboardInterrupt:
                raise
            except (ConnectionError, timeout):
                pass
            except Exception as e:
                print(e)
                raise


def stalk(count, workers):
    modules = {}
    ports = set()

    proc = Processor()

    for _, m, _ in iter_modules(['modules']):
        if m.startswith('_'):
            continue
        c_name = ''.join(p[0].upper()+p[1:] for p in m.split('_'))
        module = modules[m] = getattr(getattr(__import__(f'modules.{m}'), m), c_name)(proc.print_lock)
        ports.add(module.PORT)
        print(m, module.PORT)

    print('Stalking...', end='\n\n')

    proc.process_each(scan, generate_addresses(count, ports), workers, modules)


if __name__ == '__main__':
    setdefaulttimeout(1)
    stalk(1000000, 1024)

