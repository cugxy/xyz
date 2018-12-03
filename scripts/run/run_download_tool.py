#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: run_download_tool.py
@time: 2018/12/3
"""
from PyQt5.QtWidgets import QApplication

from xyz.tool.downloader.ui.main_dialog import MainDialog


if __name__ == '__main__':
    try:
        import sys
        app = QApplication(sys.argv)
        dialog = MainDialog()
        dialog.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)