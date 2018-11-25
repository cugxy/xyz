#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        for _ in s:
            if _ in ['{', '[' ,'(']:
                stack.append(_)
            if _ == '}':
                if len(stack) == 0:
                    return False
                if stack[-1] == '{':
                    stack.pop()
                else:
                    return False
            if _ == ']':
                if len(stack) == 0:
                    return False
                if stack[-1] == '[':
                    stack.pop()
                else:
                    return False
            if _ == ')':
                if len(stack) == 0:
                    return False
                if stack[-1] == '(':
                    stack.pop()
                else:
                    return False
        return stack == []


if __name__ == '__main__':
    s = Solution()
    r = s.isValid("(])")
    pass