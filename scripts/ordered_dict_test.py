# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       ordered_dict_test.py
   Description :
   Author :          cugxy
   date：            2019/10/9
-------------------------------------------------
   Change Activity:
                     2019/10/9
-------------------------------------------------
"""


class XYOrderedDict(dict):

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('')
        try:
            self.__root
        except AttributeError:
            self.__root = root = []
            root[:] = [root, root, None]
            self.__map = {}
        # self.__update(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        dict_delitem(self, key)
        link_prev, link_next, key = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]


if __name__ == '__main__':
    if 1:
        o_d = XYOrderedDict()
        o_d[1] = 1
        o_d[2] = 2
        o_d[3] = 3
        o_d[4] = 4
        o_d[5] = 5
        o_d[-1] = -1
        o_d[-2] = -2
        o_d[-3] = -3
        o_d[-4] = -4
        o_d[-5] = -5
        for e in o_d:
            print(e)
        pass
