# encoding: utf-8
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
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        
    def OnCreate(self, event):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        if wx.Platform == "__WXMAC__":
            self.MacCheckSpelling(False)
    
    def SetValue(self, value):
        if wx.Platform == "__WXMAC__":
            value = value.replace('\r\n', '\n')
        try:
            if len(value) > 2000:
                self.text = value
                self.Bind(wx.EVT_SET_FOCUS, self.OnFocus, self)
                value = value[:2000]
            super(TextCtrl, self).SetValue(value)
        except Exception, e:
            pass

    def OnFocus(self, event):
        if self.text:
            try:
                self.AppendText(self.text[2000:])
                self.SetInsertionPoint(0)
                self.text = None
            except Exception, e:
                pass
    