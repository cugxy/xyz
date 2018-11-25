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