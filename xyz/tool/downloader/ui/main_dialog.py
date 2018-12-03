#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
from PyQt5.QtCore import QSettings

from LiGlobal.tool.downloader.ui.ui_dialog import *
from LiGlobal.tool.downloader.cmd.GoogleDownloader import *
from LiGlobal.tool.downloader.cmd.TDTDownloader import *
from LiGlobal.tool.downloader.cmd.TerrainDownloader import *


ROOT_DIR = 'ROOT_DIR'


class MainDialog(QDialog):
    logger = None
    setting = QSettings('map_downloader', 'main_dialog')

    root_dir = ''
    data_type = ''
    thread_count = ''
    bbox = None

    download_engine = None

    downloading = False
    paused = True
    count = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.init_ui()
        self.init_logger()
        self.reset_state()
        self.init_connect()

    def init_ui(self):
        self.__ui.root_dir_edit.setText(self.setting.value(ROOT_DIR))
        self.init_access_token()

    def init_access_token(self):
        self.__ui.edit_access_token.setText('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkZGM5ZDhhNi00MTEzLTQ3YzUt'
                                            'OGQ1Zi0xZjE3MGM0NDYzNWEiLCJpZCI6MjU5LCJpYXQiOjE1MzU3MjQyMjh9.pIEOyZPuF4xHR'
                                            'zAQFnDgZJwgpLXDtS7vGMwha6fCs2g')
        self.__ui.widget_access_token.hide()

    def init_logger(self):
        self.logger = logging.getLogger('error')
        formatter = logging.Formatter('%(asctime)s-%(filename)s-%(levelname)s-%(message)s')
        log_file = os.path.join(os.path.dirname(__file__), 'error.log')
        file_hdlr = logging.FileHandler(log_file)
        file_hdlr.setFormatter(formatter)
        self.logger.addHandler(file_hdlr)
        self.logger.setLevel(logging.ERROR)

    def init_connect(self):
        self.__ui.root_dir_btn.clicked.connect(self.slot_root_dir_btn_clicked)
        self.__ui.download_btn.clicked.connect(self.slot_download_btn_clicked)
        self.__ui.cancel_btn.clicked.connect(self.slot_cancel_btn_clicked)
        self.__ui.data_type_combox.currentIndexChanged.connect(self.slot_data_type_combox_changed)

    def reset_state(self):
        self.downloading = False
        self.paused = True
        _translate = QtCore.QCoreApplication.translate
        self.__ui.download_btn.setText(_translate("Dialog", "download"))
        self.reset_progress()

    def reset_progress(self):
        self.count = 0
        self.__ui.progress_bar.setValue(0)

    def set_ui_state(self, enable):
        self.__ui.root_dir_edit.setEnabled(enable)
        self.__ui.root_dir_btn.setEnabled(enable)
        self.__ui.data_type_combox.setEnabled(enable)
        self.__ui.thread_count_edit.setEnabled(enable)
        self.__ui.max_lat_edit.setEnabled(enable)
        self.__ui.min_lat_edit.setEnabled(enable)
        self.__ui.max_lng_edit.setEnabled(enable)
        self.__ui.min_lng_edit.setEnabled(enable)
        self.__ui.start_zoom_edit.setEnabled(enable)
        self.__ui.end_zoom_edit.setEnabled(enable)

    def slot_data_type_combox_changed(self, index):
        if index == 2:
            self.__ui.widget_access_token.show()
        else:
            self.__ui.widget_access_token.hide()

    def slot_root_dir_btn_clicked(self):
        _translate = QtCore.QCoreApplication.translate
        _root_dir = QFileDialog.getExistingDirectory(None, _translate("Dialog", "choose directory"), self.setting.value(ROOT_DIR))
        self.__ui.root_dir_edit.setText(_root_dir)
        self.setting.setValue(ROOT_DIR, _root_dir)

    def slot_download_btn_clicked(self):
        _translate = QtCore.QCoreApplication.translate
        self.paused = not self.paused
        if not self.downloading:
            if not self.check_parameters():
                return
            self.reset_progress()
            self.__ui.download_btn.setText(_translate("Dialog", "pause"))
            self.set_ui_state(False)
            if self.data_type == 'google':
                self.download_engine = GoogleDownloadEngine(self.root_dir, self.bbox, self.thread_count, self.logger)
            elif self.data_type == 'tianditu':
                self.download_engine = TDTDownloadEngine(self.root_dir, self.bbox, self.thread_count, self.logger)
            elif self.data_type == 'terrain':
                token = self.__ui.edit_access_token.text()
                if not token:
                    msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"),
                                          _translate("Dialog", "Please enter access token first!"))
                    msg_box.exec_()
                else:
                    self.download_engine = TerrainDownloadEngine(self.root_dir, self.bbox, token, self.thread_count, self.logger)
            else:
                return
            self.download_engine.division_done_signal.connect(self.slot_division_done)
            self.download_engine.progressBar_updated_signal.connect(self.slot_progress_update)
            self.download_engine.download_done_signal.connect(self.slot_download_done)
            self.download_engine.start()
        else:
            if hasattr(self.download_engine, 'threads'):
                self.download_engine.pause()
            else:
                self.paused = not self.paused
            self.__ui.download_btn.setText(_translate("Dialog", "download") if self.paused else _translate("Dialog", "pause"))
        self.downloading = True

    def slot_cancel_btn_clicked(self):
        if hasattr(self.download_engine, 'threads'):
            self.download_engine.terminate()
        time.sleep(0.5)
        self.set_ui_state(True)
        self.reset_state()

    def slot_division_done(self, total):
        self.__ui.progress_bar.setMaximum(total)

    def slot_progress_update(self):
        self.count += 1
        self.__ui.progress_bar.setValue(self.count)

    def slot_download_done(self):
        _translate = QtCore.QCoreApplication.translate
        self.__ui.progress_bar.setValue(self.__ui.progress_bar.maximum())
        msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"),
                              _translate("Dialog", "Download completed!"))
        msg_box.exec_()
        self.reset_state()
        self.set_ui_state(True)

    def check_parameters(self):
        try:
            _translate = QtCore.QCoreApplication.translate
            _root_dir = self.__ui.root_dir_edit.text()
            if not os.path.exists(_root_dir):
                msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"),
                                      _translate("Dialog", "Storage directory is not exist!"))
                msg_box.exec_()
                return False
            self.root_dir = _root_dir
            _index = self.__ui.data_type_combox.currentIndex()
            if _index == 0:
                self.data_type = 'google'
            elif _index == 1:
                self.data_type = 'tianditu'
            elif _index == 2:
                self.data_type = 'terrain'
            else:
                msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"),
                                      _translate("Dialog", "Unknowing data type!"))
                msg_box.exec_()
                return False
            _thread_count = int(self.__ui.thread_count_edit.text())
            self.thread_count = _thread_count
            _max_lat = float(self.__ui.max_lat_edit.text())
            _min_lat = float(self.__ui.min_lat_edit.text())
            _max_lng = float(self.__ui.max_lng_edit.text())
            _min_lng = float(self.__ui.min_lng_edit.text())
            _start_zoom = int(self.__ui.start_zoom_edit.text())
            _end_zoom = int(self.__ui.end_zoom_edit.text())
            if self.data_type == 'google' or self.data_type == 'tianditu':
                if _min_lat >= 85.05112877980659 or _min_lat <= -85.05112877980659:
                    msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"),
                                        _translate("Dialog", "In mercator projection, latitude range is -85.05112877980659 to 85.05112877980659!"))
                    msg_box.exec_()
                    return False
                if _min_lat >= 85.05112877980659 or _min_lat <= -85.05112877980659:
                    msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"),
                                          _translate("Dialog", "In mercator projection, latitude range is -85.05112877980659 to 85.05112877980659!"))
                    msg_box.exec_()
                    return False
            self.bbox = BoundBox(_max_lat, _max_lng, _min_lat, _min_lng, _start_zoom, _end_zoom)
            return True
        except Exception as e:
            msg_box = QMessageBox(QMessageBox.Information, _translate("Dialog", "Tips"), str(e))
            msg_box.exec_()
            if self.logger is not None:
                self.logger.error(e)
            return False
        pass


if __name__ == '__main__':
    pass