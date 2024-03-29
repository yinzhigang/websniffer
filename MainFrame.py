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

import wx
from wx import xrc
import wx.gizmos

from cStringIO import StringIO
import cPickle as pickle
import urllib, urlparse, cgi

import resource
from DataCache import Cache

class MainFrame(wx.Frame):
    """主窗口"""
    
    def __init__(self):
        """初始化主窗口"""
        pre = wx.PreFrame()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
    
    def OnCreate(self, event):
        """加载资源并呼叫初始化"""
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self.res = resource.GetResource()
        icon = wx.Icon('images/websniffer.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        wx.CallAfter(self._PostInit)
    
    def _PostInit(self):
        """初始化窗口控件"""
        self.Bind(wx.EVT_MENU, self.OnPreferences, 
                  id=xrc.XRCID('menuPreferences'))
        self.Bind(wx.EVT_MENU, self.OnExit, 
                  id=xrc.XRCID('menuExit'))
        self.Bind(wx.EVT_MENU, self.OnHomePage, 
                  id=xrc.XRCID('helpHomePageMenu'))
        self.Bind(wx.EVT_MENU, self.OnAbout, 
                  id=xrc.XRCID('helpAboutMenu'))
        
        self.Bind(wx.EVT_TOOL, self.OnProxyStart, 
                  id=xrc.XRCID('toolBarStart'))
        self.Bind(wx.EVT_TOOL, self.OnClearAll, 
                  id=xrc.XRCID('toolBarClearAll'))
        self.Bind(wx.EVT_TOOL, self.OnPreferences, 
                  id=xrc.XRCID('toolBarPreferences'))
        
        self.infoPanel = xrc.XRCCTRL(self, 'infoPanel')
        self.info_notebook = xrc.XRCCTRL(self, 'info_notebook')
        
        il = wx.ImageList(16, 16)
        self.fldridx = il.Add(wx.Image('images/tree/folderclosed.png', 
                                       wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.fldropen = il.Add(wx.Image('images/tree/folderopen.png', 
                                        wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.itemgeneric = il.Add(wx.Image('images/tree/generic.png', 
                                           wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        
        self.request_tree = xrc.XRCCTRL(self, 'request_tree')
        self.request_tree.AssignImageList(il)
        self.request_tree.Bind(wx.EVT_TREE_SEL_CHANGED,
              self.OnRequestTreeSelChanged, id=xrc.XRCID('request_tree'))
        self.tree_root = self.request_tree.AddRoot('root')
    
    def OnRequestTreeSelChanged(self, event):
        """ RequesTree选择更换事件 """
        item = event.GetItem()
        if self.request_tree.ItemHasChildren(item) is False:
            data = self.request_tree.GetItemPyData(item)
            parse_info = pickle.loads(Cache.Get(data))
#            try:
            self.ShowInfo(parse_info)
#            except:
#                self.infoPanel.Thaw()
#                print 'ShowInfo error'
    
    def ShowInfo(self, parse_info):
        """ 显示相关请求信息 """
        self.infoPanel.Freeze()
        bookSelection = self.info_notebook.GetSelection()
        self.info_notebook.DeleteAllPages()
        #========== General Tab ===========
        generalPanpel = self.res.LoadPanel(self.info_notebook, 'generalPanel')
        self.info_notebook.AddPage(page=generalPanpel,
                                   select=True, text=_("General"))
        
        generalBoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        treeListCtrl1 = wx.gizmos.TreeListCtrl(id=-1,
              name='treeListCtrl1', parent=generalPanpel,
              size=generalPanpel.GetSize(),
              style=wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT |
              wx.TR_DEFAULT_STYLE | wx.TR_NO_LINES)
        treeListCtrl1.AddColumn(text=_('Name'), width=150)
        treeListCtrl1.AddColumn(text=_('Value'), width=350)
        root = treeListCtrl1.AddRoot('root')
        generalList = [(_('URL:'), parse_info.getUrl()),
                       (_('Status:'), parse_info.getStatus()),
                       (_('Host:'), parse_info.getHost()),
                       (_('Client:'), parse_info.getClient()),
                       (_('Content-Type:'), parse_info.header('response', 'Content-Type')),
                       ]
        i = 0
        for label, value in generalList:
            item = treeListCtrl1.AppendItem(root, label)
            treeListCtrl1.SetItemText(item, value, 1)
            if i % 2:
                treeListCtrl1.SetItemBackgroundColour(item, "light blue")
            i += 1
        treeListCtrl1.Expand(root)
        
        generalPanpel.SetSizer(generalBoxSizer)
        generalBoxSizer.Add(treeListCtrl1, 1, border=2, flag=wx.EXPAND)
        #========== End General Tab ===========
        #========== Request Tab ===========
        requestPanel = self.res.LoadPanel(self.info_notebook, 'notebookPanel')
        self.info_notebook.AddPage(page=requestPanel, select=False, text=_("Request"))
        
        requestBook = xrc.XRCCTRL(requestPanel, 'noteBook')
        
        requestHeader = self.res.LoadPanel(requestBook, 'textPanel')
        requestHeaderTextCtrl = xrc.XRCCTRL(requestHeader, 'textCtrl')
        request_header_text = parse_info.getHeaderText('request')
        requestBook.AddPage(page=requestHeader, select=True, text=_("Headers"))
        requestHeaderTextCtrl.SetValue(request_header_text)
        
        (scm, host, path, params, query, fragment) = urlparse.urlparse(parse_info.getUrl())
        if query:
            query_arr = cgi.parse_qs(query)
            queryPanel = self.res.LoadPanel(requestBook, 'listPanel')
            queryListCtrl = xrc.XRCCTRL(queryPanel, 'listCtrl')
            requestBook.AddPage(page=queryPanel, select=False, text=_("Query"))
            queryListCtrl.InsertColumn(0, _('Key'), width=150)
            queryListCtrl.InsertColumn(1, _('Value'), width=350)
            i = 0
            for key, value in query_arr.items():
                queryItem = queryListCtrl.InsertStringItem(i, label=key)
                if i % 2:
                    queryListCtrl.SetItemBackgroundColour(queryItem, "light blue")
                queryListCtrl.SetStringItem(queryItem, 1, value[0])
                i += 1
#            query_arr = dict(part.split('=') for part in query.split('&'))
        
        request_cookie = parse_info.cookie('request')
        if request_cookie:
            requestCookie = self.res.LoadPanel(requestBook, 'listPanel')
            requestCookieListCtrl = xrc.XRCCTRL(requestCookie, 'listCtrl')
            requestBook.AddPage(page=requestCookie, select=False, text=_("Cookies"))
            requestCookieListCtrl.InsertColumn(0, _('Key'), width=150)
            requestCookieListCtrl.InsertColumn(1, _('Value'), width=350)
            i = 0
            for key, value in request_cookie.items():
                cookieItem = requestCookieListCtrl.InsertStringItem(i, label=key)
                if i % 2:
                    requestCookieListCtrl.SetItemBackgroundColour(cookieItem, "light blue")
                requestCookieListCtrl.SetStringItem(cookieItem, 1, value.value)
                i += 1
        
        requestRaw = self.res.LoadPanel(requestBook, 'textPanel')
        requestRawTextCtrl = xrc.XRCCTRL(requestRaw, 'textCtrl')
        request_raw_text = parse_info.raw('request')
        request_raw_text = repr(request_raw_text)
        requestBook.AddPage(page=requestRaw, select=False, text=_("Raw"))
        requestRawTextCtrl.SetValue(request_raw_text)
        #========== End Request Tab ===========
        #========== Response Tab ===========
        responsePanel = self.res.LoadPanel(self.info_notebook, 'notebookPanel')
        self.info_notebook.AddPage(page=responsePanel, select=False, text=_("Response"))
        
        responseBook = xrc.XRCCTRL(responsePanel, 'noteBook')
        
        responseHeader = self.res.LoadPanel(responseBook, 'textPanel')
        responseHeaderTextCtrl = xrc.XRCCTRL(responseHeader, 'textCtrl')
        response_header_text = parse_info.getHeaderText('response')
        responseBook.AddPage(page=responseHeader, select=True, text=_("Headers"))
        responseHeaderTextCtrl.SetValue(response_header_text)
        
        response_cookie = parse_info.cookie('response')
        if response_cookie:
            responseCookie = self.res.LoadPanel(responseBook, 'listPanel')
            responseCookieListCtrl = xrc.XRCCTRL(responseCookie, 'listCtrl')
            responseBook.AddPage(page=responseCookie, select=False, text=_("Cookies"))
            responseCookieListCtrl.InsertColumn(0, _('Key'), width=150)
            responseCookieListCtrl.InsertColumn(1, _('Value'), width=350)
            responseCookieListCtrl.InsertColumn(2, _('Domain'), width=100)
            responseCookieListCtrl.InsertColumn(3, _('Path'), width=100)
            i = 0
            for key, value in response_cookie.items():
                cookieItem = responseCookieListCtrl.InsertStringItem(i, label=key)
                responseCookieListCtrl.SetStringItem(cookieItem, 1, value.value)
                responseCookieListCtrl.SetStringItem(cookieItem, 2, value['domain'])
                responseCookieListCtrl.SetStringItem(cookieItem, 3, value['path'])
                i += 1
        
        content_type = parse_info.header('response', 'Content-Type')
        if content_type[:5] == 'image':
            try:
                responseBody = self.res.LoadPanel(responseBook, 'imagePanel')
                responseBodyImageCtrl = xrc.XRCCTRL(responseBody, 'image')
                response_body_image = StringIO(parse_info.getBodyContent('response'))
                image = wx.ImageFromStreamMime(response_body_image, 
                                               content_type).ConvertToBitmap()
                responseBook.AddPage(page=responseBody, select=False, text=_("Image"))
                responseBodyImageCtrl.SetBitmap(image)
            except Exception, e:
                pass
        else:
            responseBody = self.res.LoadPanel(responseBook, 'textPanel')
            responseBodyTextCtrl = xrc.XRCCTRL(responseBody, 'textCtrl')
            response_body_text = parse_info.getBodyContent('response')
            responseBook.AddPage(page=responseBody, select=False, text=_("Text"))
            responseBodyTextCtrl.SetValue(response_body_text)
        
        responseRaw = self.res.LoadPanel(responseBook, 'textPanel')
        responseRawTextCtrl = xrc.XRCCTRL(responseRaw, 'textCtrl')
        response_raw_text = parse_info.raw('response')#.decode('utf-8', 'ignore')
        response_raw_text = repr(response_raw_text)
        responseBook.AddPage(page=responseRaw, select=False, text=_("Raw"))
        responseRawTextCtrl.SetValue(response_raw_text)
        #========== End Response Tab ===========
        if bookSelection > 0:
            self.info_notebook.ChangeSelection(bookSelection)
        self.infoPanel.Thaw()

    def OnProxyStart(self, event):
        """启动检测"""
        import SocketServ
        if event.IsChecked():
            Cache.Init()  #初始化缓存
            self.thread = SocketServ.StartServer('SocketServ', self)
            self.thread.setDaemon(1)
            self.thread.start()
            if wx.Platform == '__WXMSW__':
                import _winreg as winreg
                from ctypes import windll
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings',
                        0, winreg.KEY_WRITE|winreg.KEY_READ)
                self.ProxyEnable = winreg.QueryValueEx(key, 'ProxyEnable')
                self.ProxyServer = winreg.QueryValueEx(key, 'ProxyServer')
                winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ,
                                  'http=localhost:8789;https=localhost:8789;')
                winreg.CloseKey(key)
                windll.wininet.InternetSetOptionW(None, 39, None, 0)
        else:
            if wx.Platform == '__WXMSW__':
                import _winreg as winreg
                from ctypes import windll
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings',
                        0, winreg.KEY_WRITE|winreg.KEY_READ)
                winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, '')
                winreg.CloseKey(key)
                windll.wininet.InternetSetOptionW(None, 39, None, 0)
            self.thread.stop()

    def DoNewRequest(self, path, data = ''):
        """添加请求到树中"""
        host, path, params, query = path
        item, cookie = self.request_tree.GetFirstChild(self.tree_root)
        host_item = None
        while item:
            text = self.request_tree.GetItemText(item)
            if text == host:
                host_item = item
                break
            item, cookie = self.request_tree.GetNextChild(self.tree_root, cookie)
        if host_item is None:
            host_item = self.request_tree.AppendItem(self.tree_root, host)
            self.request_tree.SetItemImage(host_item, self.fldridx,
                                           wx.TreeItemIcon_Normal)
            self.request_tree.SetItemImage(host_item, self.fldropen,
                                           wx.TreeItemIcon_Expanded)
        url = urlparse.urlunparse(('', '', path, params, query, ''))
        request = self.request_tree.AppendItem(host_item, url)
        self.request_tree.SetItemImage(request, self.itemgeneric,
                                       wx.TreeItemIcon_Normal)
        self.request_tree.SetItemPyData(request, data)

    def OnClearAll(self, event):
        """清除所有监控数据"""
        dlg = wx.MessageDialog(self, _("Are you sure clear all data?"),
                               _("Are you sure?"), wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Freeze()
            self.request_tree.DeleteChildren(self.tree_root)
            self.info_notebook.DeleteAllPages()
            Cache.ClearCache(init=True)
            self.Thaw()
        dlg.Destroy()
    
    def OnPreferences(self, event):
        """打开设置窗口"""
        preferences = self.res.LoadDialog(None, 'preferencesDialog')
        preferences.Center()
        if preferences.ShowModal() == wx.ID_OK:
            preferences.Save()
        preferences.Destroy()
    
    def OnHomePage(self, event):
        """打开项目首页"""
        import webbrowser
        webbrowser.open('http://www.websniffer.cn')
    
    def OnAbout(self, event):
        """打开关于窗口"""
        aboutDialog  = self.res.LoadDialog(None, 'aboutDialog')
        aboutDialog.Center()
        aboutDialog.ShowModal()
        aboutDialog.Destroy()
    
    def OnExit(self, event):
        """退出窗口"""
        self.Close(True)
    
    def __del__(self):
        """退出程序时清除缓存"""
        Cache.ClearCache()
        if wx.Platform == '__WXMSW__':
            import _winreg as winreg
            from ctypes import windll
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                    'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings',
                    0, winreg.KEY_WRITE|winreg.KEY_READ)
            winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, '')
            winreg.CloseKey(key)
            windll.wininet.InternetSetOptionW(None, 39, None, 0)
