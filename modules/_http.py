from modules import Base

class Http(Base):
    PORT = 80
    def process(self, s):
        ip, _ = s.getpeername()
        s.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n'.encode())
        return s.recv(1024).decode(errors='ignore')

