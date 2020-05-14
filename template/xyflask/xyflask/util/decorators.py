#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:greenvalley
@file: decorators.py
@time: 2019/1/8
"""
import sys
import traceback
from functools import wraps

from xyflask.util.jsonify_util import return_msg


def try_exception(f):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_tbtext = traceback.format_tb(exc_traceback.tb_next)
            error = '\n[Exception]:{0}-{1}'.format(formatted_tbtext, exc_instance)
            return return_msg(-1, msg='exception', log=error)
    return wrapper
