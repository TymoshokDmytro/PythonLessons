from urllib import request
from threading import Thread
from os import path, mkdir
from time import time


def thread_decorator(name, daemon):
    def actual_decorator(func):
        def wrapper(*args):
            t = MyThread(target=func, args=(*args,), name=name, daemon=daemon)
            t.start()

        return wrapper

    return actual_decorator


class MyThread(Thread):
    _id = 0

    def __init__(self, target, args, daemon, name):
        self._args = args
        MyThread._id += 1
        self._thread_name = name + "_" + str(MyThread._id)
        super().__init__(target=target, args=args, daemon=daemon, name=name)

    def run(self):
        print(f'Thread {self._thread_name} started on {next(iter(self._args))}')
        start_time = time()
        super().run()
        print(f'Thread {self._thread_name} ended in {round(time() - start_time, 5)}')


@thread_decorator('web_file_retrieving_thread', False)
def get_web_file(url):
    if not path.exists('files'):
        mkdir('files')
    request.urlretrieve(url, path.join("files", path.basename(url)))


urls = ['http://meme.vandorp.biz/fap.jpg',
        'http://meme.vandorp.biz/DoubleFacePalm.jpg',
        'http://www.eso.org/~wfreudli/pressreleases/iron/images/high_resolution.jpg',
        'http://speedtest.tele2.net/10MB.zip',
        'http://meme.vandorp.biz/?#grin.jpg',
        'http://meme.vandorp.biz/?#americans.jpg',
        'http://meme.vandorp.biz/?#anoyingfacebook.jpg',
        'http://meme.vandorp.biz/gtfo.jpg',
        'http://meme.vandorp.biz/?#rage.jpg',
        'http://meme.vandorp.biz/?#happy.jpg',
        'http://meme.vandorp.biz/?#areyoukiddingme.jpg',
        'http://meme.vandorp.biz/?#badass.jpg']

for i, url in enumerate(urls):
    get_web_file(url)
