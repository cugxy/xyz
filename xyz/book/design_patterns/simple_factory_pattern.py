# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       simple_factory_pattern.py
   Description :
   Author :          cugxy
   date：            2019/12/3
-------------------------------------------------
   Change Activity:
                     2019/12/3
-------------------------------------------------

https://design-patterns.readthedocs.io/zh_CN/latest/creational_patterns/simple_factory.html

简单工厂模式(Simple Factory Pattern)：又称为静态工厂方法(Static Factory Method)模式，它属于类创建型模式。在简单工厂模式中，
可以根据参数的不同返回不同类的实例。简单工厂模式专门定义一个类来负责创建其他类的实例，被创建的实例通常都具有共同的父类。

- 优点
* 工厂类或函数含有必要的判断逻辑，可以决定在什么时候创建哪一个产品类的实例，客户端可以免除直接创建产品对象的责任，
    而仅仅“消费”产品；简单工厂模式通过这种做法实现了对责任的分割，它提供了专门的工厂类用于创建对象。

* 客户端无须知道所创建的具体产品类的类名，只需要知道具体产品类所对应的参数即可，对于一些复杂的类名，
    通过简单工厂模式可以减少使用者的记忆量。

* 通过引入配置文件，可以在不修改任何客户端代码的情况下更换和增加新的具体产品类，在一定程度上提高了系统的灵活性。


- 缺点
* 由于工厂类集中了所有产品创建逻辑，一旦不能正常工作，整个系统都要受到影响。

* 使用简单工厂模式将会增加系统中类的个数，在一定程序上增加了系统的复杂度和理解难度。

* 系统扩展困难，一旦添加新产品就不得不修改工厂逻辑，在产品类型较多时，有可能造成工厂逻辑过于复杂，不利于系统的扩展和维护。

* 简单工厂模式由于使用了静态工厂方法，造成工厂角色无法形成基于继承的等级结构。

"""
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def work(self):
        pass


class ProductA(BaseProduct):
    def work(self):
        print('Product A is working.')


class ProductB(BaseProduct):
    def work(self):
        print('Product B is working.')


def create_product(product_type) -> BaseProduct:
    if product_type == 'A':
        return ProductA()
    elif product_type == 'B':
        return ProductB()
    raise ValueError('param error')


if __name__ == '__main__':
    if 1:
        product = create_product('A')
        product.work()


