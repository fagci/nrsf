from handlers import Base

class Handler(Base):
    PORT = 70
    def handle(self):
        return self.dialog(b'\r\n')
