"""Finger"""
from modules import Base

class Finger(Base):
    PORT = 79
    def process(self, s, _):
        s.send(b'root\n')
        return s.recv(1024).decode(errors='ignore')