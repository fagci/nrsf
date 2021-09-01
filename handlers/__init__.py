from pathlib import Path
from socket import (
    SOL_SOCKET,
    SO_BINDTODEVICE,
    SO_LINGER,
    SO_REUSEADDR,
    create_connection,
    timeout as SocketTimeoutError,
)
from struct import pack
from threading import Lock
from time import sleep, time

LINGER = pack('ii', 1, 0)

class PortStatus:
    UNKNOWN = 0
    OPENED = 1
    CLOSED = 2
    FILTERED = 3

class Base:
    PORT = 0
    TRIM = True
    SHOW_EMPTY = False
    DEBUG = False

    __slots__ = ('__print_lock', '__out_path', 'port_status', 'socket', 'ip', 'address', 'iface')

    __print_lock: Lock
    __out_path: Path

    def __init__(self, ip, iface=''):
        self.socket = None
        self.iface = iface
        self.ip = ip
        self.address = (ip, self.PORT)
        self.port_status = PortStatus.UNKNOWN

    def handle(self):
        """Make some things here while that port is open"""
        if not self.socket:
            return
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
                print(f'[{self.get_name()}]', repr(e))
        except Exception as e:
            print(e)
            raise

    def pre(self):
        """Make some initial things here
        ex.: wrap socket with SSL"""
        pass

    def pre_open(self):
        pass

    def post(self):
        """Make some things here after knowing that port is open
        ex.: connect to FTP without wrapping socket or reinvent client"""
        pass

    def post_open(self):
        pass

    def __enter__(self):
        self.pre()
        start = time()

        while time() - start < 2:
            try:
                self.socket = create_connection(self.address)
                setsockopt = self.socket.setsockopt
                if self.iface:
                    setsockopt(SOL_SOCKET, SO_BINDTODEVICE, self.iface.encode())
                setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                setsockopt(SOL_SOCKET, SO_LINGER, LINGER)
                self.port_status = PortStatus.OPENED
                self.pre_open()
            except KeyboardInterrupt:
                raise
            except SocketTimeoutError:
                break
            except OSError:
                sleep(1)

        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.socket:
            self.socket.close()
        
        self.post()

        if self.socket:
            self.post_open()

        is_interrupt = isinstance(exc_value, KeyboardInterrupt)
        return not is_interrupt

    def read(self, count=1024):
        return self.socket.recv(count).decode(errors='ignore')

    def write(self, text):
        self.socket.send(text)

    def dialog(self, text, count=1024):
        self.write(text)
        return self.read(count)
    
    def process(self):
        """NotImplemented"""
        return self.read()

    @classmethod
    def get_name(cls):
        return cls.__module__.split('.')[-1]


    def print(self, res):
        is_default = False
        if self.process.__doc__ == 'NotImplemented':
            is_default = True
        print(f'[{self.get_name()}{"(default strategy)" if is_default else ""}] {self.ip}:{self.PORT}')
        print(res, end='\n\n')

        out_dir = self.__out_path / self.get_name()
        out_dir.mkdir(exist_ok=True)
        
        with (out_dir / 'things.txt').open('a') as f:
            res_f = str(res).replace("\n", "\\n").replace('\r', '')
            f.write(f'{self.ip}:{self.PORT} {res_f}\n')


    @staticmethod
    def set_print_lock(lock):
        Base.__print_lock = lock

    @staticmethod
    def set_output_path(path):
        Base.__out_path = path
