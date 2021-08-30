from socket import timeout as SocketTimeoutError
import sys

class Base:
    PORT = 0
    TRIM = True
    SHOW_EMPTY = False
    DEBUG = False

    def __init__(self, print_lock, force_debug=False):
        self.print_lock = print_lock
        if force_debug:
            self.DEBUG = True

    def handle(self, s):
        try:
            addr = s.getpeername()
            res = self.process(s)
            if self.TRIM and res:
                res = res.strip()
            if res or self.SHOW_EMPTY:
                with self.print_lock:
                    self.print(addr, res)
        except KeyboardInterrupt:
            raise
        except (ConnectionError, SocketTimeoutError) as e:
            if self.DEBUG:
                print(f'[{self.__class__.__module__.split(".")[-1]}]', repr(e))
        except Exception as e:
            print(e)
            raise
    
    def process(self, s):
        """NotImplemented"""
        return s.recv(1024).decode(errors='ignore')


    def print(self, addr, res):
        is_default = False
        if self.process.__doc__ == 'NotImplemented':
            is_default = True
        print(f'[{self.__class__.__module__.split(".")[-1]}{"(default strategy)" if is_default else ""}] {addr[0]}:{addr[1]}')
        print(res, end='\n\n')
