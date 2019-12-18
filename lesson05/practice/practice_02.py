from urllib import request
from threading import Thread
from os import path, mkdir
from time import time


def thread_decorator(name, daemon):
    def actual_decorator(func):
        def wrapper(*args):
            t = Thread(target=func, args=(*args, ), name=name, daemon=daemon)
            print(f'Thread {name} started on {args[0]}')
            start_time = time()
            t.start()
            print(f'Thread {name} ended in {round(time() - start_time, 5)}')
        return wrapper
    return actual_decorator


@thread_decorator('web_file_retrieving_thread', False)
def get_web_file(url, i):
    if not path.exists('files'):
        mkdir('files')
    request.urlretrieve(url,  path.join("files", path.basename(url)))

urls = ['http://meme.vandorp.biz/fap.jpg',
        'http://meme.vandorp.biz/DoubleFacePalm.jpg',
        'http://meme.vandorp.biz/?#grin.jpg',
        'http://meme.vandorp.biz/?#americans.jpg',
        'http://meme.vandorp.biz/?#anoyingfacebook.jpg',
        'http://meme.vandorp.biz/gtfo.jpg',
        'http://meme.vandorp.biz/?#rage.jpg',
        'http://meme.vandorp.biz/?#happy.jpg',
        'http://meme.vandorp.biz/?#areyoukiddingme.jpg',
        'http://meme.vandorp.biz/?#badass.jpg']


for i, url in enumerate(urls):
    get_web_file(url, i)






