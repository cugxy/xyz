#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy 
@file: 38.py.py 
@time: 2019/11/16

在线程中使用 Lock 来防止数据竞争

- Python 确实有全局解释锁, 但是在编写自己的程序时, 依然要设法防止多个线程争用同一份数据
- 如果在不加锁的前提下, 允许多条线程修改同一个对象, 那么程序的数据结果可能会遭到破坏
- 在 Python 内置的 threading 模块中, 有个叫 Lock 的类, 他用标准的方式实现了互斥锁

"""
from threading import Thread, Lock


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


def worker(sensor_idx, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for i in threads:
        i.join()


if __name__ == '__main__':
    if 1:
        how_many = 10 ** 5
        counter = Counter()
        run_threads(worker, how_many, counter)
        print('Counter should be %d, found %d' % (5 * how_many, counter.count))
    if 1:
        how_many = 10 ** 5
        counter = LockingCounter()
        run_threads(worker, how_many, counter)
        print('Counter should be %d, found %d' % (5 * how_many, counter.count))
    pass

