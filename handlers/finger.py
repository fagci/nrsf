from handlers import Base

class Handler(Base):
    PORT = 79
    def process(self):
        return self.dialog(b'root\n')
