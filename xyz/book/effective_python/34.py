# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       34.py
   Description :
   Author :          cugxy
   date：            2019/10/21
-------------------------------------------------
   Change Activity:
                     2019/10/21
-------------------------------------------------

用元类来注册子类

- 再构建模块化的 Python 程序时, 类的注册是一种很有用的模式
- 开发者每次从基类中继承子类时, 基类的元类都可以自动运行注册代码
- 通过元类来实现类的注册, 可以确保所有子类都不会遗漏, 从而避免后续的错误

"""

import json


class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point 2D(%d, %d)' % (self.x, self.y, )


class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point 2D(%d, %d)' % (self.x, self.y, )


class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })


registry = {}


def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point 2D(%d, %d)' % (self.x, self.y, )


register_class(EvenBetterPoint2D)


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return 'Vector 3D(%d, %d, %d)' % (self.x, self.y, self.z, )


if __name__ == '__main__':
    if 0:
        point = Point2D(5, 3)
        print('Object:      ', point)
        print('Serialized:  ', point.serialize())
    if 1:
        point = EvenBetterPoint2D(5, 3)
        data = point.serialize()
        after = deserialize(data)
        print(after)
    if 1:
        v3 = Vector3D(1, 2, 3)
        data = v3.serialize()
        print(deserialize(data))
    pass

