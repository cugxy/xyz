#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:$USER
@file: $NAME 
@time: $YEAR/$MONTH/$DAY
"""
"""
av394281 中，充满威严的蕾米莉亚大小姐因为触犯某条禁忌，被隙间妖怪八云紫（紫m……èi）按住头在键盘上滚动。
同样在弹幕里乱刷梗被紫姐姐做成罪袋的你被指派找到大小姐脸滚键盘打出的一行字中的第 `k` 个仅出现一次的字。
(为简化问题，大小姐没有滚出 ascii 字符集以外的字)



输入描述:
每个输入都有若干行，每行的第一个数字为`k`，表示求第`k`个仅出现一次的字。然后间隔一个半角空格，
之后直到行尾的所有字符表示大小姐滚出的字符串`S`。

输出描述:
输出的每一行对应输入的每一行的答案，如果无解，输出字符串`Myon~`

(请不要输出多余的空行）

为了方便评测，如果答案存在且为c，请输出[c]

输入例子1:
2 misakamikotodaisuki
3 !bakabaka~ bakabaka~ 1~2~9!
3 3.1415926535897932384626433832795028841971693993751o582097494459211451488946419191919l91919hmmhmmahhhhhhhhhh
7 www.bilibili.com/av170001
1 111

输出例子1:
[d]
[9]
[l]
[7]
Myon~
"""
from IPython import embed

nan = 'Myon~'

def func(s, n):
    if s is None:
        return None
    _s = []
    d_s = []        # 重复
    for i in s:
        if i not in _s:
            _s.append(i)
        else:
            if i not in d_s:
                d_s.append(i)
    for k in d_s:
        if k in _s:
            _s.remove(k)
    if len(_s) < n:
        return None
    return _s[n-1]


if __name__ == '__main__':
    ns = []
    ss = []
    while True:
        _input = input()
        idx = _input.find(' ')
        try:
            n = int(_input[:idx])
            s = _input[idx+1:]
            ns.append(n)
            ss.append(s)
        except Exception as e:
            break
    for i in range(len(ns)):
        n = ns[i]
        s = ss[i]
        r = func(s, n)
        if r is None:
            print(nan)
        else:
            print('[%s]' % r)
    pass