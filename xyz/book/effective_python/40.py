#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy 
@file: 40.py.py 
@time: 2019/11/16

线程的缺点:
- 为确保数据安全, 我们必须使用特殊的工具来协助这些线程. 这使得多线程的代码, 要比单线程的过程式代码更加难懂.
- 线程需要占用大量内存, 每个正在执行的线程, 大约占据 8MB 内存
- 线程启动时的开销较大.

考虑使用协程来并发的运行多个函数

"""
from collections import namedtuple


def xy_coroutine():
    while True:
        received = yield
        print('received:', received)


def minimize():
    cur = yield
    while True:
        val = yield cur
        cur = min(val, cur)


Query = namedtuple('Query', ('x', 'y'))
ALIVE = '*'
EMPTY = '-'


def count_neighbors(y, x):
    n_ = yield Query(y + 1, x + 0)
    ne = yield Query(y + 1, x + 1)
    e_ = yield Query(y + 0, x + 1)
    se = yield Query(y - 1, x + 1)
    s_ = yield Query(y - 1, x + 0)
    sw = yield Query(y - 1, x - 1)
    w_ = yield Query(y + 0, x - 1)
    nw = yield Query(y + 1, x - 1)
    nei = [n_, ne, e_, se, s_, sw, w_, nw, ]
    count = 0
    for s in nei:
        if s == ALIVE:
            count += 1
    return count


if __name__ == '__main__':
    if 0:
        it = xy_coroutine()
        next(it)
        it.send('First')
        it.send('Second')
        pass
    if 1:
        it = minimize()
        next(it)
        print(it.send(10))
        print(it.send(20))
        print(it.send(30))
        print(it.send(-10))
        print(it.send(120))
        print(it.send(-1210))
