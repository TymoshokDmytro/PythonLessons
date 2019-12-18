from threading import Thread


class MyThread(Thread):

    def __init__(self, arg, daemon, name):
        self._arg = arg
        super().__init__(daemon=daemon, name=name)

    def run(self):
        print("Working in a thread " + self.name)


for i in range(20):
    MyThread(1, False, f'name-{i}').start()

