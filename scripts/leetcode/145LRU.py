# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       145LRU
   Description :
   Author :          cugxy
   date：            2019/7/23
-------------------------------------------------
   Change Activity:
                     2019/7/23
-------------------------------------------------

运用你所掌握的数据结构，设计和实现一个  LRU (最近最少使用) 缓存机制。它应该支持以下操作： 获取数据 get 和 写入数据 put 。

获取数据 get(key) - 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
写入数据 put(key, value) - 如果密钥不存在，则写入其数据值。当缓存容量达到上限时，它应该在写入新数据之前删除最近最少使用的数据值，从而为新的数据值留出空间。

进阶:

你是否可以在 O(1) 时间复杂度内完成这两种操作？

示例:

LRUCache cache = new LRUCache( 2 /* 缓存容量 */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // 返回  1
cache.put(3, 3);    // 该操作会使得密钥 2 作废
cache.get(2);       // 返回 -1 (未找到)
cache.put(4, 4);    // 该操作会使得密钥 1 作废
cache.get(1);       // 返回 -1 (未找到)
cache.get(3);       // 返回  3
cache.get(4);       // 返回  4

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lru-cache
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.cap = capacity
        self.data = {}
        self.keys = []

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key in self.keys:
            self.keys.remove(key)
            self.keys.append(key)
            return self.data.get(key, -1)
        return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if len(self.keys) <= self.cap - 1:
            self.__add(key, value)
        else:
            if key in self.keys:
                self.__add(key, value)
            else:
                tmp = self.keys.pop(0)
                self.data.pop(tmp)
                self.__add(key, value)

    def __add(self, key, value):
        if key not in self.keys:
            self.keys.append(key)
        else:
            self.keys.remove(key)
            self.keys.append(key)
        self.data[key] = value


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
# ["LRUCache","put","put","put","put","get","get"]
# [[2],[2,1],[1,1],[2,3],[4,1],[1],[2]]

if __name__ == '__main__':
    cache = LRUCache(2)
    cache.put(2, 1)
    cache.put(1, 1)
    cache.put(2, 3)
    cache.put(4, 1)
    print(cache.get(1))
    print(cache.get(2))


