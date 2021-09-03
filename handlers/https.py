from ssl import create_default_context

from handlers.http import Handler as HttpHandler


class Handler(HttpHandler):
    __slots__ = ('__ctx')

    PORT = 443
    
    def wrap(self, socket):
        self.__ctx = create_default_context()
        self.__ctx.check_hostname = False
        return self.__ctx.wrap_socket(socket, server_hostname=self.ip)

