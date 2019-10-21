# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       24.py
   Description :
   Author :          cugxy
   date：            2019/10/11
-------------------------------------------------
   Change Activity:
                     2019/10/11
-------------------------------------------------

以 @classmethod 形式的多态去通用地构建对象

- 在 python 中, 每个类只能有一个构造器, 也就是 __init__ 方法
- 通过 @classmethod 机制, 可以用一种与构造器相仿的方式来构造类的对象
- 通过类方法多态机制, 我们能够以更加通用的方式来构建并拼接具体的子类

"""
import os
from threading import Thread


class InputData(object):
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generate_inputs(data_dir):
    for e in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, e))


def create_worker(input_list):
    workers = []
    for e in input_list:
        workers.append(LineCountWorker(e))
    return workers


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    f, r = workers[0], workers[1:]
    for w in r:
        f.reduce(w)
    return f.result


def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_worker(inputs)
    return execute(workers)


# 使用 @classmethod 重构上述代码


class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData2(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for e in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, e))


class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_worker(cls, input_class, config):
        workers = []
        for e in input_class.generate_inputs(config):
            workers.append(cls(e))
        return workers


class LineCountWorker2(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def mapreduce2(worker_class, input_class, config):
    workers = worker_class.create_worker(input_class, config)
    return execute(workers)


if __name__ == '__main__':
    data_dir = r'X:\liearth_test\data\logs'
    if 1:
        r = mapreduce(data_dir)
        print(r)
    if 1:
        config = {'data_dir': data_dir}
        r = mapreduce2(LineCountWorker2, PathInputData2, config)
        print(r)
