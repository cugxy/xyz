# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       27.py
   Description :
   Author :          cugxy
   date：            2019/10/12
-------------------------------------------------
   Change Activity:
                     2019/10/12
-------------------------------------------------

多用 public 属性, 少用 private 属性

- Python 编译器无法严格的保证 private 字段的私密性
- 不要盲目的将属性设为 private, 而是应该从一开始就做好规划, 并允许子类更多的访问超类的内部 API
- 应该多用 protected 属性 (单个 _ 开头), 并在文档中把这些字段的合理用法告诉子类的开发者, 而不要试图用 private 属性来限制子类访问这些字段
- 只有当子类不受自己控制时, 才可以考虑用 private 属性来避免名称冲突

"""


class XYZ(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


if __name__ == '__main__':
    if 1:
        foo = XYZ()
        assert foo.public_field == 5
        assert foo.get_private_field() == 10
        try:
            assert foo.__private_field == 10
        except AttributeError as e:
            print(e)
        print(foo._XYZ__private_field)
        print(foo.__dict__)

    pass

