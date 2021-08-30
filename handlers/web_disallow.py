from handlers import Base
from re import compile as re_compile, IGNORECASE, MULTILINE

class Handler(Base):
    PORT = 80
    DISALLOW_RE = re_compile(r'^User-agent:\s+\*$[\n\r]+^Disallow:\s+/$', IGNORECASE | MULTILINE)

    def process(self, s):
        host, _ = s.getpeername()
        robots_request = (
            'GET /robots.txt HTTP/1.1\r\n'
            f'Host: {host}\r\n'
            'User-Agent: Mozilla/5.0\r\n\r\n'
        )
        
        s.send(robots_request.encode())
        robots = s.recv(1024).decode(errors='ignore')

        if not self.DISALLOW_RE.findall(robots):
            return

        return '\n'.join(set(filter(lambda ln: ln.startswith('Disallow'), robots.split('\n'))))

