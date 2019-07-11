#!usr/bin/env python  
# -*- coding:utf-8 _*-
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
