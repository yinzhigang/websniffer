# encoding: utf-8
'''
Created on Apr 30, 2009

@author: yinzhigang
'''

import wx
import os
import ConfigParser

_sp = wx.StandardPaths.Get()
_config_dir = _sp.GetUserDataDir()

start = None
if start is None:
    _cp = ConfigParser.ConfigParser()
    _config_file = os.path.join(_config_dir, 'config.ini')
    _cp.read(_config_file)
    start = True

def GetProxyIP():
    ip = _get('proxy', 'ip')
    if ip is None:
        ip = ''
    return ip

def SetProxyIP(ip):
    _set('proxy', 'ip', ip)

def GetProxyPort():
    port = _get('proxy', 'port')
    if port is None:
        port = '8789'
    return int(port)

def SetProxyPory(port):
    _set('proxy', 'port', port)

def save():
    if not os.path.isdir(_config_dir):
        os.mkdir(_config_dir)
    _cp.write(open(_config_file, 'w'))

def _get(section, option):
    try:
        val = _cp.get(section, option)
    except:
        val = None
    return val

def _set(section, option, value):
    if not _cp.has_section(section):
        _cp.add_section(section)
    _cp.set(section, option, value)
