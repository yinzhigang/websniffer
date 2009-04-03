# encoding: utf-8

import wx
from wx import xrc
import wx.gizmos

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
        
        blogbus = self.request_tree.AppendItem(self.tree_root, 'www.blogbus.com')
        self.request_tree.AppendItem(blogbus, '<default>')
        ttitem = self.request_tree.AppendItem(blogbus, 'user/')
        self.request_tree.SetItemPyData(ttitem, 'abcdefgbbcc')
        gang = self.request_tree.AppendItem(self.tree_root, 'gang.blogbus.com')
        self.request_tree.AppendItem(gang, '<default>')
        zhigang = self.request_tree.AppendItem(self.tree_root, 'www.zhigang.net')
        self.request_tree.SetItemPyData(zhigang, 't8b6d/32')
    
    def OnTreeRequestTreeSelChanged(self, event):
        """ RequesTree选择更换事件 """
        item = event.GetItem()
        print self.request_tree.GetItemPyData(item)
        text = self.request_tree.GetItemText(item)
        self.ShowInfo(text)
    
    def ShowInfo(self, text):
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
        treeListCtrl1.SetItemText(clientItem, text, 1)
        treeListCtrl1.Expand(root)
        
        generalPanpel.SetSizer(generalBoxSizer)
        generalBoxSizer.Add(treeListCtrl1, 1, border=2, flag=wx.EXPAND)
        #========== End General Tab ===========
        #========== Request Tab ===========
        requestPanel = self.res.LoadPanel(self.info_notebook, 'notebookPanel')
        self.info_notebook.AddPage(page=requestPanel, select=False, text="Request")
        
        requestBook = xrc.XRCCTRL(requestPanel, 'noteBook')
        
        requestHeader = self.res.LoadPanel(requestBook, 'textPanel')
        requestBook.AddPage(page=requestHeader, select=True, text="Headers")
        
        requestBody = self.res.LoadPanel(requestBook, 'textPanel')
        requestBook.AddPage(page=requestBody, select=False, text="Cookies")
        #========== End Request Tab ===========
        #========== Response Tab ===========
        responsePanel = self.res.LoadPanel(self.info_notebook, 'notebookPanel')
        self.info_notebook.AddPage(page=responsePanel, select=False, text="Response")
        
        responseBook = xrc.XRCCTRL(responsePanel, 'noteBook')
        
        responseHeader = self.res.LoadPanel(responseBook, 'textPanel')
        responseBook.AddPage(page=responseHeader, select=True, text="Heasers")
        
        responseText = self.res.LoadPanel(responseBook, 'textPanel')
        responseBook.AddPage(page=responseText, select=False, text="Text")
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

    def DoNewRequest(self, path):
        self.request_tree.AppendItem(self.tree_root, path)
        pass
    
    def LogWindow(self, message):
        print message

    def OnExit(self, event):
        """退出窗口"""
        self.Close(True)
