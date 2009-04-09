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
import gzip

import chardet

_blanklines = ('\r\n', '\n')

class ParseInfo(object):
    
    def __init__(self):
        self.request = StringIO()
        self.response = StringIO()
        self.request_header = {}
        self.response_header = {}
    
    def write(self, method, s):
        """写入请求数据"""
        if method == 'request':
            self.request.write(s)
        elif method == 'response':
            self.response.write(s)
    
    def parse(self):
        self.request.seek(0)
        #request header
        self.request_commend = self.request.readline()
        for line in self.request:
            if not line: break
            if line in _blanklines: break
            key, value = line.split(':', 1)
            self.request_header[key] = value
        #request body
        self.requst_body = ''.join(self.request.readlines())
        request_body_encode = chardet.detect(self.requst_body).get('encoding')
        if request_body_encode and request_body_encode.lower() != 'utf-8':
            self.request_body = self.request_body.decode(request_body_encode, 'replace')
        
        self.response.seek(0)
        #response header
        self.response_commend = self.response.readline()
        for line in self.response:
            if not line: break
            if line in _blanklines: break
            key, value = line.split(':', 1)
            self.response_header[key] = value
        #response body
        chunked = self.response_header.get('Transfer-Encoding')
        if not chunked:
            chunked = ''
        if chunked.strip() == 'chunked':
            content = []
            chunk_size = int(self.response.readline()[:-2], 16)
            while chunk_size > 0:
                content.append(self.response.read(chunk_size))
                self.response.read(2)
                chunk_size = int(self.response.readline()[:-2], 16)
            self.response_body = ''.join(content)
        else:
            self.response_body = ''.join(self.response.readlines())
        try:
            if self.response_header.get('Content-Encoding').strip() == 'gzip':
                self.response_body = gzip.GzipFile(fileobj=StringIO(self.response_body)).read()
        except Exception, e:
            pass
        response_body_encode = chardet.detect(self.response_body).get('encoding')
        if response_body_encode:
            self.response_body = self.response_body.decode(response_body_encode, 'replace')
        self.raw_request = self.request.getvalue()
        self.raw_response = self.response.getvalue()
        del self.request
        del self.response

    def getHeader(self, method):
        if method == 'request':
            header = self.request_header
            headers = [self.request_commend]
        elif method == 'response':
            header = self.response_header
            headers = [self.response_commend]
        for key, value in header.items():
            headers.append('%s: %s' % (key, value))
        return ''.join(headers)
    
    def getBody(self, method):
        if method == 'request':
            return self.requst_body
        elif method == 'response':
            return self.response_body

    def raw(self, method):
        if method == 'request':
            return self.raw_request
        elif method == 'response':
            return self.raw_response
