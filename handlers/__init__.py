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
            res = self.process(s)
            if self.TRIM:
                res = res.strip()
            if res or self.SHOW_EMPTY:
                with self.print_lock:
                    self.print(s.getpeername(), res)
        except KeyboardInterrupt:
            raise
        except (ConnectionError, SocketTimeoutError) as e:
            if self.DEBUG:
                print(f'[{self.__class__.__name__}]', repr(e))
        except Exception as e:
            print(e)
            raise
    
    def process(self, s):
        """NotImplemented"""
        return s.recv(1024).decode(errors='ignore')


    def print(self, ip, res):
        if self.DEBUG and self.process.__doc__ == 'NotImplemented':
            with self.print_lock:
                print(f'[i {self.__class__.__name__}] Default handle strategy', file=sys.stderr)
        print(f'[{self.__class__.__name__}] {ip}:{self.PORT}')
        print(res, end='\n\n')
