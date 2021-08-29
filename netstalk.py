#!/usr/bin/env python3

from pkgutil import iter_modules
from socket import setdefaulttimeout, socket

from lib.generators import generate_addresses
from lib.processors import process_each


# ports = (
#     # 11, # systat (active users list)
#     13, # time
#     17, # qotd
#     # 70, # gopher
#     79, # finger
#     # 87, # talk (chat)
#     119, # nntp (news)
#     # 123, # ntp (time)
#     # 113, # statistics
# )


def scan(addr, pl, modules:dict):
    with socket() as s:
        r = s.connect_ex(addr)
        if r == 0:
            ip, port = addr
            try:
                for module in modules.values():
                    if module.PORT == port:
                        return module.process(pl, s, ip, port)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                # print(e)
                pass


def stalk(count=1000000, workers=None):
    modules = {}
    ports = set()
    for _, m, _ in iter_modules(['modules']):
        if m.startswith('_'):
            continue
        c_name = ''.join(p[0].upper()+p[1:] for p in m.split('_'))
        module = modules[m] = getattr(getattr(__import__(f'modules.{m}'), m), c_name)()
        ports.add(module.PORT)

    print('ports:', ports)


    process_each(scan, generate_addresses(count, ports), workers, modules)


if __name__ == '__main__':
    setdefaulttimeout(1)
    stalk(workers=1024)
