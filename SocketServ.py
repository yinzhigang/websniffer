# encoding: utf-8
import socket, urlparse, SocketServer, rfc822, gzip, threading
import select
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from wx import CallAfter

class ProxyRequestHandler(SocketServer.StreamRequestHandler):
    
    def handle(self):
        """
        处理请求
        """
        raw_requestline = self.rfile.readline()
        if raw_requestline:
            [command, path, version] = raw_requestline.split()
            headers = rfc822.Message(self.rfile, 0)
            (scm, host, path, params, query, fragment) = urlparse.urlparse(path)
            #通知主窗口更新
            CallAfter(self.server.window.DoNewRequest, (host, path, params, query))
            headers['Connection'] = 'close'
            del headers['Proxy-Connection']
            print command, urlparse.urlunparse(('', '', path, params, query, ''))
            
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                i = host.find(':')
                if i >= 0:
                    host_port = host[:i], int(host[i+1:])
                else:
                    host_port = host, 80
                soc.connect(host_port)
                soc.send("%s %s %s\r\n" % (command,
                                       urlparse.urlunparse(('', '', path, params, query, '')),
                                       version))
                for key_val in headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                self._read_write(soc)
            except Exception, e :
                print 'error', e
            finally:
                soc.close()
                self.connection.close()
    
    def _read_write(self, soc, max_idling=20):
        """
        发回服务器返回数据
        """
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
                    else:
                        out = soc
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            else:
                print "\t" "idle", count
            if count == max_idling: break
#        
#        rfile = soc.makefile('rw', -1)
##        for i in rfile:
##            print i
##            print ''.join(map(lambda c: "%02X" % ord(c), i))
#        raw_responseline = rfile.readline()
#        self.wfile.write(raw_responseline)
#        headers = rfc822.Message(rfile, 0)
#        encoding = headers.get('Content-Encoding', '')
#        content_type = headers.get('Content-Type', '')
#        content = []
#        if headers.get('Transfer-Encoding') == 'chunked':
#            chunk_size = int(rfile.readline()[:-2], 16)
#            while chunk_size > 0:
#                content.append(rfile.read(chunk_size))
#                rfile.read(2)
#                chunk_size = int(rfile.readline()[:-2], 16)
#        else:
#            for i in rfile:
#                content.append(i)
#        content = "".join(content)
#        del headers['Transfer-Encoding']
#        headers['Content-Length'] = str(len(content))
#        self.wfile.write(headers)
#        self.wfile.write('\r\n')
#        self.wfile.write(content)
#        if encoding == 'gzip' and content_type[:4] == 'text':
#            print gzip.GzipFile(fileobj=StringIO(content)).read()
#        elif content_type[:4] == 'text':
#            print content
#        else:
#            print 'no text', content_type

class MBThreadingTCPServer(SocketServer.ThreadingTCPServer):

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
        CallAfter(self.window.LogWindow, 'SocketServ Started')
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
        CallAfter(self.window.LogWindow, 'SocketServ Stoping')
        self.server.server_close()
        CallAfter(self.window.LogWindow, 'SocketServ Stoped')

if __name__ == '__main__':
    server = MBThreadingTCPServer(('', 8789), ProxyRequestHandler)
    server.serve_forever()
