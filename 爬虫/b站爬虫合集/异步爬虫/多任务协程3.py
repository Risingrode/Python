import requests
import asyncio
import time
import aiohttp
start = time.time()
urls = [
    'http://127.0.0.1:5000/a',
    'http://127.0.0.1:5000/b',
    'http://127.0.0.1:5000/c',
    'http://127.0.0.1:5000/d'
]


async def get_page(url):
  async with aiohttp.ClientSession() as session:
      # 这里也可以发post请求
      # params/data,proxy='http://...'
      async with await session.get(url=url) as response:
          #text()返回字符串  read()返回二进制响应数据 json()返回的是json对象
          #注意：响应数据操作之前一定要使用await进行手动挂起
          page_text=await response.text()
          print(page_text)


tasks = []

for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print('总耗时：', time.time() - start)
