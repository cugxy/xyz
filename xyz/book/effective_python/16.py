# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       16
   Description :
   Author :          cugxy
   date：            2019/7/11
-------------------------------------------------
   Change Activity:
                     2019/7/11
-------------------------------------------------

考虑使用生成器来改写直接返回列表的函数

- 使用生成器比把收集到的结果放入到列表里返回给调用者更加清晰
- 由生成器函数所返回的那个迭代器, 可以把生成器函数体中, 传给 yield 表达式的那些值, 逐次产生出来
- 无论输入量有多大, 生成器都能产生一系列输出, 因为这些输入量和输出量都不会影响它在执行时所耗的内存

"""


def index_words(text):
    rs = []
    if text:
        rs.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            rs.append(index + 1)
    return rs


def index_words_iter(text):
    if text:
        yield 0
    for idx, letter in enumerate(text):
        if letter == ' ':
            yield idx + 1


def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


if __name__ == '__main__':
    address = 'Four score and seven years ago...'
    rs = index_words(address)
    print(rs[:3])

