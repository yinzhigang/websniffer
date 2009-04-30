# encoding: utf-8
'''
Created on Apr 29, 2009

@author: yinzhigang
'''
import os
import tempfile, anydbm
import random

class Cache(object):
    _cahefile = None
    dbm = None
    
    def Init():
        if Cache._cahefile is None:
            tempath = tempfile.gettempdir()
            cache_file = os.path.join(tempath, 'datacache')
            if os.path.isfile(cache_file):
                os.unlink(cache_file)
            Cache.dbm = anydbm.open(cache_file, 'n')
    Init = staticmethod(Init)
    
    def Get(name):
        return Cache.dbm[name]
    Get = staticmethod(Get)
    
    def Set(name, value):
        Cache.dbm[name] = value
    Set = staticmethod(Set)
    
    def RandomString():
        """返回随机20位随机字符串，用于dbm key"""
        
        c = ("abcdefghijklmnopqrstuvwxyz" +
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
             "0123456789-_")
        letters = [random.choice(c) for dummy in "12345678901234567890"]
        return ''.join(letters)
    RandomString = staticmethod(RandomString)

