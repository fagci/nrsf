import ssl

from handlers.http import Handler as HttpHandler


class Handler(HttpHandler):
    __slots__ = ('__ctx')

    PORT = 443

    def wrap(self, socket):
        self.__ctx = ssl._create_unverified_context()
        return self.__ctx.wrap_socket(
            socket,
            server_hostname=self.ip,
        )
