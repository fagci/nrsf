from threading import Lock, Thread
from time import sleep

class ProcessorThread(Thread):
    def __init__(self, fn, gen, gl, pl, *args):
        super().__init__(target=fn, daemon=True)
        self.gen = iter(gen)
        self.gl = gl
        self.pl = pl
        self.args = args

    def run(self):
        running = True
        while running:
            try:
                with self.gl:
                    item = next(self.gen)
            except StopIteration:
                break
            try:
                self._target(item, self.pl, *self.args)
            except StopIteration:
                running = False
                return
            except:
                running = False
                raise

class Processor:
    def __init__(self):
        self.threads = []
        self.gen_lock = Lock()
        self.print_lock = Lock()

    def process_each(self, fn, it, workers=16, *args):
        for _ in range(workers):
            t = ProcessorThread(fn, it, self.gen_lock, self.print_lock, *args)
            self.threads.append(t)

        for t in self.threads:
            t.start()

        try:
            while any(map(lambda t: t.is_alive(), self.threads)):
                sleep(0.5)
        except KeyboardInterrupt:
            print('Interrupted')
