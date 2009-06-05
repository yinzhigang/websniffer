#!/usr/bin/env python
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
Created on Mar 21, 2009

@author: sxin
'''
import os
import sys

import wx
from wx import xrc

import resource

class WebSnifferApp(wx.App):
    
    def OnInit(self):
        import __builtin__
        __builtin__.__dict__['_'] = wx.GetTranslation
        
        self.SetAppName('WebSniffer')
#        L.Init(wx.LANGUAGE_CHINESE_SIMPLIFIED)
        L.Init(L.GetSystemLanguage())
        L.AddCatalogLookupPathPrefix(r'./locale')
        L.AddCatalog('messages')

        import config
        self.res = resource.GetResource()
        self.init_frame()
        return True
    
    def init_frame(self):
        if wx.Platform=="__WXMAC__":
            self.SetMacHelpMenuTitleName(_('&Help'))
            self.SetMacExitMenuItemId(xrc.XRCID('menuExit'))
            self.SetMacAboutMenuItemId(xrc.XRCID('helpAboutMenu'))
            self.SetMacPreferencesMenuItemId(xrc.XRCID('menuPreferences'))
        wx.Log_SetActiveTarget(wx.LogStderr())
        
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.frame.SetSize(wx.Size(800,600))
        self.frame.Center()
        self.frame.Show()

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(sys.argv[0])) 
    if os.path.isfile(path):
        path = os.path.dirname(path)
    os.chdir(path)
    
    L = wx.Locale()
    app = WebSnifferApp(False)
    app.MainLoop()
