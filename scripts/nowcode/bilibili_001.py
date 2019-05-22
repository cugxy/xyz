#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:$USER
@file: $NAME 
@time: $YEAR/$MONTH/$DAY
"""  
from IPython import embed

result = []


def func3(x):
    result.append('3')
    return (x - 2) / 2


def func2(x):
    result.append('2')
    return (x - 1) / 2


def func(n):
    if n == 0:
        return []
    if n == 1:
        return ['2']
    if n == 2:
        return ['3']
    while True:
        if n <= 0:
            return result[: :-1]
        if n % 2 == 0:
            n = func3(n)
        else:
            n = func2(n)


if __name__ == '__main__':
    n = int(input())
    r = ''
    rs = func(n)
    if rs:
        for i in rs:
            r = r + i
    print(r)
    pass
