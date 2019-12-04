# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       factory_method_pattern.py
   Description :
   Author :          cugxy
   date：            2019/12/3
-------------------------------------------------
   Change Activity:
                     2019/12/3
-------------------------------------------------

https://design-patterns.readthedocs.io/zh_CN/latest/creational_patterns/factory_method.html

工厂方法模式(Factory Method Pattern)又称为工厂模式，也叫虚拟构造器(Virtual Constructor)模式或者多态工厂(Polymorphic Factory)
模式 它属于类创建型模式。在工厂方法模式中，工厂父类负责定义创建产品对象的公共接口，而工厂子类则负责生成具体的产品对象，这样做的目的是将
产品类的实例化操作延迟到工厂子类中完成，即通过工厂子类来确定究竟应该实例化哪一个具体产品类。


- 优点
* 在工厂方法模式中, 工厂方法用来创建客户所需要的产品, 同时还向客户隐藏了那种具体产品类将被实例化这一细节, 用户只需要关心所需产品对应
    的工厂, 而无须关系创建细节, 甚至无须知道具体产品类的类名

* 基于工厂角色和产品觉得的多态性设计是工厂方法模式的关键, 它能够使工厂可以自主确定创建何种产品对象, 而如何创建这个对象的细节则会完全封装
    在具体的工厂内部, 工厂方法模式之所以又被称为多态工厂模式, 是因为所有的具体工厂类都具有同一抽象父类

* 使用工厂方法模式的另一个优点是在系统中加入新的产品时, 无须修改抽象工厂和抽象产品提供的接口, 无需修改客户端, 也无需修改其他具体工厂
    和具体产品, 而只要添加一个具体工厂和一个具体产品即可, 这样, 系统的可拓展性也就变的非常好, 完全符合"开闭原则".


- 缺点
* 在添加新产品时, 需要编写新的具体产品类, 而还要提供与之对应的具体工厂类, 系统中类的个数将成对增加, 在一定程度上增加了系统的复杂度,
    有更多的类需要处理, 会给系统带来一些额外的开销

* 由于考虑到系统的可拓展性, 需要引入抽象层, 在客户端代码中均使用抽象层进行定义, 增加了系统的抽象性和理解难度, 且在实现时有可能需要用到
    DOM, 反射等技术, 增加了系统的实现难度.

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


class BaseFactory(ABC):

    @abstractmethod
    def create_product(self) -> BaseProduct:
        pass


class FactoryA(BaseFactory):
    def create_product(self):
        return ProductA()


class FactoryB(BaseFactory):
    def create_product(self):
        return ProductB()


if __name__ == '__main__':
    if 1:
        factory = FactoryA()
        product = FactoryA.create_product()
        product.work()

