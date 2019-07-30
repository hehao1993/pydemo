"""
线程和进程的操作是由程序触发系统接口，最后的执行者是系统，它本质上是操作系统提供的功能。而协程的操作则是程序员指定的，在python中通过yield，人为的实现并发处理。

协程存在的意义：对于多线程应用，CPU通过切片的方式来切换线程间的执行，线程切换时需要耗时。协程，则只使用一个线程，分解一个线程成为多个“微线程”，在一个线程中规定某个代码块的执行顺序。

协程的适用场景：当程序中存在大量不需要CPU的操作时（IO）。
常用第三方模块gevent和greenlet。（本质上，gevent是对greenlet的高级封装，因此一般用它就行，这是一个相当高效的模块。）
"""
import grequests as grequests
from gevent import monkey; monkey.patch_all()
import gevent
import requests

urls = [
    'https://www.python.org/',
    'https://www.yahoo.com/',
    'https://github.com/',
]


def f(url):
    print('GET: %s' % url)
    resp = requests.get(url)
    print('%d bytes received from %s.' % (len(resp.text), url))


gevent.joinall([gevent.spawn(f, u) for u in urls])

# grequests 模块相当于是封装了gevent的requests模块
# grequests.map((grequests.get(u) for u in urls))
