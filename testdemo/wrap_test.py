from functools import wraps
from threading import Thread


def async_thread(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def wrap_func_out(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def retry(times=3):
    def wrap_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                print(f"wait elements, retry {i+1} times")
                return func(*args, **kwargs)
        return wrapper
    return wrap_func


@wrap_func_out
def say(something):
    print(f'say {something}')


say(123)
