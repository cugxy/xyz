#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: jsonify_util
@time: 2018/10/30
"""

from flask import jsonify, current_app


def return_msg(status, msg, data=None, log=None):
    """
    统一服务返回
    :param status:  状态 ERROR_CODE
    :param msg:     返回消息
    :param data:    服务成功时，返回数据
    :param log:     服务异常时，打印日志
    :return: dict
    """
    result = {
        "status": status,
        "msg": msg,
    }
    if data is not None:
        result["data"] = data
    if log is not None:
        current_app.logger.error(log)
    return jsonify(result)
