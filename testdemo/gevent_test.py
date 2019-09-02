"""
线程和进程的操作是由程序触发系统接口，最后的执行者是系统，它本质上是操作系统提供的功能。而协程的操作则是程序员指定的，在python中通过yield，人为的实现并发处理。

协程存在的意义：对于多线程应用，CPU通过切片的方式来切换线程间的执行，线程切换时需要耗时。协程，则只使用一个线程，分解一个线程成为多个“微线程”，在一个线程中规定某个代码块的执行顺序。

协程的适用场景：当程序中存在大量不需要CPU的操作时（IO）。
常用第三方模块gevent和greenlet。（本质上，gevent是对greenlet的高级封装，因此一般用它就行，这是一个相当高效的模块。）
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait

import gevent
from gevent import monkey;
monkey.patch_all()

import requests

urls = [
    'https://www.python.org/',
    'https://www.yahoo.com/',
    'https://github.com/',
]


def f(url):
    time.sleep(2)
    # threading.Thread(target=ff).start()
    print('GET: %s' % url)


def ff():
    time.sleep(2)
    print('22222222222222')


while True:
    # executor = ThreadPoolExecutor(max_workers=2)
    # all_tasks = []
    # for u in urls:
    #     all_tasks.append(executor.submit(f, u))
    # wait(all_tasks)
    gevent.joinall([gevent.spawn(f, u) for u in urls])
    print('end')
    time.sleep(60*10)

# grequests 模块相当于是封装了gevent的requests模块
# grequests.map((grequests.get(u) for u in urls))
