"""Systat"""
from modules import Base

class Systat(Base):
    PORT = 11

    def process(self, s):
        return s.recv(1024).decode(errors='ignore')
