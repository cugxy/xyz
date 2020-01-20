# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       holiday.py
   Description :
   Author :          cugxy
   date：            2020/1/20
-------------------------------------------------
   Change Activity:
                     2020/1/20
-------------------------------------------------
"""
import time

if __name__ == '__main__':
    holiday = '2020-01-20 18:00:00'
    holiday = time.strptime(holiday, '%Y-%m-%d %H:%M:%S')
    holiday = int(time.mktime(holiday))
    while True:
        time.sleep(0.5)
        now = int(time.time())
        print('\rholiday:%s' % (holiday - now), end="")

