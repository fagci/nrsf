from handlers import Base
from html.parser import HTMLParser

class Handler(Base):
    PORT = 80
    def handle(self):
        html = self.dialog(f'GET / HTTP/1.1\r\nHost: {self.ip}\r\n\r\n'.encode(), 4096)
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

