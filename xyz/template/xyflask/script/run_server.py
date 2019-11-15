# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       run_server.py
   Description :
   Author :          cugxy
   date：            2019/11/15
-------------------------------------------------
   Change Activity:
                     2019/11/15
-------------------------------------------------
"""
import os
from flask_script import Manager

from xyflask import create_app, create_celery


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
celery = create_celery(app)


if __name__ == '__main__':
    manager = Manager(app)
    manager.run()

# celery worker -A run_server.celery -l info --logfile=w1.log -P eventlet
