"""Quote of the day"""
from modules import Base

class Qotd(Base):
    PORT = 17

    def process(self, s, _):
        return s.recv(1024).decode(errors='ignore')
