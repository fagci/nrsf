def process_each(fn, it, workers=16, *args):
    running = True

    def fn2(gen, gl, pl, running, *args):
        while running:
            try:
                with gl:
                    item = next(gen)
            except StopIteration:
                break
            try:
                fn(item, pl, *args)
            except StopIteration:
                running = False
                return
            except:
                running = False
                raise

    process(fn2, iter(it), workers, running, *args)


def process(fn, it, workers=16, *args):
    from threading import Lock, Thread
    from time import sleep

    threads = []
    gen_lock = Lock()
    print_lock = Lock()

    for _ in range(workers):
        t = Thread(target=fn, daemon=True, args=(
            it, gen_lock, print_lock, *args))
        threads.append(t)

    for t in threads:
        t.start()

    while any(map(lambda t: t.is_alive(), threads)):
        sleep(0.5)
