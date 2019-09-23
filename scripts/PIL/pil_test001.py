# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       pil_test001
   Description :
   Author :          cugxy
   date：            2019/9/21
-------------------------------------------------
   Change Activity:
                     2019/9/21
-------------------------------------------------
"""

from IPython import embed
from PIL import Image, ImageDraw, ImageFont


if __name__ == '__main__':
    str1 = "25°, 晴"
    font = ImageFont.truetype('simhei.ttf', 30)
    if 1:
        im = Image.open('test1.jpg')
        draw = ImageDraw.Draw(im)
        size = im.size()
        draw.text((50, 40), str1, fill=(0, 25, 25), font=font)
        im.show()
        im.save('test1_b.jpg')
        pass
    pass
