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


if __name__ == '__main__':
    if 1:
        point = Point2D(5, 3)
        print('Object:      ', point)
        print('Serialized:  ', point.serialize())
    if 1:
        pass
    pass

