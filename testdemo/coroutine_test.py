"""
Python中的协程大概经历了如下三个阶段： 
1. 最初的生成器变形yield/send 
2. 引入@asyncio.coroutine和yield from 
3. 在最近的Python3.5版本中引入async/await关键字
async定义协程（暂停执行），await挂起等待耗时io阻塞
"""
import asyncio
import time

import aiohttp


async def coroutine(url):
    print("request:", url)
    # await 后面就是调用耗时的操作
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


now = lambda: time.time()
start = now()

# 将协程封装成task后可以添加回调方法，以处理协程返回值（可以直接协程列表传给asyncio.wait）
tasks = [asyncio.ensure_future(coroutine('http://0.0.0.0:8099/')) for _ in range(100)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

print("Time:", now() - start)

for task in tasks:
    print('Task ret: ', task.result())
