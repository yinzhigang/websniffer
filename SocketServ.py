# encoding: utf-8
import sys
import socket, urlparse, SocketServer, threading
import select
import tempfile
import cPickle as pickle

from wx import CallAfter
import ParseInfo
from DataCache import Cache

_blanklines = ('\r\n', '\n')

class ProxyRequestHandler(SocketServer.StreamRequestHandler):
    
    def handle(self):
        """处理请求"""
        raw_requestline = self.rfile.readline()
        if raw_requestline:
            if raw_requestline[-2:] == '\r\n':
                reline = '\r\n'
            elif raw_requestline[-1:] == '\n':
                reline = '\n'
            [command, url, version] = raw_requestline.split()
            (scm, host, path, params, query, fragment) = urlparse.urlparse(url)
            
            parse_info = ParseInfo.ParseInfo()
            parse_info.setUrl(url)
            parse_info.setClient(self.client_address)
            
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                i = host.find(':')
                if i >= 0:
                    host_port = host[:i], int(host[i+1:])
                else:
                    host_port = host, 80
                soc.connect(host_port)
                parse_info.setHost(host, soc.getpeername())
#                print soc.getpeername()
                
                url = urlparse.urlunparse(('', '', path, params, query, ''))
                request_url_command = "%s %s %s%s" % (command, url, version, reline)
                
                soc.send(request_url_command)
                parse_info.write('request', request_url_command)
                
                content_len = None
                while True:
                    line = self.rfile.readline()
                    if not line:
                        break
                    if line[:16].lower() == 'proxy-connection':
                        line = "Connection: close%s" % (reline)
                    if line[:14].lower() == 'content-length':
                        content_len = int(line[15:])
                    soc.send(line)
                    parse_info.write('request', line)
                    if line in _blanklines:
                        if content_len:
                            postdata = self.rfile.read(content_len)
                            if postdata:
                                soc.send(postdata)
                                parse_info.write('request', postdata)
                        break
                self._read_write(soc, parse_info)
                
                parse_info.parse()
                
                cache_key = Cache.RandomString()
                dump = pickle.dumps(parse_info, protocol=1)
                Cache.Set(cache_key, dump)
                #通知主窗口更新
                CallAfter(self.server.window.DoNewRequest, (host, path, params, query), cache_key)
            except Exception, e:
                print 'error sock', e
            finally:
                soc.close()
                self.connection.close()
    
    def _read_write(self, soc, parse_info, max_idling=20):
        """ 发回服务器返回数据 """
        iw = [self.connection, soc]
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                        method = 'response'
                    else:
                        out = soc
                        method = 'request'
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        parse_info.write(method, data)
                        count = 0
            else:
                print "\t" "idle", count
            if count == max_idling: break

class MBThreadingTCPServer(SocketServer.ThreadingTCPServer):
    
    daemon_threads = True

    def __init__(self, address_tuple, handler, window):
        SocketServer.ThreadingTCPServer.__init__(self, address_tuple, handler)
        self.window = window
        self.__serving = True

    def serve_forever(self):
        while self.__serving:
            SocketServer.ThreadingTCPServer.handle_request(self)

    def shutdown(self):
        self.__serving = False

class StartServer(threading.Thread):
    
    address_tuple = ('', 8789)
    
    def __init__(self, threadname, window):
        threading.Thread.__init__(self)
        self.window = window
    
    def run(self):
        self.server = MBThreadingTCPServer(self.address_tuple, ProxyRequestHandler, self.window)
        self.server.serve_forever()
    
    def stop(self):
        self.server.shutdown()
        close_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            close_sock.connect(self.address_tuple)
        except Exception:
            pass
        finally:
            close_sock.close()
        self.server.server_close()

