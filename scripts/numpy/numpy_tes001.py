#!usr/bin/env python  
# -*- coding:utf-8 _*-
from IPython import embed
import numpy as np


a = np.arange(25)
a = a.reshape((5, 5))

b = np.array([10, 62, 1, 14, 2, 56, 79, 2, 1, 45,
              4, 92, 5, 55, 63, 43, 35, 6, 53, 24,
              56, 3, 56, 44, 78])
b = b.reshape((5,5))
print('a:')
print(a)
print('b:')
print(b)
print('a+b:')
print(a + b)
print('a-b:')
print(a - b)
print('a*b:')
print(a * b)
print('a/b:')
print(a / b)
print('a**2:')
print(a ** 2)
print('a<b:')
print(a < b) 
print('a>b:')
print(a > b)
print('a·b:')
print(a.dot(b))
print(a.sum())
print(a.cumsum())
