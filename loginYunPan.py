# -*- coding: utf8 -*-
"""
云盘登陆，该类可以登录所有使用360账号登录的网站
@Example
    login = loginYunPan()
    userinfo = login.run('user', 'pwd')
    print userinfo

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

class loginYunPan():

    cookieFile = None
    cookie_jar = None
    serverAddr = None
    userFile = None

    def __init__(self):
        self.envInit()
        self.loginInit()

    def envInit(self):
        base = sys.path[0] + "/tmp"
        self.userFile = base + '/user.dat'
        self.cookieFile = base + '/cookie.dat' 
        if not os.path.isdir(base):
            os.mkdir(base)
        if not os.path.exists(self.userFile):
            open(self.userFile, 'w').close()
        if not  os.path.exists(self.cookieFile):
            open(self.cookieFile, 'w').close()

    def loginInit(self):       
        self.cookie_jar  = cookielib.LWPCookieJar(self.cookieFile)
        try:
            self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
        except Exception:
            self.cookie_jar.save(self.cookieFile, ignore_discard=True, ignore_expires=True)
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie_jar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def getToken(self, username):
        '''根据用户名等信息获得登陆的token值
            
            username String 用户名
            return 返回Token 值
        '''
        login = {
            'callback' : 'QiUserJsonP1377767974691',
            'func' : 'test',
            'm' : 'getToken',
            'o' : 'sso',
            'rand' : str(random.random()),
            'userName' : username
        }

        url = "https://login.360.cn/?"
        queryString = urllib.urlencode(login)
        url += queryString
        result = urllib2.urlopen(url).read()
        result = result.strip(' ')
        result = json.loads(result[5:-1])
        token = ''
        if int(result['errno']) == 0:
            print 'getToken Success'
            token = result['token']
            self.cookie_jar.save(self.cookieFile, ignore_discard=True, ignore_expires=True)
        else:
            print 'getToken Failed, Errno:' + str(result['errno'])
            sys.exit()
        return token


    def doLogin(self, username, password, token):
        '''开始执行登陆操作
            
            username String 用户名
            password String 密码
            token String 根据getToken获得
        '''
        login = {
            'callback' : 'QiUserJsonP1377767974692',
            'captFlag' : '',
            'from' : 'pcw_cloud',
            'func' : 'test',
            'isKeepAlive' : '0',
            'm' : 'login',
            'o' : 'sso',
            'password' : self.pwdHash(password),
            'pwdmethod' : '1',
            'r' : str((long)(time.time()*100)),
            'rtype' : 'data',
            'token' : token,
            'userName' : username
        }
        url = "https://login.360.cn/?"
        queryString = urllib.urlencode(login)
        url += queryString
        result = urllib2.urlopen(url).read()
        result = result.replace("\n", '').strip(' ')
        result = json.loads(result[5:-1])
        userinfo = {}
        if int(result['errno']) == 0:
            print 'Login Success'
            userinfo = result['userinfo']
            open(self.userFile, 'w').write(json.dumps(userinfo))
            self.cookie_jar.save(self.cookieFile, ignore_discard=True, ignore_expires=True)
        else:
            print 'Login Failed, please check your password in cli.py or main.py, Errno:' + str(result['errno'])
            sys.exit()
        return userinfo


    def getServer(self):
        '''获得分布式服务器的地址
            
            return True 已登录 False 未登录
        '''
        url = 'http://yunpan.360.cn/user/login?st=163'
        result = urllib2.urlopen(url).read()
        regx = "web : '([^']*)'"
        server = re.findall(regx, result)
        if len(server) and server[0] != '' > 0:
            print "Get Server Success, Server Address:" + server[0]
            self.serverAddr = server[0]
            return True
        else:
            print "Logining!"
            return False


    def run(self, username, password):
        '''开始执行登陆流程
            
            username String 用户名
            password String 密码
        '''
        userinfo = None
        if self.getServer():
            print 'Login Success!'
            userinfo = open(self.userFile).read()
            userinfo = json.loads(userinfo)
            return userinfo
        else:
            # 获取token
            token = self.getToken(username)
            # 登陆
            userinfo = self.doLogin(username, password, token);
            # 获得分布式服务器
            self.getServer()
        return userinfo


    def pwdHash(self, password):
        '''md5操作函数用于密码加密

            password String 需要加密的密码
            return 加密后的密码
        '''
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()



if __name__ == '__main__':
    login = loginYunPan()
    userinfo = login.run('user', 'pwd')
    print userinfo

    

'''
{"errno":0,
"errmsg":"",
"s":"e4x7a%27FD%7EtNm%3AF%29To.%20ocV%40%3CUC7Z3%2F%7Ce%3C%2Aw%40CsRMK%3FE8FUD5.m%27%3F%5D%2C%25p4tqp7%22%40%3Fs%7ETzr%2C%3D%21CE-%3C%5Be%3E%26j%28s%2C%25U%7DPP%5C%5E_4%28arVSU%28%3ECa%5Cr_o%2CS%28%2BJ%2FA%21.%2CWZRAwptNdB4%7D%3BeY3XP-WR3%24%24%29pt%3Ey%25ia%23D%24%3E%7D8%3A%28nH2G0C%23%2Cg%5D09Y%40jF%5EF4h%23",
"userinfo":
    {"qid":"15747194",
    "userName":"logbird",
    "nickName":"",
    "realName":"",
    "imageId":"1c03c17q97c61",
    "theme":"quc",
    "src":"quanzi",
    "type":"formal",
    "loginEmail":"",
    "loginTime":"1377767983",
    "lm":"",
    "unSafeLogin":"0",
    "isKeepAlive":"0",
    "crumb":"020c3d",
    "imageUrl":"http:\/\/u.qhimg.com\/qhimg\/quc\/48_48\/1c\/03\/c1\/1c03c17q97c61.892c07.jpg"
    }
}
'''
