# -*- coding: utf-8 -*-
import os


class Config:
    """
    配置类
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xy_flask_server_template'
  
    CACHE_TYPE = 'redis'
    LOG_FILE_FILENAME = os.environ.get('LOG_FILE_FILENAME') or '/data/logs/vege.log'
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST') or '127.0.0.1'
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT') or 6379
    CACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB') or '1'
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD') or 'greenvalley'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 'redis://auth:password@redishost:6379/0'
    CELERY_BROKER_URL = 'redis://auth:%s@%s:%s/10' % (CACHE_REDIS_PASSWORD, CACHE_REDIS_HOST, CACHE_REDIS_PORT, )
    CELERY_RESULT_BACKEND = 'redis://auth:%s@%s:%s/11' % (CACHE_REDIS_PASSWORD, CACHE_REDIS_HOST, CACHE_REDIS_PORT, )
    CELERY_DISABLE_RATE_LIMITS = True

    JSON_SORT_KEYS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'postgresql://greenvalley:greenvalley_postgis@127.0.0.1:54321/xyflask'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URL') or \
                              'postgresql://greenvalley:greenvalley_postgis@127.0.0.1:54321/xyflask'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
