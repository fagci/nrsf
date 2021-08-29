class Base:
    PORT = 0

    def _process(self, pl, s, ip):
        res = self.process(s, ip)
        with pl:
            self.print(ip, res)
    
    def process(self, s, ip):
        raise NotImplementedError

    def print(self, ip, res):
        print(f'{ip}:{self.PORT}')
        print(res, end='\n\n')
