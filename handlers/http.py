from handlers import Base
from html.parser import HTMLParser

class Http(Base):
    PORT = 80
    def process(self, s):
        ip, _ = s.getpeername()
        s.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n'.encode())
        html = s.recv(1024).decode(errors='ignore')
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

