import sys
from IPython import embed

class A:
    pass
 
def func(x):
    print(f'对象a：{sys.getrefcount(x)-1}',end='  ')
    return x
 
#a=123.56
embed()
a=A()       #创建对象a
print(f'对象a：{sys.getrefcount(a)-1}')
b=a         #再一次引用对象a
print(f'对象a：{sys.getrefcount(a)-1}，对象b：{sys.getrefcount(b)-1}')
c=func(a)   #对象a作为函数参数
print(f'对象c：{sys.getrefcount(c)-1}')
d=list()    #对象a作为列表元素
d.append(a)
print(f'对象a：{sys.getrefcount(a)-1}，对象d：{sys.getrefcount(d)-1}')
