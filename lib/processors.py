from handlers import Base
from threading import Lock, Thread, Event
from time import sleep


class Processor:
    __slots__ = ('__handlers', '__threads', '__gen', '__gen_lock',
                 '__print_lock', 'run_event', 'args')

    def __init__(self):
        self.__handlers = []
        self.__threads = []
        self.__gen_lock = Lock()
        self.__print_lock = Lock()
        self.run_event = Event()

    def add_handler(self, handler:Base, output_path, iface, timeout, debug, args):
        handler.set_print_lock(self.__print_lock)

        handler.set_output_path(output_path)
        handler.set_iface(iface)
        handler.set_timeout(timeout)
        handler.set_args(args)

        if debug:
            handler.DEBUG = True

        self.__handlers.append(handler)
        print('+', repr(handler), f'({handler.PORT} port)')

    def __process(self):
        while self.run_event.is_set():
            with self.__gen_lock:
                ip = next(self.__gen, None)
            if not ip:
                break
            for handler_class in self.__handlers:
                with handler_class(ip) as handler:
                    handler()

    def process(self, it, workers):
        if not self.__handlers:
            print('No handlers loaded.')
            return

        self.run_event.set()

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
        except:
            pass

        print('Stopping threads...')
        self.run_event.clear()
        try:
            for t in threads:
                t.join()
            print('Stopped')
        except KeyboardInterrupt:
            print('Killed')
