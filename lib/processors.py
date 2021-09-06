from threading import Event, Lock, Thread
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

    def add_handler(self, handler, output_path, iface, timeout, debug, args):
        handler.set_print_lock(self.__print_lock)

        handler.set_output_path(output_path)
        handler.set_iface(iface)
        handler.set_timeout(timeout)
        handler.set_args(args)
        handler.set_debug(debug)

        self.__handlers.append(handler)
        print('+', repr(handler), f':{handler.PORT}')

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


        threads = self.__threads
        self.__gen = iter(it)

        for _ in range(workers):
            t = Thread(target=self.__process, daemon=True)
            threads.append(t)

        print('Working...', end='\n\n')

        for t in threads:
            t.start()

        try:
            while any(map(lambda t: t.is_alive(), threads)):
                sleep(0.25)
        except:
            pass

        self.run_event.clear()
        print('Stopping threads...')

        try:
            for t in threads:
                t.join()
            print('Stopped')
        except KeyboardInterrupt:
            print('Killed')
