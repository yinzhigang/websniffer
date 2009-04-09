'''
Created on Apr 9, 2009

@author: yinzhigang
'''

import wx
from wx import xrc

import resource

class TextCtrl(wx.TextCtrl):
    
    def __init__(self):
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
    
    def SetValue(self, value):
        if wx.Platform == "__WXMAC__":
            value = value.replace('\r\n', '\n')
        try:
            super(TextCtrl, self).SetValue(value)
        except Exception, e:
            pass
