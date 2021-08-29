class Base:
    PORT = 0

    def __init__(self, print_lock):
        self.print_lock = print_lock

    def _process(self, s, ip):
        res = self.process(s, ip)
        with self.print_lock:
            self.print(ip, res)
    
    def process(self, s, ip):
        raise NotImplementedError

    def print(self, ip, res):
        print(f'{ip}:{self.PORT}')
        print(res, end='\n\n')
