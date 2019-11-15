# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       error_code.py
   Description :
   Author :          cugxy
   date：            2019/11/15
-------------------------------------------------
   Change Activity:
                     2019/11/15
-------------------------------------------------
"""


class ERROR_CODE(object):
    XY_ERR_NONE = 101               # 成功
    XY_ERR_KNOWN = -100             # 已知错误
    XY_ERR_EXCEPTION = -101         # 异常失败
    XY_ERR_TIMEOUT = -102           # 超时
    XY_ERR_RAM = -103               # 内存错误
    XY_ERR_DATABASE = -104          # 数据库错误
    XY_ERR_REDIS = -105             # redis 错误
    XY_ERR_NO_PARAM = -201          # 无足够参数
    XY_ERR_PARAM_VALUE = -202       # 参数值错误
    XY_ERR_ILLEGAL_PARAM = -203     # 非法参数
    XY_ERR_NO_DATA = -301           # 无数据

    # you can definition your error code
