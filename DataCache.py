# encoding: utf-8
###############################################################################
# WebSniffer - The web debug proxy.
# Copyright (C) 2009 yinzhigang <sxin.net@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
###############################################################################

'''
Created on Apr 29, 2009

@author: yinzhigang
'''
import os
import tempfile, anydbm
import random
import thread

class Cache(object):
    _cachefile = ''
    dbm = None
    
    def Init():
        if Cache._cachefile == '':
            tempath = tempfile.gettempdir()
            tempname = 'datacache' #Cache.RandomString(6)
            Cache._cachefile = os.path.join(tempath, tempname)
            if os.path.isfile(Cache._cachefile + '.db'):
                os.unlink(Cache._cachefile + '.db')
            Cache.dbm = anydbm.open(Cache._cachefile, 'n')
    Init = staticmethod(Init)
    
    def Get(name):
        return Cache.dbm[name]
    Get = staticmethod(Get)
    
    def Set(name, value):
        Cache.dbm[name] = value
    Set = staticmethod(Set)
    
    def RandomString(strlen = 20):
        """ 返回随机20位随机字符串，用于dbm key """
        
        c = ("abcdefghijklmnopqrstuvwxyz" +
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
             "0123456789-_")
        letters = [random.choice(c) for dummy in range(strlen)]
        return ''.join(letters)
    RandomString = staticmethod(RandomString)
    
    def ClearCache(init = False):
        """清除缓存"""
        if os.path.isfile(Cache._cachefile + '.db'):
#            m = thread.allocate_lock()
#            m.acquire()
            Cache.dbm.close()
            del Cache.dbm
#            Cache.dbm = None
            os.unlink(Cache._cachefile + '.db')
            Cache._cachefile = ''
            if init:
                Cache.Init()
#            m.release()
    ClearCache = staticmethod(ClearCache)

