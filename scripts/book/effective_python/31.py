# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       31.py
   Description :
   Author :          cugxy
   date：            2019/10/16
-------------------------------------------------
   Change Activity:
                     2019/10/16
-------------------------------------------------

用描述符来改写需要复用的 @property 方法


"""


class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value


class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, val):
        self._writing_grade = val

    @property
    def math_grade(self):
        return self._writing_grade

    @math_grade.setter
    def math_grade(self, val):
        self._writing_grade = val


class Grade(object):
    def __init__(self):
        self._value = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._value.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value[instance] = value


class Exam2(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

    pass






if __name__ == '__main__':
    if 1:
        galileo = Homework()
        galileo.grade = 95

    pass
