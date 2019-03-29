# -*- coding: utf-8 -*-
#  coding=utf-8

import math, queue

import os
from PyQt5.QtCore import QThread, pyqtSignal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from LiGlobal.tool.downloader.cmd.model import *

def latlng2tile_google(lat_deg, lng_deg, z):
    """
    convert latitude, longitude and zoom into tile in x and y axis
    referencing http://www.cnblogs.com/Tangf/archive/2012/04/07/2435545.html and https://blog.csdn.net/mygisforum/article/details/7582449
    :param lat_deg: latitude in degree
    :param lng_deg: longitude in degree
    :param z:       map scale (0-18)
    :return:        Return two parameters as tile numbers in x axis and y axis
    """
    if lat_deg >= 85.05112877980659 or lat_deg <= -85.05112877980659:
        raise Exception('wmts latitude error lat')
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** z
    x = ((lng_deg + 180.0) / 360.0 * n)
    y = ((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return x, y


def latlng2tile_TD(lat_deg, lng_deg, zoom):
    """
    convert latitude, longitude and zoom into tile in x and y axis
    referencing http://www.cnblogs.com/Tangf/archive/2012/04/07/2435545.html
    Keyword arguments:
    lat_deg -- latitude in degree
    lng_deg -- longitude in degree
    zoom    -- map scale (0-18)
    Return two parameters as tile numbers in x axis and y axis
    """
    n = math.pow(2, int(zoom + 1))
    reg = 360.0 / n
    x = (lng_deg + 180.0) // reg
    y = (90.0-lat_deg) // reg
    return x, y


def latlng2tile_terrain(lat_deg, lng_deg, z):
    """
    convert latitude, longitude and zoom into tile in x and y axis, cesium terrain rule
    :param lat_deg: latitude in degree
    :param lng_deg: longitude in degree
    :param z:       map scale (0-18)
    :return:        Return two parameters as tile numbers in x axis and y axis
    """
    n = math.pow(2, int(z + 1))
    reg = 360.0 / n
    x = (lng_deg + 180.0) // reg
    y = (lat_deg + 90.0) // reg
    return x, y


class BoundBox(object):
    '''
    地图数据（包括影像和地形） bound box，包括 z 范围
    '''
    max_lat = 0.0
    max_lng = 0.0
    min_lat = 0.0
    min_lng = 0.0
    start_zoom = 0
    end_zoom = 0

    def __init__(self, max_lat, max_lng, min_lat, min_lng, start_zoom, end_zoom):
        if not self.check_lat(max_lat):
            raise Exception('max latitude error')
            return
        if not self.check_lat(min_lat):
            raise Exception('min latitude error')
            return
        if not self.check_lng(max_lng):
            raise Exception('max longitude error')
            return
        if not self.check_lng(min_lng):
            raise Exception('min longitude error')
            return
        if not self.check_zoom(start_zoom):
            raise Exception('start zoom error')
            return
        if not self.check_zoom(end_zoom):
            raise Exception('end zoom error')
            return
        if max_lng <= min_lng:
            raise Exception('max or min latitude error')
            return
        if max_lat <= min_lat:
            raise Exception('max or min longitude error')
            return
        if start_zoom > end_zoom:
            raise Exception('error start or end zoom')
            return
        self.max_lat = max_lat
        self.max_lng = max_lng
        self.min_lat = min_lat
        self.min_lng = min_lng
        self.start_zoom = start_zoom
        self.end_zoom = end_zoom

    @staticmethod
    def check_lat(lat):
        return 90.0 >= lat >= -90.0

    @staticmethod
    def check_lng(lng):
        return 180.0 >= lng >= -180.0

    @staticmethod
    def check_zoom(zoom):
        return 0 <= zoom


class BaseDownloaderThread(QThread):
    root_dir = ''
    bbox = None
    logger = None

    sub_progressBar_updated_signal = pyqtSignal()
    running = True
    stopped = False
    task_q = queue.Queue()

    def __init__(self, root_dir, bbox, task_q, logger=None, write_db=False, db_file_name='tile.db'):
        super(BaseDownloaderThread, self).__init__()
        self.running = True
        self.stopped = False
        self.root_dir = root_dir
        self.bbox = bbox
        self.logger = logger
        self.task_q = task_q
        if self.bbox is None:
            raise Exception('bbox init error')
        self.write_db = write_db
        self.session = None
        self.num = 0
        if self.write_db:
            file_path = '%s/%s' % (self.root_dir, db_file_name)
            if not os.path.exists(file_path):
                file = open(file_path, 'w')
                file.close()
            engine_str = 'sqlite:///%s' % (file_path, )
            engine = create_engine(engine_str, echo=False)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            BaseModel.metadata.create_all(engine)

    def __del__(self):
        self.wait()
        if self.write_db:
            self.session.commit()
            self.session.close()

    def stop(self):
        self.stopped = True
        if self.write_db:
            self.session.commit()

    def pause(self):
        if self.isRunning():
            self.running = not self.running
        if self.write_db:
            self.session.commit()

    def run(self):
        try:
            while True:
                if self.running:
                    try:
                        x, y, z = self.task_q.get_nowait()
                    except queue.Empty as e:
                        break
                    _r = self._download(x, y, z)
                    if _r == 1:
                        if self.logger is not None:
                            self.logger.info('download %i %i %i OK' % (z, x, y))
                    elif _r == 0:
                        if self.logger is not None:
                            self.logger.info('download %i %i %i Exist' % (z, x, y))
                    else:
                        if self.logger is not None:
                            self.logger.error('download %i %i %i ERROR' % (z, x, y))
                    self.sub_progressBar_updated_signal.emit()
                if self.stopped:
                    if self.write_db:
                        self.session.commit()
                    break
            if self.write_db:
                self.session.commit()
                self.session.close()
        except Exception as e:
            if self.write_db:
                self.session.commit()
                self.session.close()
            if self.logger is not None:
                self.logger.error(e)

    def _download(self, x, y, z):
        """
        下载
        :param x:
        :param y:
        :param z:
        :return: 0 已存在 -1 失败 1 成功
        """
        pass

    def _data2DB(self, x, y, z, file):
        if not self.write_db:
            return 0
        if not file or not os.path.exists(file):
            return -1
        query_result = self.session.query(Tiles).filter(Tiles.zoom_level == z).filter(Tiles.tile_column == x). \
            filter(Tiles.tile_row == y).one_or_none()
        if query_result:
            if self.logger is not None:
                self.logger.error('%i %i %i is exist in database' % (z, x, y))
            return 0
        tile = Tiles(z, x, y)
        with open(file, 'rb') as f:
            tile.tile_data = f.read()
        self.session.add(tile)
        self.num += 1
        if self.num % 100 == 0:
            self.session.commit()
        return 1


class DownloadEngine(QThread):
    bbox = None
    logger = None

    thread_num = 0
    threads = []

    division_done_signal = pyqtSignal(int)
    download_done_signal = pyqtSignal()
    progressBar_updated_signal = pyqtSignal()

    def __init__(self, bbox, thread_num, logger=None, write_db=False):
        super(DownloadEngine, self).__init__()
        self.bbox = bbox
        self.logger = logger
        self.thread_num = int(thread_num)
        self.write_db = write_db

    def __del__(self):
        self.wait()

    def pause(self):
        if self.isRunning():
            for t in self.threads:
                t.pause()

    def get_task_queue(self):
        try:
            task_q = queue.Queue()
            for z in range(self.bbox.start_zoom, self.bbox.end_zoom + 1):
                min_x, min_y, max_x, max_y = self.bbox2xyz(z)
                for x in range(min_x, max_x):
                    for y in range(min_y, max_y):
                        task_q.put((x, y, z))
            return task_q
        except Exception as e:
            if self.logger is not None:
                self.logger.error(e)

    def bbox2xyz(self, z):
        return 0, 0, 0, 0

    def generate_metadata(self):
        pass

    def sub_update_progressBar(self):
        self.progressBar_updated_signal.emit()

    def run(self):
        print('DownloadEngine-run')
        pass

    def terminate(self):
        for t in self.threads:
            t.stop()
            t.quit()
        self.threads = []
        super(DownloadEngine, self).terminate()

