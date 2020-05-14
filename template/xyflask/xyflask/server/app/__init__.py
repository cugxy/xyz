#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:cugxy
@file: __init__.py.py
@time: 2018/04/18
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from flask_cache import Cache
from flask_celery import Celery

from xyflask.server.config import config
from xyflask.database import models

db = models.db
sdb = SQLAlchemy()  # 数据库db

login_manager = models.login_manager
celery = Celery()
cache = Cache()


def create_app(config_name):
    """
    创建服务实例
    :param config_name:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.before_first_request
    def create_tables():
        cache.clear()
        if app.config['DEBUG']:
            return
        db.create_all()

    gzip = Gzip(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    celery.init_app(app)
    celery.broker = app.config['CELERY_BROKER_URL']
    celery.conf.update(app.config)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    from .calculation import cal as cal_blueprint
    app.register_blueprint(cal_blueprint, url_prefix='/api/cal')

    logfile = app.config['LOG_FILE_FILENAME']
    _dir = os.path.dirname(logfile)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    handler = RotatingFileHandler(logfile, maxBytes=10000, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    return app


def create_celery(app):
    from celery import Celery
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    celery.conf.update(app.config)
    Taskbase = celery.Task

    class ContextTask(Taskbase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():                                             # task can user app
                return Taskbase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

