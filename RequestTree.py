# encoding: utf-8
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
    
    def AppendItem(self, parent, text, image=-1, selectedImage=-1, 
            data=None):
        item = super(RequestTree, self).AppendItem(parent, text, image, selectedImage,
                                                   data)
        
        return item
