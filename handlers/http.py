from handlers import Base
from html.parser import HTMLParser

class Handler(Base):
    PORT = 80
    def handle(self):
        return self.handle_host(self.ip)

    def handle_host(self, hostname):
        html = self.dialog((
            'GET / HTTP/1.1\r\n'
            f'Host: {hostname}\r\n'
            'User-Agent: Mozilla/5.0\r\n'
            'Accept: text/html\r\n'
            '\r\n'
        ).encode(), 4096)
        if self.DEBUG:
            with self._print_lock:
                print(html)
        title_parser = TitleParser()
        title_parser.feed(html)
        return title_parser.title.replace('\n', ' ').replace('\r', '')

class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title = ''

    def handle_starttag(self, tag, _):
        self.match = tag == 'title'

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False

