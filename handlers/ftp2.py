from ftplib import FTP
from handlers import Base

class Handler(Base):
    PORT = 21
    __slots__ = ('ftp')

    def handle(self):
        pass

    def traverse_files(self, depth, path):
        if depth < 0:
            return

        if not path:
            path = ''

        for fname in self.ftp.nlst():
            if fname in ('.', '..'):
                continue
            cpath = f'{path}/{fname}'
            possibly_file = '.' in fname and len(fname.rsplit('.', 1)[-1]) < 6
            if not possibly_file:
                try:
                    self.ftp.cwd(fname)
                    self.traverse_files(depth - 1, cpath)
                    self.ftp.cwd('..')
                    continue
                except:
                    pass

            with self._print_lock:
                print(f'{self.ip} {cpath}')

    def post_disconnect(self):
        try:
            self.ftp = FTP()
            self.ftp.connect(self.ip, self.PORT, 5)
            if self.ftp.login().startswith('230'):
                self.traverse_files(3, '')
        except Exception as e:
            # with self._print_lock:
            #     print(f'{self.ip} {e!r}')
            pass
        finally:
            self.ftp.close()


