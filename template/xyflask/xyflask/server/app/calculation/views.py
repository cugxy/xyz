# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       views
   Description :
   Author :          cugxy
   date：            2019/5/30
-------------------------------------------------
   Change Activity:
                     2019/5/30
-------------------------------------------------

将 数据库查询放入视图函数
- 通过杆塔编号查询档段相交的点云文件列表
- 通过干他编号查询档段包围盒

将 获取点云, 以及点云计算放入 celery tasks

"""
from flask import request, url_for


from xyflask.server.app.calculation import cal
from xyflask.server.app.calculation.tasks import test_celery_add, result, cancel
from xyflask.util.decorators import try_exception
from xyflask.util.jsonify_util import return_msg


@cal.route('/test', methods=['GET'])
@try_exception
def test():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    task = test_celery_add.apply_async(args=[a, b, ])
    return return_msg(1, 'ok', data={'Location': url_for('cal.test_result', task_id=task.id),
                                     'celery_task_id': task.id, })


@cal.route('/test_result/<task_id>', methods=['GET'])
@try_exception
def test_result(task_id):
    state, msg, data = result(test_celery_add, task_id)
    return return_msg(state, msg, data)


@cal.route('/test/cancel', methods=['POST'])
@try_exception
def cancel_test():
    celery_task_id = request.form.get('celery_task_id', None, type=str)
    if not celery_task_id:
        return return_msg(0, 'param error', log='error celery_task_id: %s' % (celery_task_id, ))
    state, _, __ = result(test_celery_add, celery_task_id)
    if state != 0:
        return return_msg(0, 'can not cancel')
    cancel(celery_task_id)
    return return_msg(1, 'ok')
