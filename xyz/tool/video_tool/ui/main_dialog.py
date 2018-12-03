#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: main_dialog
@time: 2018/11/25
"""
import logging
import os

from PyQt5.QtWidgets import QDialog, QFileDialog

from LiGlobal.tool.video_tool.ui.ui_dialog import Ui_Dialog
from LiGlobal.tool.video_tool.process.process_video import GetImgThread, CutVideoThread


class MainDialog(QDialog):

    def __init__(self, parent=None, log_path=None):
        super().__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.init_logger(log_path)
        self.init_connect()
        self.init_ui()

    def init_ui(self):
        self.__ui.stackedWidget.setCurrentIndex(0)

    def init_logger(self, log_path):
        self.logger = logging.getLogger('xyz')
        self.logger.setLevel(logging.INFO)

        class QTHandler(logging.Handler):
            def __init__(self, text):
                logging.Handler.__init__(self)
                self.text = text

            def emit(self, record):
                record = self.format(record)
                self.text.append(record)
                self.text.update()

        formatter = logging.Formatter('%(asctime)s-%(filename)s-%(levelname)s-%(message)s')
        qt_handler = QTHandler(self.__ui.text_log)
        self.logger.addHandler(qt_handler)
        qt_handler.setFormatter(formatter)
        qt_handler.setLevel(logging.INFO)
        if log_path:
            log_file = os.path.join(log_path)
            file_hdlr = logging.FileHandler(log_file)
            file_hdlr.setFormatter(formatter)
            file_hdlr.setLevel(logging.INFO)
            self.logger.addHandler(file_hdlr)
        self.logger.info('启动')

    def init_connect(self):
        self.__ui.btn_video_path.clicked.connect(self.slot_btn_video_path_clicked)
        self.__ui.btn_get_img.clicked.connect(self.slot_btn_get_img_clicked)
        self.__ui.btn_next.clicked.connect(self.slot_btn_next_clicked)
        self.__ui.btn_prv.clicked.connect(self.slot_btn_prv_clicked)
        self.__ui.btn_out_path.clicked.connect(self.slot_btn_out_clicked)
        self.__ui.btn_cut.clicked.connect(self.slot_btn_cut_clicked)

    def slot_btn_video_path_clicked(self):
        video_path = QFileDialog.getOpenFileName()[0]
        self.__ui.edit_video_path.setText(video_path)

    def slot_btn_get_img_clicked(self):
        video_path = self.__ui.edit_video_path.text()
        sample_ts = self.__ui.edit_time.text()
        if not video_path or not sample_ts:
            if self.logger:
                self.logger.error('参数错误 视频文件：%s 时间：%s' % (video_path, sample_ts))
            return
        if not os.path.exists(video_path):
            if self.logger:
                self.logger.error('参数错误 视频文件：%s 时间：%s' % (video_path, sample_ts))
            return
        img_thread = GetImgThread(video_path=video_path, sample_ts=sample_ts, logger=self.logger)
        img_thread.run()

    def slot_btn_next_clicked(self):
        self.__ui.stackedWidget.setCurrentIndex(1)

    def slot_btn_prv_clicked(self):
        self.__ui.stackedWidget.setCurrentIndex(0)

    def slot_btn_out_clicked(self):
        out_path = QFileDialog.getExistingDirectory()
        self.__ui.edit_out_path.setText(out_path)

    def slot_btn_cut_clicked(self):
        try:
            x0 = int(self.__ui.edit_x0.text())
            y0 = int(self.__ui.edit_y0.text())
            x1 = int(self.__ui.edit_x1.text())
            y1 = int(self.__ui.edit_y1.text())
            time_error = int(self.__ui.edit_error_time.text())
            size_error = int(self.__ui.edit_error_size.text())
        except Exception as e:
            if self.logger:
                self.logger.error('参数错误')
        result_dir = self.__ui.edit_out_path.text()
        video_path = self.__ui.edit_video_path.text()
        if not x0 or not y0 or not x1 or not y1 or not time_error or not size_error or not result_dir or not video_path:
            if self.logger:
                self.logger.error('参数错误')
            return
        if not os.path.exists(result_dir) or not os.path.exists(video_path):
            if self.logger:
                self.logger.error('参数错误')
            return
        cut_thread = CutVideoThread(video_path, result_dir, x0, y0, x1, y1, time_error, size_error, logger=self.logger)
        cut_thread.run()





if __name__ == '__main__':
    pass