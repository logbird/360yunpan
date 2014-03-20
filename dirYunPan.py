# -*- coding: utf8 -*-
"""
目录下载 文件下载
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

class dirYunPan:

    serverAddr = None
    pathYunPan = None
    directoryTree = None

    def __init__(self, pathYunPan, serverAddr):
        '''构造函数
            
            pathYunPan String 本地云盘的绝对路径
            serverAddr String 登陆成功后 loginYunPan的serverAddr属性
        '''
        self.serverAddr = serverAddr
        self.pathYunPan = pathYunPan
        self.mkdir(pathYunPan)

    def df(self):
        '''获取网盘剩余空间
        '''
        url = self.serverAddr + "/user/getsize/?t=1377829621254&ajax=1"
        result = urllib2.urlopen(url).read()
        result = json.loads(result)
        if result['errno'] == 0:
            size = {}
            size['total'] = long(result['data']['total_size'])
            size['used'] = long(result['data']['used_size'])
            size['free'] = long(result['data']['total_size']) - long(result['data']['used_size'])

            return size
        else:
            print 'Fetch Free Space Size Error! Message: '+ result['errmsg']
            sys.exit()

    def ls(self, path = '/'):
        '''获取path目录下的文件列表

            path String 需要查询的路径 根目录为 /
        '''
        url = self.serverAddr + '/file/list'
        args = {
            'ajax' : '1',
            'field' : 'file_name',
            'order' : 'desc',
            'page' : '0',
            'page_size' : '300',
            'path' : path,
            't' : str(random.random()),
            'type' : '2'
        }
        args = urllib.urlencode(args)
        reqArgs  = urllib2.Request(
            url = url,
            data = args
        )
        reqArgs.add_header("Referer", "http://c21.yunpan.360.cn/my/index/");
        result = urllib2.urlopen(reqArgs).read()
        #result = open(sys.path[0] + '/dir.dat').read()
        result = utilsYunPan.jsonRepair(result)
        result = json.loads(result)
        if result['errno'] == '0':
            return result['data']
        else:
            print 'Get Dir List Error, Please try again later! Message: '+ result['errmsg']
            sys.exit()

    def downloadFile(self, fname, nid, fileHash):
        ''' 根据文件名和节点ip下载文件

            fname String 文件路径名称 path
            nid Long 节点id
            fielHash String 文件的hash值
        '''
        # 如果hash值相同则无需下载
        #if fileHash == utilsYunPan.getFileHash(fname):
        #    return True
        url = self.serverAddr + "/file/download"
        args = {
            'fname' : fname,
            'hid' : '',
            'nid' : nid
        }
        args = urllib.urlencode(args)
        reqArgs  = urllib2.Request(
            url = url,
            data = args
        )
        reqArgs.add_header("Referer", "http://c21.yunpan.360.cn/my/index/");
        result = urllib2.urlopen(reqArgs).read()
        fname = self.pathYunPan + fname
        fname = fname.decode()
        if utilsYunPan.isText(result[0:512]):
            print "Download File: " + fname + " type: ASCII"
            open(fname, 'w').write(result)
        else:
            print "Download File: " + fname + " type: Binary"
            open(fname, 'wb').write(result)

    def downloadDirTree(self, path = '/', force = False):
        dirTreeName = utilsYunPan.getConfig('tmpDir') + '/dirTree.dat'
        tree = []
        if os.path.exists(dirTreeName):
            tree = open(dirTreeName).read()
            tree = json.loads(tree)

        if len(tree) == 0 or force:
            tree = self.fetchDirTree(path)
            open(dirTreeName, "w").write(json.dumps(tree))

        # 保存文件数
        self.directoryTree = tree

        # 开始下载文件夹
        for i in tree:
            if len(i) > 0 and i.has_key('isDir') and i['isDir'] == 1:
                self.mkdir(self.pathYunPan + i['path'])
                print "Download Directroy: " + i['path']
                # 查询子目录
                if i.has_key('childs') and len(i['childs']) > 0:
                    tree += i['childs']
        return tree

    def fetchDirTree(self, path = '/'):
        dirList = self.ls(path)
        for i in dirList:
            if len(i) > 0 and i.has_key('isDir') and i['isDir'] == 1:
                print "Fetch Directroy: " + i['path']
                i['childs']= self.fetchDirTree(i['path']);
        sys.stdout.flush()
        return dirList

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


if __name__ == '__main__':
    login = loginYunPan()
    userinfo = login.run('user', 'pwd')
    pathYunPan = 'E:/testyun'
    dir = dirYunPan(pathYunPan, login.serverAddr)
    dir.downloadFile('/文档/体检报告.pdf', '13679929262714855', 'c26aac23bd0e3c1565adeee9d6681dcab37fb2a9')





# 签到 http://c21.yunpan.360.cn/user/signin/
'''
ajax	1
'''

# 提示 http://c21.yunpan.360.cn/notice/getNoticeCount
'''
ajax	1
method	check
qid	15747194
t	1377830443043
'''

# 上传 http://c21.yunpan.360.cn/upload/getuploadaddress/
'''
ajax    1
'''