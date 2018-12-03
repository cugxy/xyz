#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: process_video
@time: 2018/11/25
"""
import os
from functools import partial

import numpy as np
from PyQt5.QtCore import QThread
from moviepy.video.io.VideoFileClip import VideoFileClip
from scipy.misc import imsave


def rgb2gray_3u1(rgb):
    val = rgb.dot([0.299, 0.587, 0.114])
    return val.astype('u1')


VIDEO_PATH = 'video_path'


class GetImgThread(QThread):
    def __init__(self, video_path, sample_ts, logger=None):
        super(GetImgThread, self).__init__()
        self.video_path = video_path
        self.dir_path = os.path.dirname(self.video_path)
        self.sample_ts = sample_ts
        self.logger = logger

    def _get_simple_image(self, video_path, sample_ts, img_path):
        if not video_path or not sample_ts or not img_path:
            return False
        if not os.path.exists(video_path):
            return False

        def _dump_im(src):
            imsave(img_path, src)
            return src

        clip = VideoFileClip(video_path).subclip(sample_ts, sample_ts + 1)
        clip = clip.fl_image(_dump_im)
        clip.write_videofile("%s/tmp.mp4" % self.dir_path)
        return True

    def run(self):
        try:
            img_path = '%s/sample.png' % self.dir_path
            if self._get_simple_image(self.video_path, int(self.sample_ts), img_path):
                if self.logger:
                    self.logger.info('成功截取图片，请查看 %s  找到杆塔号最后一位在图片中的位置' % img_path)
        except Exception as e:
            if self.logger:
                self.logger.error(e)

    def __del__(self):
        self.wait()


class CutVideoThread(QThread):
    def __init__(self, video_path, result_dir, x0, y0, x1, y1, time_error, size_error, logger=None):
        super(CutVideoThread, self).__init__()
        self.video_path = video_path
        self.dir_path = os.path.dirname(self.video_path)
        self.result_dir = result_dir
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.time_error = time_error
        self.size_error = size_error
        self.logger = logger

    def _cut(self, video_path, x0, y0, x1, y1, result_dir, size, min_split):
        if not video_path or not x0 or not y0 or not x1 or not y1 or not result_dir or not size or not min_split:
            return False
        if not os.path.exists(video_path):
            return False
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        def _dump_roi(get_frame, t, cache=[], cache_t=[]):
            src = get_frame(t)
            arr = rgb2gray_3u1(src)
            val = arr[y0:y1, x0:x1]
            cache.append(np.expand_dims(val, 0))
            cache_t.append(t)
            val = np.expand_dims(val, 2).repeat(3, axis=2).copy()
            return val

        clip = VideoFileClip(video_path)
        cache, cache_t = [], []
        _collect_roi = partial(_dump_roi, cache=cache, cache_t=cache_t)
        clip2 = clip.fl(_collect_roi)
        clip2.write_videofile("%s/roi.mp4" % self.dir_path)
        cache = np.vstack(cache)
        cache_t = np.hstack(cache_t)
        n, h, w = cache.shape
        arr = cache.reshape(n, -1).astype('i4')
        diff = np.abs(arr[1:, :] - arr[0:-1, :])
        diff = diff.astype('f4') / 255
        v0 = np.linalg.norm(diff, axis=1)
        t = v0 > (v0.mean() + size * v0.std())
        t = t.nonzero()[0]
        t = np.r_[0, t, n - 1]
        keep = t[1:] - t[:-1]
        keep = keep > min_split
        t = t[1:][keep]
        roi = np.r_[0, cache_t[t], cache_t[-1]]
        roi = np.c_[roi[:-1], roi[1:]]
        for e in roi[:-1]:
            tb, te = e
            clip = VideoFileClip(video_path).subclip(tb, te)
            clip.write_videofile("%s/%.2f_%.2f.mp4" % (result_dir, tb, te))
            if self.logger:
                self.logger.info('保存视频：%s/%.2f_%.2f.mp4' % (result_dir, tb, te))
        return True

    def run(self):
        try:
            if self._cut(self.video_path, self.x0, self.y0, self.x1, self.y1, self.result_dir, self.size_error, self.time_error):
                if self.logger:
                    self.logger.info('成功截取视频，请查看 %s' % self.result_dir)
        except Exception as e:
            if self.logger:
                self.logger.error(e)

    def __del__(self):
        self.wait()


if __name__ == '__main__':
    pass