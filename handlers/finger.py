"""Finger"""
from handlers import Base

class Finger(Base):
    PORT = 79
    def process(self, s):
        s.send(b'root\n')
        return s.recv(1024).decode(errors='ignore')
