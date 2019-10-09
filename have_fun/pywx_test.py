# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       pywx_test
   Description :
   Author :          cugxy
   date：            2019/9/27
-------------------------------------------------
   Change Activity:
                     2019/9/27
-------------------------------------------------
"""

from wxpy import *
from IPython import embed

bot = Bot()


if __name__ == '__main__':
    if 1:
        zhu = bot.friends().search(sex=FEMALE, city='冰岛')
        print(zhu)
        embed()
