# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       36.py
   Description :
   Author :          cugxy
   date：            2019/10/25
-------------------------------------------------
   Change Activity:
                     2019/10/25
-------------------------------------------------

用 subprocess 模块来管理子进程

"""
import os
import time
import subprocess


def run_sleep(preiod):
    proc = subprocess.Popen(['sleep', str(preiod)], shell=True)
    return proc


def run_openssl(data):
    env = os.environ.copy()
    env['pa']


if __name__ == '__main__':
    if 0:
        proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        print(out.decode('utf-8'))
    if 0:
        proc = subprocess.Popen(['sleep', '0.3'], shell=True)
        while proc.poll() is None:
            print('Working...')
        print('Exit status')
    if 1:
        start = time.time()
        procs = []
        for _ in range(10):
            proc = run_sleep(0.1)
            procs.append(proc)
        for proc in procs:
            proc.communicate()
        end = time.time()
        print('Finished in %.3f seconds' % (end - start, ))
    pass

