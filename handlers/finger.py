from handlers import Base


class Handler(Base):
    PORT = 79

    def handle(self):
        return self.dialog(b'root\n')
