# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       29.py
   Description :
   Author :          cugxy
   date：            2019/10/12
-------------------------------------------------
   Change Activity:
                     2019/10/12
-------------------------------------------------

用纯属性取代 get 和 set 方法
- 编写新类时, 应该用简单的 public 属性来定义其接口, 而不要手工实现 set 和 get 方法
- 如果访问对象的某个属性时, 需要表现出特殊的行为, 那就用 @property 来定义这种行为
- @property 方法应该遵循最小惊讶原则, 而不应该产生奇怪的副作用
- @property 方法需要执行得迅速一些, 缓慢或复杂得操作, 应该放在普通方法里面

"""


class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._ohms = 0

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms


class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._ohms = 0

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can not set attribute")
        self._ohms = ohms


if __name__ == '__main__':

    pass

