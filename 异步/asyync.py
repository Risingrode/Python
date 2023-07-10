import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(3)
    print("World")
    await asyncio.sleep(3)
    print("小可爱")

async def main():
    await asyncio.gather(hello(), hello(), hello())

# 启动事件循环
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
