#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
多线程下载管理器
@Author logbird@126.com
"""
import json
import sys
from threading import Thread
import utilsYunPan

class downloadYunPan(Thread):
    dir = None
    def __init__(self, dir):
        Thread.__init__(self)
        self.dir = dir
        
    def run(self):
        while(True):
            try:
                finfo = downloadManager.popFile()
                self.dir.downloadFile(finfo['path'], finfo['nid'], finfo['fhash'])
                sys.stdout.flush()
            except IndexError:
                break


class downloadManager():
    '''
        oriName = "反面.jpg"
        path = "/图片/反面.jpg"
        nid = "13745783832785911"
        date = "2013-07-23 19:19"
        oriSize = "167332"
        size = "163.4KB"
        scid = "21"
        preview = "1"
        hasThumb = true
        thumb = "http://t21-1.yunpan.360...972bb352e450&d=20130902"
        pic = "http://dl21.yunpan.360....af49d7acdabaad563cb964&"
        fhash = "88196e3f6edfe9280ede0aa98a28ac02e471be88"
        fileType = "jpg"
        mtime = "2013-07-23 19:19:52"
        fmtime = "2013-07-23 19:19"
    '''
    downloadQueue = []

    @classmethod
    def pushQueue(self, tree):
        '''将目录树种的待下载文件压入队列中
            tree List 目录树
        '''
        # 整理下载队列
        for i in tree:
            if len(i) > 0 and i.has_key('isDir') and i['isDir'] == 1:
                # 查询子目录
                if i.has_key('childs') and len(i['childs']) > 0:
                    tree += i['childs']
            elif len(i) > 0 and i.has_key('oriSize') and i.has_key('fileType'):
                self.downloadQueue.append(i)


    @classmethod
    def popFile(self):
        return self.downloadQueue.pop(0)

    @classmethod
    def start(self, dir, threadCount = 1):
        sThread = []
        print "Download Starting in {0} Threads, Please Wait!".format(threadCount)
        sys.stdout.flush()
        for i in xrange(0, threadCount):
            c = downloadYunPan(dir)
            c.start()
            sThread.append(c)

        for i in sThread:
            i.join()

        print "All Is Done!"

    

    
    