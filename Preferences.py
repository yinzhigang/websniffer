'''
Created on Apr 23, 2009

@author: yinzhigang
'''
import wx
from wx import xrc

import resource

class PreferencesDialog(wx.Dialog):
    
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
    
    def OnCreate(self, event):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        wx.CallAfter(self._PostInit)

    def _PostInit(self):
        address = xrc.XRCCTRL(self, 'address_text')
        address.SetValue('127.0.0.1')
        port = xrc.XRCCTRL(self, 'portText')
        port.SetValue('8789')
