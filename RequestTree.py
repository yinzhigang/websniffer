'''
Created on Apr 4, 2009

@author: yinzhigang
'''

import wx
from wx import xrc

import resource

class RequestTree(wx.TreeCtrl):
    
    def __init__(self):
        pre = wx.PreTreeCtrl()
        self.PostCreate(pre)
