# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       tasks.py
   Description :     celery 任务
   Author :          cugxy
   date：            2019/5/31
-------------------------------------------------
   Change Activity:
                     2019/5/31
-------------------------------------------------
"""


"""
1. If your task does I/O then make sure you add timeouts to these operations
2. When using multiple decorators in combination with the task decorator you must make sure that the task decorator is 
    applied last (oddly, in Python this means it must be first in the list)
3. use log:
    from celery.utils.log import get_task_logger
    
    logger = get_task_logger(__name__)
4. ignore result
    The option precedence order is the following:
        Global task_ignore_result
        ignore_result option
        Task execution option ignore_result

"""


from xyflask.server.app import celery


def result(task_val, task_id):
    task = task_val.AsyncResult(task_id)
    if task.state == 'FAILURE':
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
        return -1, 'error', response
    if task.state == 'PENDING':
        response = {
            'state': task.state,
        }
        return 0, 'pending', response
    if task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.info,
        }
        return 1, 'ok', response
    if task.state == 'STARTED':
        response = {
            'state': task.state,
            'result': str(task.info),
        }
        return 2, 'ok', response
    if task.state == 'REVOKED':
        response = {
            'state': task.state,
            'result': str(task.info),
        }
        return 3, 'revoked', response
    response = {
        'state': task.state,
        'status': str(task.info),  # this is the exception raised
    }
    return -1, 'error', response


def cancel(task_id):
    celery.control.revoke(task_id)
    return 1


@celery.task(track_started=True)
def test_celery_add(a, b):
    return a + b
