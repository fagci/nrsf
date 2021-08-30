from socket import timeout as SocketTimeoutError
class Base:
    PORT = 0
    TRIM = True
    SHOW_EMPTY = False
    DEBUG = False

    def __init__(self, print_lock):
        self.print_lock = print_lock

    def _process(self, s, ip):
        try:
            res = self.process(s, ip)
            if self.TRIM:
                res = res.strip()
            if res or self.SHOW_EMPTY:
                with self.print_lock:
                    self.print(ip, res)
        except (ConnectionError, SocketTimeoutError) as e:
            if self.DEBUG:
                print(f'[self.__class__.__name__]',repr(e))
    
    def process(self, s, ip):
        raise NotImplementedError

    def print(self, ip, res):
        print(f'[{self.__class__.__name__}] {ip}:{self.PORT}')
        print(res, end='\n\n')
