# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       35.py
   Description :
   Author :          cugxy
   date：            2019/10/21
-------------------------------------------------
   Change Activity:
                     2019/10/21
-------------------------------------------------

用元类来注解类的属性

- 借助元类, 我们可以在某个类完全定义好之前, 率先修改该类的属性
- 描述符与元类能够有效地组合起来, 以便对某种行为做出修饰, 或在程序允许时探查相关信息
- 如果把元类与描述符相结合, 那就可以在不使用 weakref 模块的前提下避免内存泄漏

"""


class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name        # 变成 protected 属性

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer(object):
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


class Field2(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, val in class_dict.items():
            if isinstance(val, Field2):
                val.name = key
                val.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


class DatabaseRow(object, metaclass=Meta):
    pass


class BetterCustomer(DatabaseRow):
    first_name = Field2()
    last_name = Field2()
    prefix = Field2()
    suffix = Field2()


if __name__ == '__main__':
    if 1:
        foo = Customer()
        print('Before', repr(foo.first_name), foo.__dict__)
        foo.first_name = 'Euclid'
        print('After', repr(foo.first_name), foo.__dict__)

        foo2 = Customer()
        foo2. first_name = 'cug'
        print('After foo', repr(foo.first_name), foo.__dict__)
        print('After foo2', repr(foo2.first_name), foo2.__dict__)
    if 1:
        foo = BetterCustomer()
        print('Before', repr(foo.first_name), foo.__dict__)
        foo.first_name = 'Euclid'
        print('After', repr(foo.first_name), foo.__dict__)
    pass
