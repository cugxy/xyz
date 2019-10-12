# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       mp3_test
   Description :
   Author :          cugxy
   date：            2019/10/12
-------------------------------------------------
   Change Activity:
                     2019/10/12
-------------------------------------------------
"""
import os

from pydub import AudioSegment
from pydub.playback import play


if __name__ == '__main__':
    root = os.path.dirname(__file__)
    save_path = '%s/%s' % (root, 'ntdd1.mp4')
    if 0:
        mp3_path = '%s/%s' % (root, 'ntdd.mp3')
        sound = AudioSegment.from_mp3(mp3_path)
        start_time = "2:10"
        stop_time = "2:15"

        start_time = (int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])) * 1000
        stop_time = (int(stop_time.split(':')[0]) * 60 + int(stop_time.split(':')[1])) * 1000

        ntdd = sound[start_time:stop_time]

        ntdd.export(save_path, format="mp4")
    if 1:
        os.system("ffmpeg.exe -i ntdd1.mp4 -vf reverse -af areverse -preset superfast ntdd1_reversed.mp4")
    pass

