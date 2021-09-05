import ssl

from handlers.http import Handler as HttpHandler


class Handler(HttpHandler):
    __slots__ = ('__ctx', 'domains')

    PORT = 443

    def wrap(self, socket):
        self.__ctx = ssl._create_unverified_context(cert_reqs=ssl.CERT_REQUIRED)
        return self.__ctx.wrap_socket(
            socket,
            server_hostname=self.ip,
        )

    def post_connect(self):
        try:
            ssl_info = self.socket.getpeercert()
            self.domains = [v for _, v in ssl_info.get('subjectAltName', [])]
        except: # not connected
            self.domains = []

    def handle(self):
        results = set()
        for d in self.domains:
            if d.startswith('*'):
                continue # skip wildcards for now
            results.add(d + ': ' + self.handle_host(d))
        results.add(super().handle())
        return results
