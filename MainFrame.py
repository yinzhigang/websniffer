# encoding: utf-8

import wx
from wx import xrc
import wx.gizmos

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
try:
    import cPickle as pickle
except ImportError:
    import pickle

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
        wx.CallAfter(self._PostInit)
    
    def _PostInit(self):
        """初始化窗口控件"""
        self.Bind(wx.EVT_MENU, self.OnExit, id=xrc.XRCID('menuExit'))
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
        self.info_notebook.AddPage(page=generalPanpel, select=True, text="General")
        
        generalBoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        treeListCtrl1 = wx.gizmos.TreeListCtrl(id=-1,
              name='treeListCtrl1', parent=generalPanpel,
              size=generalPanpel.GetSize(),
              style=wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_DEFAULT_STYLE)
        treeListCtrl1.AddColumn(text=u'Name', width=300)
        treeListCtrl1.AddColumn(text=u'Value', width=200)
        root = treeListCtrl1.AddRoot('root')
        hostItem = treeListCtrl1.AppendItem(root, 'Host:')
        treeListCtrl1.SetItemText(hostItem, 'www.blogbus.com', 1)
        clientItem = treeListCtrl1.AppendItem(root, 'Client:')
        treeListCtrl1.Expand(root)
        
        generalPanpel.SetSizer(generalBoxSizer)
        generalBoxSizer.Add(treeListCtrl1, 1, border=2, flag=wx.EXPAND)
        #========== End General Tab ===========
        #========== Request Tab ===========
        requestPanel = self.res.LoadPanel(self.info_notebook, 'notebookPanel')
        self.info_notebook.AddPage(page=requestPanel, select=False, text="Request")
        
        requestBook = xrc.XRCCTRL(requestPanel, 'noteBook')
        
        requestHeader = self.res.LoadPanel(requestBook, 'textPanel')
        requestHeaderTextCtrl = xrc.XRCCTRL(requestHeader, 'textCtrl')
        request_header_text = parse_info.getHeader('request')
        requestBook.AddPage(page=requestHeader, select=True, text="Headers")
        requestHeaderTextCtrl.SetValue(request_header_text)
        
        requestBody = self.res.LoadPanel(requestBook, 'textPanel')
        requestBodyTextCtrl = xrc.XRCCTRL(requestBody, 'textCtrl')
        request_body_text = parse_info.getBody('request')
        requestBook.AddPage(page=requestBody, select=False, text="Cookies")
        requestBodyTextCtrl.SetValue(request_body_text)
        
        requestRaw = self.res.LoadPanel(requestBook, 'textPanel')
        requestRawTextCtrl = xrc.XRCCTRL(requestRaw, 'textCtrl')
        request_raw_text = parse_info.raw('request')
        request_raw_text = repr(request_raw_text)
        requestBook.AddPage(page=requestRaw, select=False, text="Raw")
        requestRawTextCtrl.SetValue(request_raw_text)
        #========== End Request Tab ===========
        #========== Response Tab ===========
        responsePanel = self.res.LoadPanel(self.info_notebook, 'notebookPanel')
        self.info_notebook.AddPage(page=responsePanel, select=False, text="Response")
        
        responseBook = xrc.XRCCTRL(responsePanel, 'noteBook')
        
        responseHeader = self.res.LoadPanel(responseBook, 'textPanel')
        responseHeaderTextCtrl = xrc.XRCCTRL(responseHeader, 'textCtrl')
        response_header_text = parse_info.getHeader('response')
        responseBook.AddPage(page=responseHeader, select=True, text="Heasers")
        responseHeaderTextCtrl.SetValue(response_header_text)
        
        responseText = self.res.LoadPanel(responseBook, 'textPanel')
        responseBodyTextCtrl = xrc.XRCCTRL(responseText, 'textCtrl')
        response_body_text = parse_info.getBody('response')
        responseBook.AddPage(page=responseText, select=False, text="Text")
        responseBodyTextCtrl.SetValue(response_body_text)
        
        responseRaw = self.res.LoadPanel(responseBook, 'textPanel')
        responseRawTextCtrl = xrc.XRCCTRL(responseRaw, 'textCtrl')
        response_raw_text = parse_info.raw('response')#.decode('utf-8', 'ignore')
        response_raw_text = repr(response_raw_text)
        responseBook.AddPage(page=responseRaw, select=False, text="Raw")
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

    def OnExit(self, event):
        """退出窗口"""
        self.Close(True)
