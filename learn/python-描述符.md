# python 描述符
## 定义

- 一个描述符是一个有**绑定行为**的对象属性, 它的访问控制会被**描述符协议**方法重写.
- 任何定义了 `__get__, __set__ ` 或者 `__delete__` 任一方法的类被称为**描述符类**, 其实例对象便是一个**描述符**,
 这些方法称为**描述符协议**.
- 当对一个实例属性进行访问时, Python 会按照, `obj.__dict__`->`type(obj).__dict__`->`super().__dict__` 顺序进行查找, 如果查找到
目标属性并发现是一个描述符, Python 会调用描述符协议来改变默认的控制行为.
- 描述符是 `@property @classmethod @staticmethod super` 的底层实现机制.

## 特性

- 同时定义了 `__get__, __set__` 的描述符称为**数据描述符(data description)**; 仅定义了 `__get__` 的称为 
**非数据描述符(non-data description)**; 两者的区别在于: 如果 `obj.__dict__` 中有与描述符同名的属性, 若描述符是数据描述符,
则优先调用描述符, 若是非数据描述符, 则优先使用 `obj.__dict__` 中属性.
- 描述符协议必须定义在类的层次, 否则无法被自动调用.

## 描述符协议

```python
def __get__(self, instance, owner):
    """
    :param self:        描述符对象
    :param instance:    使用描述符的对象
    :param owner:       使用描述符对象拥有者
    """
    pass
    
def __set__(self, instance, value):
    """
    :param self:        描述符对象
    :param instance:    使用描述符的对象
    :param value:       对描述符的赋值
    """
    pass
    
def __delete__(self, instance):
    """
    :param self:        描述符对象
    :param instance:    使用描述符的对象
    """
    pass

```

## 实例

```python
class Field2(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, val in class_dict.items():
            if isinstance(val, Field2):
                val.name = key
                val.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


class DatabaseRow(object, metaclass=Meta):
    pass


class BetterCustomer(DatabaseRow):
    first_name = Field2()
    last_name = Field2()
    prefix = Field2()
    suffix = Field2()


if __name__ == '__main__':
    if 1:
        foo = BetterCustomer()
        print('Before', repr(foo.first_name), foo.__dict__)
        foo.first_name = 'Euclid'
        print('After', repr(foo.first_name), foo.__dict__)
    pass
```