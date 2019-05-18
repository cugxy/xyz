# 第一行包括一个数字N，表示本次用例包括多少个待校验的字符串。
# 后面跟随N行，每行为一个待校验的字符串。

# 2
# helloo
# wooooooow

# hello
# woow
import numpy as np


def func1(s):
    s_set = []
    for item in s:
        if item not in s_set:
            s_set.append(item)
    f = False
    while True:
        if f:
            break
        f = True
        for item in s_set:
            t_s = '%s%s%s' % (item, item, item, )
            idx = s.find(t_s) 
            if idx != -1:
                f = False
                s = s[:idx] + s[idx+1:]
    return s


def func2(s):
    f = False
    while True:
        if f:
            break
        f = True
        index = 0
        t = []
        for i in s:
            _t = []
            for j in s:
                if i == j:
                    _t.append(1)
                else:
                    _t.append(0)
            t.append(_t)
        t = np.array(t)
        for k in range(index, len(s)):
            if find2(t, k):
                index = k
                s = s[:k+2] + s[k+3:]
                f = False
                break
    return s


def find2(t, k):
    n = t.shape[0]
    if n - k <= 3:
        return False
    return np.all(t[k:k+2,k:k+2]) == 1 and np.all(t[k+2:k+4,k+2:k+4]) == 1
       

def func(s):
    s = func1(s)
    s = func2(s)
    return s

if __name__ == '__main__':
    print(func('vvummmxxxppaaarrrzzeennmmqqqljeecccrpqqquuummjjjqqquuuyyyvviiicccbbimuucqqqnnnrrfffddhslllsssiiiwwwnnlllrrrzzbblwaxxvvvjjjbbbggeemsfglcxxnnnddcccuuuzzlllzzmxxxxxxkkkxxxfffddejjjuuqqxxooniiyyyzz  '))
    n = int(input())
    ss = []
    for i in range(n):
        ss.append(input())
    for item in ss:
        print(func(item))
    pass