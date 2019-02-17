#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


number_dict = {'2' : ['a', 'b', 'c', ],
               '3' : ['d', 'e', 'f', ],
               '4' : ['g', 'h', 'i', ],
               '5' : ['j', 'k', 'l', ],
               '6' : ['m', 'n', 'o', ],
               '7' : ['p', 'q', 'r', 's', ],
               '8' : ['t', 'u', 'v', ],
               '9' : ['w', 'x', 'y', 'z', ],
               }


def fun(digits):
    if len(digits) == 0:
        return ['', ]
    if len(digits) == 1:
        return number_dict[digits]
    result = []
    s = digits[-1]
    digits = digits[0: -1]
    r = fun(digits)
    for _ in number_dict[s]:
        for _r in r:
            r1 = _r + _
            result.append(r1)
    return result


class Solution:
    """
    给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。

    给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

    示例:

    输入："23"
    输出：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
    """
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        return fun(digits)


if __name__ == '__main__':
    s = Solution()
    p = '23'
    r = s.letterCombinations(p)
    pass