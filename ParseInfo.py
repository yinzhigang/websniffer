# encoding: utf-8
'''
Created on Apr 6, 2009

@author: yinzhigang
'''
#try:
#    from cStringIO import StringIO
#except ImportError:
#    from StringIO import StringIO
from StringIO import StringIO
import rfc822

class ParseInfo(object):
    
    def __init__(self):
        self.request = StringIO()
        self.response = StringIO()
    
    def write(self, method, s):
        """写入请求数据"""
        if method == 'request':
            self.request.write(s)
        elif method == 'response':
            self.response.write(s)
    
    def parse(self):
        self.request.seek(0)
        for i in self.request:
            print i,
#        request_parsed = rfc822.Message(self.request, 0)
#        respose_parsed = rfc822.Message(self.response)
#        self.request_header = str(request_parsed)
