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

    def add_handler(self, handler):
        handler.set_print_lock(self.__print_lock)
        self.__handlers.append(handler)
        print('+', handler.get_name(), f'({handler.PORT} port)')

    def __process(self):
        while True:
            try:
                with self.__gen_lock:
                    ip = str(next(self.__gen))
                for handler_class in self.__handlers:
                    with handler_class(ip) as handler:
                        handler.handle()
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
