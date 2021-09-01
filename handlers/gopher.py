from handlers import Base

class Handler(Base):
    PORT = 70
    def process(self):
        return self.dialog(b'\r\n')
