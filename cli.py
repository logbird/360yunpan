#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
命令行工具

  用法: ./cli.py -o http://xxx.com/xxx.tar.gz

  例子:
        开始离线下载
        ./cli.py -o http://xxx.com/xxx.tar.gz
        ./cli.py --offline="http://xxx.com/xxx.tar.gz"

  -h, --help 查看帮助
  -o, --offline 开始离线下载
  -t, --task 查看离线下载队列

360yunpan - 360YunPan Command-line tools, support: Linux Mac Windows 
Licensed under the MIT license:
  http://www.opensource.org/licenses/mit-license.php
Project home:
  https://github.com/logbird/360yunpan
Version:  1.0.0

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
    print result['task_id']

def offlineList(loginObj):
    dir = dirYunPan('/', loginObj.serverAddr)
    result = dir.offlineList();
    task_list = {}
    if result.has_key('offline_task_list'):
        task_list = result['offline_task_list']
    for i in task_list:
        print "%s\t%s\t%s" % (i['status'], i['task_id'], i['url'])

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
    username = '账号'
    password = '密码'
    # 初始化 命令行参数
    conf = runCommand(conf, username, password)
    sys.exit()




