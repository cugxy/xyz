#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:cugxy 
@file: 32.py.py 
@time: 2019/10/19 

用 __getattr__, __getattribute__ 和 __setattr__ 实现按需生成的属性

- 通过 __getattr__ 和 __setattr__, 我们可以用惰性的方式来加载并保存对象的属性
- 要理解 __getattr__ 和 __getattribute__ 的区别: 前者只会在待访问属性缺失时触发, 而后者则会在每次访问属性时触发
- 如果要在 __getattribute__ 和 __setattr__ 方法中访问实例属性, 那么应该直接通过 super() 来做, 以避免无限递归

"""


class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, item):
        value = 'Value for %s ' % item
        setattr(self, item, value)
        return value


class LoggingLazyDB(LazyDB):
    def __getattr__(self, item):
        print('Called __getattr__(%s)' % item)
        return super().__getattr__(item)


class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, item):
        print('Called __getattribute__(%s)' % item)
        try:
            return super().__getattribute__(item)
        except AttributeError:
            value = 'Value for %s ' % item
            setattr(self, item, value)
            return value


class MissingPropertyDB(object):
    def __getattr__(self, item):
        if item == 'bad_item':
            raise AttributeError('%s is missing' % item)
        value = 'Value for %s ' % item
        setattr(self, item, value)
        return value


class SavingDB(object):
    def __setattr__(self, key, value):
        super().__setattr__(key, value)


class LoggingSavingDB(SavingDB):
    def __setattr__(self, key, value):
        print('Call __setattr__(%s, %r)' % (key, value, ))
        super().__setattr__(key, value)


class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, item):
        print('Call __getattribute__(%s)' % item)
        return self._data[item]                         # 会导致递归调用, 最终崩溃


class DictionaryDB(object):
    def __init__(self, data):
        self. _data = data

    def __getattribute__(self, item):
        data_dict = super().__getattribute__('_data')   # 可以通过 super().__getattribute__ 和 super().__setattr__ 来避免无限递归
        return data_dict[item]


if __name__ == '__main__':
    if 0:
        data = LazyDB()
        print('Before:', data.__dict__)
        print('data.foo:', data.foo)
        print('After:', data.__dict__)
    if 0:
        data = LoggingLazyDB()
        print('exists:', data.exists)
        print('foo:', data.foo)
        print('foo:', data.foo)
    if 0:
        data = ValidatingDB()
        print('exists:', data.exists)
        print('foo:', data.foo)
        print('foo:', data.foo)
    if 0:
        data = MissingPropertyDB()
        data.bad_item
    if 0:
        data = LoggingLazyDB()
        print('foo exists:', hasattr(data, 'foo'))
        print('Before:', data.__dict__)
        print('foo exists:', hasattr(data, 'foo'))
        print('After:', data.__dict__)
    if 1:
        data = LoggingSavingDB()
        print('Before:', data.__dict__)
        data.foo = 5
        print('After:', data.__dict__)
    pass
