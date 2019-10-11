# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       25.py
   Description :
   Author :          cugxy
   date：            2019/10/11
-------------------------------------------------
   Change Activity:
                     2019/10/11
-------------------------------------------------

使用 super 初始化父类
- 直接调用超类的 __init__ 方法, 可能会产生无法预知的行为 (棱形继承中多次调用超类 __init__ 方法)
- 使用 super 时, 会参照, MRO 以标准的流程来安排超类之间的初始化顺序问题

"""


class XYBaseClass(object):
    def __init__(self, val):
        self.val = val


class XYChildClass(XYBaseClass):
    def __init__(self):
        XYBaseClass.__init__(self, 5)


class TimesTwo(object):
    def __init__(self):
        self.val *= 2


class PlusFive(object):
    def __init__(self):
        self. val += 5


class TimesFive(XYBaseClass):
    def __init__(self, val):
        XYBaseClass.__init__(self, val)
        self.val *= 5


class PlusTwo(XYBaseClass):
    def __init__(self, val):
        XYBaseClass.__init__(self, val)
        self.val += 2


class OneWay(XYBaseClass, TimesTwo, PlusFive):
    def __init__(self, val):
        XYBaseClass.__init__(self, val)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


class AnotherWay(XYBaseClass, PlusFive, TimesTwo):      # 调用顺序是按照超类 __init__  函数调用顺序, 而非继承顺序
    def __init__(self, val):
        XYBaseClass.__init__(self, val)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


class ThisWay(TimesFive, PlusTwo):
    def __init__(self, val):
        TimesFive.__init__(self, val)       # 先调用 XYBaseClass 将 val 设置为 5 , 再 * 5
        PlusTwo.__init__(self, val)         # 再次调用 XYBaseClass 将 val 设置为 5 , 再 + 2


class TimesFive2(XYBaseClass):
    def __init__(self, val):
        super().__init__(val)
        self.val *= 5


class PlusTwo2(XYBaseClass):
    def __init__(self, val):
        super().__init__(val)
        self.val += 2


class ThisWay2(TimesFive2, PlusTwo2):       # 使用 super 时, 会参照, MRO 以标准的流程来安排超类之间的初始化顺序问题
    def __init__(self, val):
        super().__init__(val)
        super().__init__(val)


if __name__ == '__main__':
    if 0:
        foo = OneWay(5)
        print(foo.val)
        foo2 = AnotherWay(5)
        print(foo2.val)
    if 0:
        foo = ThisWay(5)
        print('Should be (5 * 5) + 2 = 27 but is', foo.val)

    if 1:
        from pprint import  pprint
        foo = ThisWay2(5)
        print(foo.val)
        pprint(ThisWay2.mro())



