#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:cugxy
@file: __init__.py.py
@time: 2018/04/18
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from xyflask.server.app.auth import views
