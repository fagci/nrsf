from ftplib import FTP, FTP_TLS, error_perm, error_proto, error_reply, error_temp
from time import sleep

from handlers import Base

INTERESTING_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
PATH_BLACKLIST = ('.', '..', 'bin')


class Handler(Base):
    PORT = 21

    def handle(self):
        if self.DEBUG:
            with self._print_lock:
                print(self.read())

    def post_disconnect(self):
        self.files = set()
        Connector: type[FTP] = FTP
        retries = 5

        while retries > 0:
            try:
                with Connector(self.ip, timeout=30) as ftp:
                    ftp.login()
                    try:
                        ftp.sendcmd('OPTS UTF8 ON')
                        ftp.encoding = 'utf-8'
                    except:
                        pass
                    self._get_files(ftp)
            except (error_perm, error_proto) as e:
                if Connector is FTP:
                    Connector = FTP_TLS
                else:
                    break
            except (error_reply, error_temp) as e:
                try:
                    code = int(str(e)[:3])
                except:
                    break
                if code in {331, 332}:
                    break  # anon login only
                if code == 421:
                    break
                if code == 450:
                    # print('-', self.ip, e)
                    break
                if code == 431:
                    if Connector is not FTP:
                        break
                    Connector = FTP_TLS
                    continue
                # print(repr(e))
                break
            except OSError as e:
                pass
            except KeyboardInterrupt:
                raise
            except Exception:
                break
            retries -= 1
            sleep(1)

        if self.files:
            self.print(' '.join(self.files))

    def _traverse(self, ftp: FTP, depth=0, files=None):
        if files is None:
            files = []

        if depth > 10:
            return

        paths = [p for p in ftp.nlst() if p not in PATH_BLACKLIST]

        for path in paths:
            files.append(path)
            if len(files) > 100:
                return

            try:
                if path.lower().endswith(INTERESTING_EXTENSIONS):
                    self.files.add(path)
                    return path

                # skip files by extension delimiter
                if '.' in path:
                    # print('-', path)
                    continue

                ftp.cwd(path)
                found = self._traverse(ftp, depth + 1, files)
                ftp.cwd('..')

                if found:
                    return

            except error_perm:
                pass

    def _get_files(self, ftp: FTP):
        lst = [p for p in ftp.nlst() if p not in ('.', '..')]

        if not lst:
            return

        return self._traverse(ftp)
