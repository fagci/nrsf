from pathlib import Path
from socket import timeout as SocketTimeoutError
from threading import Lock

class Base:
    PORT = 0
    TRIM = True
    SHOW_EMPTY = False
    DEBUG = False
    __print_lock: Lock
    __out_path: Path

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
                print(f'[{self.name}]', repr(e))
        except Exception as e:
            print(e)
            raise

    def post(self):
        pass

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
