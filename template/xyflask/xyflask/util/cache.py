# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       cache.py
   Description :     
   Author :          cugxy 
   date：            2020/03/24 
-------------------------------------------------
   Change Activity:
                     2020/03/24 
-------------------------------------------------
"""
import functools
import gzip
import hashlib
from io import BytesIO

from flask import request, session, current_app
from flask_login import current_user

from xyflask.server.app import cache


def redis_cache(timeout=10 * 60, key='', namespace='', with_session_id=True):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if current_app.config['DEBUG']:
                return f(*args, **kwargs)
            cache_key = '%s%s' % (key, request.full_path, )
            if with_session_id:
                session_id = session.get('_id', '')
                cache_key = '%s%s' % (cache_key, session_id, )
            md = hashlib.md5()
            md.update(cache_key.encode('utf-8'))
            cache_key = md.hexdigest()
            cache_key = '%s%s' % (namespace, cache_key, )
            value = None
            try:
                value = cache.get(cache_key)
            except Exception as e:
                current_app.logger.exception(e)
                return f(*args, **kwargs)
            if value is None:
                value = f(*args, **kwargs)
                value = gzip_rep(value)
                try:
                    cache.set(cache_key, value, timeout=timeout)
                except Exception as e:
                    pass
            return value
        return decorated_function
    return decorator


def clear_cache(namespace=''):
    if not namespace:
        return False
    keys = cache.cache._client.keys()
    d_keys = [e.decode().replace(cache.cache.key_prefix, '') for e in keys if e.decode().find(namespace) != -1]
    cache.delete_many(*d_keys)
    return True


def gzip_rep(response):
    accept_encoding = request.headers.get('Accept-Encoding', '')
    minimum_size = 500
    compress_level = 6
    if response.status_code < 200 or \
            response.status_code >= 300 or \
            response.direct_passthrough or \
            len(response.get_data()) < minimum_size or \
            'gzip' not in accept_encoding.lower() or \
            'Content-Encoding' in response.headers:
        return response

    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=compress_level, fileobj=gzip_buffer)
    gzip_file.write(response.get_data())
    gzip_file.close()
    response.set_data(gzip_buffer.getvalue())
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = len(response.get_data())

    return response
