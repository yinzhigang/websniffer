#!/usr/bin/python
# encoding: utf-8
'''
Created on Mar 21, 2009

@author: sxin
'''
import wx
import resource

class WebSnifferApp(wx.App):
    
    def OnInit(self):
        import __builtin__
        __builtin__.__dict__['_'] = wx.GetTranslation
        
        L.Init(wx.LANGUAGE_CHINESE_SIMPLIFIED)
        L.AddCatalogLookupPathPrefix(r'./locale')
        L.AddCatalog('messages')

        self.res = resource.GetResource()
        self.init_frame()
        return True
    
    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.frame.SetSize(wx.Size(800,600))
        self.frame.Center()
        self.frame.Show()

if __name__ == '__main__':
    L = wx.Locale()
    app = WebSnifferApp(False)
    app.MainLoop()
