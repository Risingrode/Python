import asyncio

async def request(url):
    print('正在请求的url是:',url)
    print('请求成功：',url)
    return url  #该行仅限于绑定回调
c=request('www.baidu.com')

# #创建一个事件循环对象
# loop=asyncio.get_event_loop()
# #把协程对象注册到loop中,然后启动loop
# loop.run_until_complete(c)

#task的使用
# loop=asyncio.get_event_loop()
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# #基于loop创建的task任务对象
# task=loop.create_task(c)
# print(task)
#
# loop.run_until_complete(task)
# print(task)

#future的使用
#loop=asyncio.get_event_loop()
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
#
# task=asyncio.ensure_future(c)
# print(task)
# loop.run_until_complete(task)
# print(task)

# 绑定回调
def callback(task):
    # 其结果返回的是任务对象中封装的协程对象对应的返回值
    print(task.result())

#loop=asyncio.get_event_loop()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task=asyncio.ensure_future(c)
#把回调函数绑定到任务对象中
task.add_done_callback(callback)
loop.run_until_complete(task)












