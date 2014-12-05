#!/bin/env python
# -*- coding: utf8 -*-
"""
main.py

@Author logbird@126.com
"""
import sys
import getopt 
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

conf = {
}

def usage():
    print """
  用法: ./cli.py -o http://xxx.com/xxx.tar.gz

  例子:
        开始离线下载
        ./cli.py -o http://xxx.com/xxx.tar.gz
        ./cli.py --offline="http://xxx.com/xxx.tar.gz"

  -h, --help 查看帮助
  -o, --offline 开始离线下载
  -t, --task 查看离线下载队列

    """
    sys.exit()

def login(user, pwd):
    login = loginYunPan()
    userinfo = login.run(user, pwd)
    return login, userinfo

def offlineDownload(loginObj, url):
    dir = dirYunPan('/', loginObj.serverAddr)
    result = dir.offlineDownload("http://todeer.sinaapp.com/include/lib/js/common_tpl.js");
    print result

def offlineList(loginObj):
    dir = dirYunPan('/', loginObj.serverAddr)
    result = dir.offlineList();
    list = []
    if result.hash_key('offline_task_list'):
        list = result.offline_task_list
    print list

def runCommand(conf, user, pwd):
    try:
        opts, args = getopt.getopt(sys.argv[1:],'o:th:',['offline=', 'task','help'])
    except getopt.GetoptError:
        usage()
        sys.exit()

    loginObj, user = login(user, pwd)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-o", "--offline"):
            offlineDownload(loginObj, a)
        elif o in ("-t", "--task"):
            offlineList(loginObj)
        else:
            #usage()
            pass
    return conf


if __name__ == '__main__':
    username = 'lihaohc@126.com'
    password = 'lihao123'
    # 初始化 命令行参数
    conf = runCommand(conf, username, password)
    sys.exit()




