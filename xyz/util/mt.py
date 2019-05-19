#!coding=utf-8

import logging
import inspect
import functools
import multiprocessing


def _worker(input, output):
    for evt in iter(input.get, 'STOP'):
        cb = evt.get('handler', None)
        if not cb:  continue

        args = evt.get('args', [])
        kwds = evt.get('kwds', {})

        _args = set(inspect.getargspec(cb).args)
        if '_output' in _args:
            kwds['_output'] = output

        if '_input' in _args:
            kwds['_input'] = input

        rs = cb(*args, **kwds)
        if rs is None:  continue

        output.put(rs)


def mt_run(cb, workers=None):
    jobs, workers = [], workers or max(1, multiprocessing.cpu_count() - 1)

    # Create queues
    task_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()

    for _ in range(workers):
        j = multiprocessing.Process(target=_worker, args=(task_queue, done_queue,))
        jobs.append(j)
        j.start()

    cb(done_queue, task_queue)
    [e.join() for e in jobs]


def default_num():
    return max(1, multiprocessing.cpu_count() - 1)


# -- utils functions for h5f file ------------------------------
def _dump(input, output, limit):
    total = limit
    while limit > 0:
        flag, e = input.get()
        logging.debug('%s' % e)
        if not flag:    continue
        limit -= 1

    for _ in range(total):
        output.put('STOP')


def mt_process(cb, cbkwds={}, workers=None):
    workers = workers or default_num()  # workers:  cpu

    def _cb(input, output, workers=None):
        for tid in range(workers):
            _kwds = {'_tid': tid, }
            _kwds.update(cbkwds)

            output.put({
                'handler': cb,
                'args': (workers,),
                'kwds': _kwds,
            })
        _dump(input, output, workers)

    mt_run(functools.partial(_cb, workers=workers), workers=workers)
