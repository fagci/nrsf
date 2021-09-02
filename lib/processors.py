from threading import Lock, Thread
from time import sleep

class Processor:
    __slots__ = ('__handlers','__threads','__gen','__gen_lock','__print_lock')
    def __init__(self, handlers):
        self.__handlers = handlers
        self.__threads = []
        self.__print_lock = Lock()
        self.__gen_lock = Lock()

        for h in handlers:
            h.set_print_lock(self.__print_lock)

    def __process(self):
        running = True
        while running:
            try:
                with self.__gen_lock:
                    ip = str(next(self.__gen))
                for handler_class in self.__handlers:
                    with handler_class(ip) as handler:
                        handler.handle()
            except StopIteration:
                running = False
                return
            except:
                running = False
                raise

    def process(self, it, workers):
        threads = self.__threads
        add_thread = threads.append
        self.__gen = iter(it)

        for _ in range(workers):
            t = Thread(target=self.__process, daemon=True)
            add_thread(t)

        for t in threads:
            t.start()

        try:
            while any(map(lambda t: t.is_alive(), threads)):
                sleep(0.5)
        except KeyboardInterrupt:
            print('Interrupted')

