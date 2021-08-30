from handlers import Base

class Handler(Base):
    PORT = 70
    def process(self):
        self.write(b'\r\n')
        return self.read()
