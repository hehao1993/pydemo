import time
from multiprocessing import Process
from webspider.proxypool.api import app
from webspider.proxypool.getter import Getter
from webspider.proxypool.setting import TESTER_CYCLE, GETTER_CYCLE, API_HOST, API_PORT, TESTER_ENABLED, GETTER_ENABLED, \
    API_ENABLED
from webspider.proxypool.tester import Tester


class Scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle:
        :return:
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle:
        :return:
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        :return:
        """
        print('开启代理获取接口')
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester())
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter())
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api())
            api_process.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
