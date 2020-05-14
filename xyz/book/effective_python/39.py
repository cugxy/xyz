#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy 
@file: 39.py.py 
@time: 2019/11/16 
"""
from collections import deque
from threading import Lock, Thread
from time import sleep


class XYQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


def download(obj):
    pass


def resize(obj):
    pass


def upload(obj):
    pass


if __name__ == '__main__':
    if 1:
        download_queue = XYQueue()
        resize_queue = XYQueue()
        upload_queue = XYQueue()
        done_queue = XYQueue()
        threads = [
            Worker(download, download_queue, resize_queue),
            Worker(resize, resize_queue, upload_queue),
            Worker(upload, upload_queue, done_queue),
        ]
        for t in threads:
            t.start()
        for _ in range(1000):
            download_queue.put(object())
        while len(done_queue.items) < 1000:
            sleep(0.1)
            print(len(done_queue.items))


    pass

