# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       __init__.py
   Description :
   Author :          cugxy
   date：            2019/5/30
-------------------------------------------------
   Change Activity:
                     2019/5/30
-------------------------------------------------
"""

from flask import Blueprint

cal = Blueprint('cal', __name__)

from xyflask.server.app.calculation import views
