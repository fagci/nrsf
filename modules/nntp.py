"""News"""
from modules import Base

class Nntp(Base):
    PORT = 119

    def process(self, s):
        return s.recv(1024).decode(errors='ignore')
