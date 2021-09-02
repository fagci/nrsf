from pathlib import Path
from socket import (
    SOL_SOCKET,
    SOL_TCP,
    SO_BINDTODEVICE,
    SO_LINGER,
    SO_REUSEADDR,
    TCP_NODELAY,
    create_connection,
    setdefaulttimeout,
    socket as Socket,
    timeout as SocketTimeoutError,
)
from struct import pack
import sys
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
    TRIM_RESULT = True
    SHOW_EMPTY_RESULT = False
    DEBUG = False

    __slots__ = ('_print_lock', '__out_path', 'port_status', 'socket',
                 '_socket', 'ip', 'address', '__iface')

    _print_lock: Lock
    __out_path: Path
    __iface: bytes

    def __init__(self, ip):
        self._socket: Socket = None
        self.socket: Socket = None
        self.ip = ip
        self.address = (ip, self.PORT)
        self.port_status = PortStatus.UNKNOWN

    def __call__(self):
        """Make some things here while that port is open"""
        if not self.socket:
            return

        try:
            res = self.process()
            if self.TRIM_RESULT and res:
                res = res.strip()
            if res or self.SHOW_EMPTY_RESULT:
                with self._print_lock:
                    self.print(res)
        except KeyboardInterrupt:
            raise
        except (ConnectionError, SocketTimeoutError) as e:
            if self.DEBUG:
                with self._print_lock:
                    print(f'[{self.get_name()}]', repr(e), file=sys.stderr)
        except Exception as e:
            with self._print_lock:
                print(repr(e), file=sys.stderr)
            raise

    def pre(self):
        """Before connect"""
        pass

    def pre_wrap(self, socket):
        """Make some initial things here
        ex.: wrap socket with SSL"""
        return socket

    def setup(self):
        """Set socket options"""
        self._socket.settimeout(self.__timeout)
        setsockopt = self._socket.setsockopt
        if self.__iface:
            setsockopt(SOL_SOCKET, SO_BINDTODEVICE, self.__iface)
        setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        setsockopt(SOL_SOCKET, SO_LINGER, LINGER)
        setsockopt(SOL_TCP, TCP_NODELAY, True)

    def pre_open(self):
        """Before process when socket open"""
        pass

    def process(self):
        """NotImplemented"""
        return self.read()

    def post(self):
        pass

    def post_open(self):
        """Make some things here after knowing that port is open
        ex.: connect to FTP without wrapping socket or reinvent client"""
        pass

    def __enter__(self):
        self.pre()
        start = time()

        while time() - start < 2:
            try:
                self._socket = Socket()
                self.setup()
                self._socket.connect(self.address)
                self.port_status = PortStatus.OPENED
                self.socket = self.pre_wrap(self._socket)
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

    def print(self, res):
        is_default = False
        if self.process.__doc__ == 'NotImplemented':
            is_default = True
        print(
            f'[{self.get_name()}{"(default strategy)" if is_default else ""}] {self.ip}:{self.PORT}'
        )
        print(res, end='\n\n')

        out_dir = self.__out_path / self.get_name()
        out_dir.mkdir(exist_ok=True, parents=True)

        with (out_dir / 'things.txt').open('a') as f:
            res_f = str(res).replace("\n", "\\n").replace('\r', '')
            f.write(f'{self.ip}:{self.PORT} {res_f}\n')

    def read(self, count=1024):
        return self.socket.recv(count).decode(errors='ignore')

    def write(self, text):
        self.socket.send(text)

    def dialog(self, text, count=1024):
        self.write(text)
        return self.read(count)

    @classmethod
    def get_name(cls):
        return cls.__module__.split('.')[-1]

    @staticmethod
    def set_iface(iface):
        Base.__iface = iface.encode()

    @staticmethod
    def set_timeout(timeout):
        # setdefaulttimeout(timeout)
        Base.__timeout = timeout

    @staticmethod
    def set_print_lock(lock):
        Base._print_lock = lock

    @staticmethod
    def set_output_path(path):
        Base.__out_path = path
