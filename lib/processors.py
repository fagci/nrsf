from handlers import Base
from threading import Lock, Thread
from time import sleep


class Processor:
    __slots__ = ('__handlers', '__threads', '__gen', '__gen_lock',
                 '__print_lock')

    def __init__(self):
        self.__handlers = []
        self.__threads = []
        self.__gen_lock = Lock()
        self.__print_lock = Lock()

    def add_handler(self, handler:Base, output_path, iface, timeout, debug):
        handler.set_print_lock(self.__print_lock)

        handler.set_output_path(output_path)
        handler.set_iface(iface)
        handler.set_timeout(timeout)

        if debug:
            handler.DEBUG = True

        self.__handlers.append(handler)
        print('+', repr(handler), f'({handler.PORT} port)')

    def __process(self):
        while True:
            try:
                with self.__gen_lock:
                    ip = next(self.__gen)
                for handler_class in self.__handlers:
                    with handler_class(ip) as handler:
                        handler()
            except StopIteration:
                return
            except:
                raise

    def process(self, it, workers):
        if not self.__handlers:
            print('No handlers loaded.')
            return

        print('Working...', end='\n\n')

        threads = self.__threads
        self.__gen = iter(it)

        for _ in range(workers):
            t = Thread(target=self.__process, daemon=True)
            threads.append(t)

        for t in threads:
            t.start()

        try:
            while any(map(lambda t: t.is_alive(), threads)):
                sleep(0.25)
        except KeyboardInterrupt:
            print('Interrupted')
