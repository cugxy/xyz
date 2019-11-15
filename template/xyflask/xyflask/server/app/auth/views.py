#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy 
@file: views.py 
@time: 2018/04/18 
"""
from flask import request, current_app
from flask_login import login_required, login_user, logout_user

from xyflask.database.models import User
from xyflask.server.app import db
from xyflask.server.app.auth import auth
from xyflask.util.decorators import try_exception
from xyflask.util.error_code import ERROR_CODE
from xyflask.util.jsonify_util import return_msg


@auth.route('/', methods=['GET', 'POST'])
@try_exception
def test():
    db.create_all()
    current_app.logger.info('auth 路由正常！')
    return "auth 路由正常！"


@auth.route('/login_test', methods=['GET', 'POST'])
@login_required
@try_exception
def login_test():
    current_app.logger.info('login test 路由正常！')
    return "login test 路由正常！"


@auth.route('/register', methods=['POST'])
@try_exception
def register():
    login_id = request.form.get('login_id', None, type=str)
    password = request.form.get('password', None, type=str)
    username = request.form.get('username', None, type=str)
    have_registered = User.query.filter_by(user_id=login_id).count()
    if have_registered is not 0:
        return return_msg(ERROR_CODE.XY_ERR_PARAM_VALUE, "用户已存在")
    if username is None:
        username = 'default-name'
    user = User(login_id=login_id, username=username)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
        return return_msg(ERROR_CODE.XY_ERR_NONE, "注册成功")
    except Exception as e:
        current_app.logger.exception(e)
    return return_msg(ERROR_CODE.XY_ERR_EXCEPTION, "用户名或密码不合法")


@auth.route('/login', methods=['POST'])
@try_exception
def login():
    login_id = request.form.get('login_id', None, type=str)
    password = request.form.get('password', None, type=str)
    user = db.session.query(User).filter(User.login_id == login_id).one_or_none()
    if user is None:
        return return_msg(ERROR_CODE.XY_ERR_NO_DATA, "用户名或密码错误")
    if not user.verify_password(password):
        return return_msg(ERROR_CODE.XY_ERR_PARAM_VALUE, "用户名或密码错误")
    user_json = {"username": user.username, "role": user.role_id, }
    login_user(user, True)
    return return_msg(ERROR_CODE.XY_ERR_NONE, "登录成功", data={"user": user_json, })


@auth.route('/logout', methods=['POST'])
@login_required
@try_exception
def logout():
    logout_user()
    return return_msg(ERROR_CODE.XY_ERR_NONE, "登出用户")
