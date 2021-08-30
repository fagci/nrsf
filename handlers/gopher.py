"""Gopher"""
from handlers import Base

class Handler(Base):
    PORT = 70
    def process(self, s):
        s.send(b'\r\n')
        return s.recv(1024).decode(errors='ignore')
