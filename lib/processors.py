from threading import Lock, Thread
from time import sleep

class Processor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.threads = []
        self.print_lock = Lock()
        self.gen_lock = Lock()

        for h in handlers:
            h.set_print_lock(self.print_lock)

    def __process(self):
        running = True
        while running:
            try:
                with self.gen_lock:
                    ip = str(next(self.gen))
                for handler_class in self.handlers:
                    with handler_class(ip) as handler:
                        handler.handle()
            except StopIteration:
                running = False
                return
            except:
                running = False
                raise

    def process(self, it, workers):
        threads = self.threads
        add_thread = threads.append
        self.gen = iter(it)

        for _ in range(workers):
            t = Thread(target=self.__process, daemon=True)
            add_thread(t)

        for t in threads:
            t.start()

        try:
            while any(map(lambda t: t.is_alive(), self.threads)):
                sleep(0.5)
        except KeyboardInterrupt:
            print('Interrupted')

