# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       mt_logger.py
   Description :
   Author :          cugxy
   date：            2019/12/10
-------------------------------------------------
   Change Activity:
                     2019/12/10
-------------------------------------------------
"""

import logging
import logging.handlers
import multiprocessing
import threading


class SingleQueueHandler(logging.handlers.QueueHandler):
    """
    queue handler 单例
    """
    _instance_lock = threading.Lock()

    def __init__(self, queue):
        super().__init__(queue)

    def __new__(cls, *args):
        if not hasattr(SingleQueueHandler, "_instance"):
            with SingleQueueHandler._instance_lock:
                if not hasattr(SingleQueueHandler, "_instance"):
                    SingleQueueHandler._instance = object.__new__(cls)
        return SingleQueueHandler._instance


def get_queue_logger(logger_queue):
    """
    用于多进程中打印日志, 在多进程运行函数中调用, 传入 Queue
    :param logger_queue: 日志队列
    :return:    logger 对象
    """
    qh = SingleQueueHandler(logger_queue)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(qh)
    return logger


def logger_thread(logger_queue, logger):
    """
    打印日志进程, 当队列中放入 None 时, 该函数退出
    :param logger_queue:    日志队列
    :param logger:          日志对象
    :return:
    """
    if not logger:
        return
    logger.info('logger thread start')
    while True:
        record = logger_queue.get()
        if record is None:
            logger.info('logger thread end')
            break
        logger.handle(record)


def worker(p_a, logger_queue):
    """
    工作函数
    :param p_a:
    :param logger_queue:
    :return:
    """
    logger = None
    if logger_queue is not None:
        logger = get_queue_logger(logger_queue)
        logger.info('worker start')
    try:
        raise ValueError('Something error')
    except ValueError as e:
        if logger:
            logger.exception(e)
    if logger:
        logger.info('worker end')
    return p_a


def mt_process(in_logger):
    """
    多进程处理
    :param in_logger:
    :return:
    """
    if in_logger:
        in_logger.info('mt_process start')
    p_count = 2
    logger_queue = multiprocessing.Manager().Queue()
    logger_process = threading.Thread(target=logger_thread, args=(logger_queue, in_logger))
    logger_process.start()
    p_count = max(1, p_count)
    p_count = min(multiprocessing.cpu_count() - 1, p_count)
    t_pool = multiprocessing.Pool(processes=p_count)
    pool_return_rs = []
    for i in range(10):
        pool_return_rs.append(t_pool.apply_async(worker, (i, logger_queue)))
    t_pool.close()
    t_pool.join()
    logger_queue.put(None)
    logger_process.join()
    pool_return_rs = [e.get(1e6) for e in pool_return_rs]
    if in_logger:
        in_logger.info('mt_process end')
    return pool_return_rs


def create_console_logger():
    """
    创建控制台日志
    :return:
    """
    logger = logging.getLogger('xyz')
    logger.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s-%(module)s-%(filename)s-%(lineno)d-%(funcName)s-%(levelname)s-'
                                       '%(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)
    return logger


if __name__ == '__main__':
    t_logger = create_console_logger()
    mt_process(t_logger)
