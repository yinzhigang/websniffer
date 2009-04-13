# encoding: utf-8

import wx
from wx import xrc
import wx.gizmos

from cStringIO import StringIO
import cPickle as pickle
import urllib

import resource

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
        self.Bind(wx.EVT_MENU, self.OnExit, id=xrc.XRCID('menuExit'))
        self.Bind(wx.EVT_MENU, self.OnAbout, id=xrc.XRCID('helpAboutMenu'))
        self.Bind(wx.EVT_TOOL, self.OnProxyStart, id=xrc.XRCID('toolBarStart'))
        
        self.infoPanel = xrc.XRCCTRL(self, 'infoPanel')
        self.info_notebook = xrc.XRCCTRL(self, 'info_notebook')
        
        self.request_tree = xrc.XRCCTRL(self, 'request_tree')
        self.request_tree.Bind(wx.EVT_TREE_SEL_CHANGED,
              self.OnTreeRequestTreeSelChanged, id=xrc.XRCID('request_tree'))
        self.tree_root = self.request_tree.AddRoot('root')
    
    def OnTreeRequestTreeSelChanged(self, event):
        """ RequesTree选择更换事件 """
        item = event.GetItem()
        if self.request_tree.ItemHasChildren(item) is False:
            data = self.request_tree.GetItemPyData(item)
            data.seek(0)
            parse_info = pickle.load(data)
            self.ShowInfo(parse_info)
    
    def ShowInfo(self, parse_info):
        """ 显示相关请求信息 """
        self.infoPanel.Freeze()
        self.info_notebook.DeleteAllPages()
        #========== General Tab ===========
        generalPanpel = self.res.LoadPanel(self.info_notebook, 'generalPanel')
        self.info_notebook.AddPage(page=generalPanpel, select=True, text=_("General"))
        
        generalBoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        treeListCtrl1 = wx.gizmos.TreeListCtrl(id=-1,
              name='treeListCtrl1', parent=generalPanpel,
              size=generalPanpel.GetSize(),
              style=wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_DEFAULT_STYLE)
        treeListCtrl1.AddColumn(text=_('Name'), width=150)
        treeListCtrl1.AddColumn(text=_('Value'), width=350)
        root = treeListCtrl1.AddRoot('root')
        urlItem = treeListCtrl1.AppendItem(root, _('URL:'))
        treeListCtrl1.SetItemText(urlItem, parse_info.getUrl(), 1)
        hostItem = treeListCtrl1.AppendItem(root, _('Host:'))
        treeListCtrl1.SetItemText(hostItem, parse_info.getHost(), 1)
        clientItem = treeListCtrl1.AppendItem(root, _('Client:'))
        treeListCtrl1.SetItemText(clientItem, parse_info.getClient(), 1)
        contentTypeItem = treeListCtrl1.AppendItem(root, _('Content-Type:'))
        treeListCtrl1.SetItemText(contentTypeItem, parse_info.header('response', 'Content-Type'), 1)
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
                requestCookieListCtrl.SetStringItem(cookieItem, 1, urllib.unquote_plus(value.value))
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
                responseCookieListCtrl.SetStringItem(cookieItem, 1, urllib.unquote_plus(value.value))
                responseCookieListCtrl.SetStringItem(cookieItem, 2, urllib.unquote_plus(value['domain']))
                responseCookieListCtrl.SetStringItem(cookieItem, 3, urllib.unquote_plus(value['path']))
                i += 1
        
        content_type = parse_info.header('response', 'Content-Type')
        if content_type[:5] == 'image':
            try:
                responseBody = self.res.LoadPanel(responseBook, 'imagePanel')
                responseBodyImageCtrl = xrc.XRCCTRL(responseBody, 'image')
                response_body_image = StringIO(parse_info.getBodyContent('response'))
                image = wx.ImageFromStreamMime(response_body_image, content_type).ConvertToBitmap()
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
        self.infoPanel.Thaw()

    def OnProxyStart(self, event):
        import SocketServ
        if event.IsChecked():
            self.thread = SocketServ.StartServer('SocketServ', self)
            self.thread.setDaemon(1)
            self.thread.start()
        else:
            self.thread.stop()
            print 'Server Stop'

    def DoNewRequest(self, path, data = ''):
        """添加请求到树中"""
        import urlparse
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
        url = urlparse.urlunparse(('', '', path, params, query, ''))
        request = self.request_tree.AppendItem(host_item, url)
        self.request_tree.SetItemPyData(request, data)
    
    def LogWindow(self, message):
        print message

    def OnAbout(self, event):
        aboutDialog  = self.res.LoadDialog(None, 'aboutDialog')
        aboutDialog.Center()
        aboutDialog.ShowModal()
        aboutDialog.Destroy()
        
    def OnExit(self, event):
        """退出窗口"""
        self.Close(True)
