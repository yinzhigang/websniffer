# encoding: utf-8
'''
Created on Mar 21, 2009

@author: sxin
'''
version = '0.1'

import os
import wx
from wx import xrc

res = None;
path = os.path.dirname(os.path.realpath(__file__)) 
if os.path.isfile(path):
    path = os.path.dirname(path)
os.chdir(path)

def GetResource():
    global res
    if res is None:
        res = xrc.XmlResource('window/window.xrc')
    return res
