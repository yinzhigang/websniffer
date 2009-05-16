# encoding: utf-8
'''
Created on Apr 6, 2009

@author: yinzhigang
'''
from StringIO import StringIO
import Cookie, httplib
import gzip
import urllib

import chardet

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
        #request header
        self.request.seek(0)
        self.request_commend = self.request.readline()
        self.request_header = httplib.HTTPMessage(self.request)
        #request body
        self.request_body = ''.join(self.request.readlines())
        request_body_encode = chardet.detect(self.request_body).get('encoding')
        if request_body_encode:
            self.request_body = self.request_body.decode(request_body_encode, 'replace')
        
        #response header
        self.response.seek(0)
        self.response_commend = self.response.readline()
        self.response_header = httplib.HTTPMessage(self.response)
        #response body
        chunked = self.response_header.get('Transfer-Encoding', '')
        if chunked == 'chunked':
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
            if self.response_header.get('Content-Encoding') == 'gzip':
                self.response_body = gzip.GzipFile(fileobj=StringIO(self.response_body)).read()
        except Exception, e:
            pass
        response_body_encode = chardet.detect(self.response_body).get('encoding')
        if response_body_encode:
            if response_body_encode.lower() == 'gb2312':
                response_body_encode = 'gb18030'
            self.response_body = self.response_body.decode(response_body_encode, 'replace')
        self.raw_request = self.request.getvalue()
        self.raw_response = self.response.getvalue()
        del self.request
        del self.response

    def getHeaderText(self, method):
        """获取请求或返回的元信息"""
        if method == 'request':
            header = self.request_header
            headers = [self.request_commend]
        elif method == 'response':
            header = self.response_header
            headers = [self.response_commend]
        for item in header.headers:
            headers.append(item)
        return ''.join(headers)
    
    def header(self, method, name):
        """获取元信息，单条"""
        if method == 'request':
            header = self.request_header
        elif method == 'response':
            header = self.response_header
        return header.get(name, '')
    
    def getBodyContent(self, method):
        """获取内容主体"""
        if method == 'request':
            return self.request_body
        elif method == 'response':
            return self.response_body
    
    def setUrl(self, url):
        """save fullurl with host"""
        self.url = url
    
    def getUrl(self):
        """return fullurl whith host"""
        return self.url
    
    def setHost(self, host, peername):
        """Set Request Host"""
        self.host = host
        self.peername = peername
    
    def getHost(self):
        """return request host with ip and port"""
        ip, port = self.peername
        return "%s/%s:%s" % (self.host, ip, port)
    
    def setClient(self, client):
        """client ip and port"""
        self.client = client
    
    def getClient(self):
        """return client ip and port"""
        return "%s:%s" % self.client
    
    def cookie(self, method):
        if method == 'request':
            cookie = self.header('request', 'cookie')
        elif method == 'response':
            cookie = self.header('response', 'Set-Cookie')
        if cookie:
            C = Cookie.SimpleCookie(cookie)
            return C
        else:
            return None

    def raw(self, method):
        """获取原始信息"""
        if method == 'request':
            return self.raw_request
        elif method == 'response':
            return self.raw_response

