#!usr/bin/env python  
# -*- coding:utf-8 _*-

"""
了解如何在闭包里使用外围作用域中的变量

- 对于定义在某作用域内的闭包来说, 它可以引用这些作用域中的变量
- 使用默认方式对闭包内的变量赋值, 不会影响外围作用域中的同名变量
- 在 python 3 中, 程序可以在闭包内用 nonlocal 语句来修饰某个名称, 使该闭包能够修改外围作用域中的同名变量
- 在 python 2 中, c'x
"""

numbers = [8, 3, 1, 2, 5, 4, 7, 6, ]
group = {2, 3, 5, 7, }


def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


def sort_priority2(values, group):
    found = False

    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x, )
        return (1, x, )
    values.sort(key=helper)
    return found


class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)


if __name__ == '__main__':
    if 1:
        f = sort_priority2(numbers, group)
        print(f)
        print(numbers)
    if 1:
        sorter = Sorter(group)
        numbers.sort(key=sorter)
        print(sorter.found)
        print(numbers)
