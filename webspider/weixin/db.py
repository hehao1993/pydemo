from pickle import dumps, loads

from redis import StrictRedis

from webspider.weixin.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from webspider.weixin.request import WeixinRequest


class RedisQueue():
    def __init__(self):
        """
        初始化Redis
        """
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)

    def add(self, request):
        """
        向队列中添加序列化后的Request
        :param request: 请求对象
        :return: 添加结果
        """
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return: Request or None
        """
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0
