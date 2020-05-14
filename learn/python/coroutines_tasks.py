# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       coroutines_tasks.py
   Description :
   Author :          cugxy
   date：            2019/11/1
-------------------------------------------------
   Change Activity:
                     2019/11/1
-------------------------------------------------

https://docs.python.org/zh-cn/3.8/library/asyncio-task.html
https://www.jianshu.com/p/b5e347b3a17c

使用 async 关键字定义一个协程, 简单的调用一个协程并不会将其加入执行日程, 要真正运行一个协程, asyncio 提供了如下三种主要机制:

- asyncio.run() 用来运行最高层级的入口点 "main()" 函数
- asyncio.create_task() 用来并发运行作为 asyncio 任务的国歌协程

"""

import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"Started at {time.strftime('%X')}")
    await say_after(1, 'Hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")


async def main2():
    task1 = asyncio.create_task(say_after(1, 'Hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    print(f"Started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


if __name__ == '__main__':
    if 1:
        asyncio.run(main2())
    pass

