class Http:
    PORT = 80
    def process(self, pl, s, ip, port):
        s.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n'.encode())
        with pl:
            print(f'{ip}:{port}\n', s.recv(1024).decode(errors='ignore'))

