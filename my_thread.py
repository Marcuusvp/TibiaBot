import threading

class MyThread():
    def __init__(self, work):
        self.event = threading.Event()
        self.thread = threading.Thread()
        self.work = work

    def stop(self):
        self.event.set()
        self.thread.join()

    def run(self):
        while not self.event.is_set():
            self.work()