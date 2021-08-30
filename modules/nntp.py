"""News"""
from modules import Base

class Nntp(Base):
    PORT = 119

    def process(self, s, _):
        return s.recv(1024).decode(errors='ignore')
