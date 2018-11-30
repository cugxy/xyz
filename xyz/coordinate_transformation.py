#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: coordinate_transformation.py
@time: 2018/11/30
"""

from numpy.ma import sin, sqrt, cos
import math

PI = math.pi
_a = 6378245
_ee = 0.006693421622965823


def WGS84ToGCJ02(wgslng, wgslat):
    if not isInChina(wgslng, wgslat):
        return [wgslng, wgslat]
    d = delta(wgslng, wgslat)
    return wgslng + d[0], wgslat + d[1]


def transformLat(x, y):
    ret = -100 + 2 * x + 3 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20 * sin(6 * x * PI) + 20 * sin(2 * x * PI)) * 2 / 3
    ret += (20 * sin(y * PI) + 40 * sin(y / 3 * PI)) * 2 / 3
    ret += (160 * sin(y / 12 * PI) + 320 * sin(y * PI / 30)) * 2 / 3
    return ret


def transformLon(x, y):
    ret = 300 + x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20 * sin(6 * x * PI) + 20 * sin(2 * x * PI)) * 2 / 3
    ret += (20 * sin(x * PI) + 40 * sin(x / 3 * PI)) * 2 / 3
    ret += (150 * sin(x / 12 * PI) + 300 * sin(x / 30 * PI)) * 2 / 3
    return ret


def delta(lon, lat):
    _dLon = transformLon(lon - 105, lat - 35)
    _dLat = transformLat(lon - 105, lat - 35)
    radLat = lat / 180 * PI
    magic = sin(radLat)
    magic = 1 - _ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLon = (_dLon * 180) / (_a / sqrtMagic * cos(radLat) * PI)
    dLat = (_dLat * 180) / ((_a * (1 - _ee)) / (magic * sqrtMagic) * PI)
    return [dLon, dLat]


def isInChina(lon, lat):
    return 72.004 <= lon <= 137.8347 and 0.8293 <= lat <= 55.8271


if __name__ == '__main__':
    pass
