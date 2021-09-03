from handlers import Base


class Handler(Base):
    PORT = 80

    def pre_connect(self):
        with self._print_lock:
            print('pre_connect')

    def setup(self):
        with self._print_lock:
            print('setup')

    def post_connect(self):
        with self._print_lock:
            print('post_connect')

    def wrap(self, socket):
        with self._print_lock:
            print('wrap')
        return socket

    def pre_handle(self):
        with self._print_lock:
            print('pre_handle')

    def handle(self):
        with self._print_lock:
            print('handle')

    def post_handle(self):
        with self._print_lock:
            print('post_handle')

    def post_disconnect(self):
        with self._print_lock:
            print('post_disconnect')
