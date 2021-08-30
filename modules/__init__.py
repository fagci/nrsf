from socket import timeout as SocketTimeoutError
class Base:
    PORT = 0
    TRIM = True
    SHOW_EMPTY = False
    DEBUG = False

    def __init__(self, print_lock):
        self.print_lock = print_lock

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
                print(f'[self.__class__.__name__]',repr(e))
        except Exception as e:
            print(e)
            raise
    
    def process(self, s):
        raise NotImplementedError

    def print(self, ip, res):
        print(f'[{self.__class__.__name__}] {ip}:{self.PORT}')
        print(res, end='\n\n')
