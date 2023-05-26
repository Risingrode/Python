import asyncio
import time


async def request(url):
    print('正在下载：', url)
    # 在异步协程中如果出现同步模块相关的代码，那么就无法实现异步
    # time.sleep(2)
    #当asyncio中遇到阻塞操作必须进行手动挂起
    await asyncio.sleep(2)
    print('下载完毕！')

start = time.time()
urls = [
    'www.baidu.com',
    'www.sougou.com',
    'www.goubanjia.com',
]
# 任务列表：存放多个对象
stacks = []
for url in urls:
    c= request(url)
    task = asyncio.ensure_future(c)
    stacks.append(task)
loop = asyncio.get_event_loop()
# 需要将任务列表封装到wait中
loop.run_until_complete(asyncio.wait(stacks))
print(time.time() - start)
