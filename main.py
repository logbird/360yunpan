# -*- coding: utf8 -*-
"""
main.py

360yunpan - 360YunPan Command-line tools, support: Linux Mac Windows 
Licensed under the MIT license:
  http://www.opensource.org/licenses/mit-license.php
Project home:
  https://github.com/logbird/360yunpan
Version:  1.0.0


@Author logbird@126.com
"""
import sys
import urllib
import urllib2
import cookielib
import time
import random
import hashlib
import json
import re
import os

reload(sys)
sys.setdefaultencoding("utf-8")

import utilsYunPan
from loginYunPan import loginYunPan
from dirYunPan import dirYunPan
from downloadYunPan import downloadYunPan
from downloadYunPan import downloadManager


if __name__ == '__main__':
    login = loginYunPan()
    userinfo = login.run('username', 'password')
    # 本地文件目录
    pathYunPan = '/data/local/'
    dir = dirYunPan(pathYunPan)
    # 需要下载的云盘路径
    tree = dir.downloadDirTree('/app/', True)
    downloadManager.pushQueue(tree)
    # 设置线程数
    downloadManager.start(dir, 10)
    # 离线下载
    #result = dir.offlineDownload("http://todeer.sinaapp.com/include/lib/js/common_tpl.js");
    # 获取离线下载列表
    #result = dir.offlineList();
