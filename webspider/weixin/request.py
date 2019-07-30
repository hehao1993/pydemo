from requests import Request
from webspider.weixin.config import TIMEOUT


class WeixinRequest(Request):
    def __init__(self, url, callback, method='GET', header=None, need_proxy=False, fail_time=0,timeout=TIMEOUT):
        Request.__init__(self, url, method, header)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout
