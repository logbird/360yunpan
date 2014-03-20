# -*- coding: utf8 -*-
"""
main.py

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
    # 输入用户名密码
    userinfo = login.run('用户名', '..密码')
    # 文件保存目录
    pathYunPan = 'E:/testyun'
    dir = dirYunPan(pathYunPan, login.serverAddr)
    # 需要下载的云盘路径
    tree = dir.downloadDirTree('/', True)
    downloadManager.pushQueue(tree)
    # 设置线程数
    downloadManager.start(dir, 10)