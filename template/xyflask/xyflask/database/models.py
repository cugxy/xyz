#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy 
@file: models.py 
@time: 2018/04/18 
"""

from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


class User(UserMixin, db.Model):
    """
    用户表
    id 记录唯一标识 用于 Flask_login 模块
    login_id         用户唯一标识
    password_hash   密码 hash
    username        用户昵称
    """
    __tablename__ = 'users'
    __table_args__ = {"useexisting": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    username = Column(String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        """
        增加密码的不可读属性，防止密码泄露
        :return:
        """
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        """
        将传入的密码进行加密
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        定义比较密码的方法：传入用户输入的密码，返回bool值
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.user_id
