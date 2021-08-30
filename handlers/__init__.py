from socket import timeout as SocketTimeoutError
import sys
from threading import Lock

class Base:
    PORT = 0
    TRIM = True
    SHOW_EMPTY = False
    DEBUG = False
    __print_lock: Lock

    def __init__(self, socket, ip):
        self.socket = socket
        self.ip = ip

    def handle(self):
        try:
            res = self.process()
            if self.TRIM and res:
                res = res.strip()
            if res or self.SHOW_EMPTY:
                with self.__print_lock:
                    self.print(res)
        except KeyboardInterrupt:
            raise
        except (ConnectionError, SocketTimeoutError) as e:
            if self.DEBUG:
                print(f'[{self.__class__.__module__.split(".")[-1]}]', repr(e))
        except Exception as e:
            print(e)
            raise

    def post(self):
        pass

    def read(self, count = 1024):
        return self.socket.recv(count).decode(errors='ignore')

    def write(self, text):
        self.socket.send(text)
    
    def process(self):
        """NotImplemented"""
        return self.read()


    def print(self, res):
        is_default = False
        if self.process.__doc__ == 'NotImplemented':
            is_default = True
        print(f'[{self.__class__.__module__.split(".")[-1]}{"(default strategy)" if is_default else ""}] {self.ip}:{self.PORT}')
        print(res, end='\n\n')

    @staticmethod
    def set_print_lock(lock):
        Base.__print_lock = lock
