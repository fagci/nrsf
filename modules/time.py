"""Time"""
from modules import Base

class Time(Base):
    PORT = 13

    def process(self, s):
        return s.recv(1024).decode(errors='ignore')
