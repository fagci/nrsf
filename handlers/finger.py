from handlers import Base

class Handler(Base):
    PORT = 79
    def process(self):
        self.write(b'root\n')
        return self.read()
