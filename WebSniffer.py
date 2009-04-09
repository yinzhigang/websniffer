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
        self.res = resource.GetResource()
        self.init_frame()
        return True
    
    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.frame.SetSize(wx.Size(800,600))
        self.frame.Center()
        self.frame.Show()

if __name__ == '__main__':
    app = WebSnifferApp(False)
    app.MainLoop()
