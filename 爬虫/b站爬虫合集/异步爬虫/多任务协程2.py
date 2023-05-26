import requests
import asyncio
import time

start = time.time()
urls = [
    'http://127.0.0.1:5000/a',
    'http://127.0.0.1:5000/b',
    'http://127.0.0.1:5000/c',
    'http://127.0.0.1:5000/d'
]


async def get_page(url):
    print('正在下载', url)
    #   get请求是同步
    # aiohttp:基于异步网络请求的模块
    reponse = await requests.get(url=url)
    print('下载完成', reponse.text)


tasks = []

for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print('总耗时：', time.time() - start)
