# encoding: utf-8
'''
Created on Apr 23, 2009

@author: yinzhigang
'''
import wx
from wx import xrc

import resource
import config

class PreferencesDialog(wx.Dialog):
    
    def __init__(self):
        pre = wx.PreDialog()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
    
    def OnCreate(self, event):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        wx.CallAfter(self._PostInit)

    def _PostInit(self):
        """配置控件并设置初始值"""
        self.address_text = xrc.XRCCTRL(self, 'address_text')
        self.address_text.SetValue(unicode(config.GetProxyIP()))
        self.port_text = xrc.XRCCTRL(self, 'portText')
        self.port_text.SetValue(unicode(config.GetProxyPort()))

    def Save(self):
        """保存配置文件"""
        config.SetProxyIP(self.address_text.GetValue())
        config.SetProxyPory(self.port_text.GetValue())
        config.save()
