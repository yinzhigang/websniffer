# encoding: utf-8
'''
Created on Mar 21, 2009

@author: sxin
'''
version = '0.1'

import wx
from wx import xrc

res = None;

def GetResource():
    global res
    if res is None:
        res = xrc.XmlResource('window/window.xrc')
    return res
