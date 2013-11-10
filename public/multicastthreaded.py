import threading
import SocketServer
import socket
import struct


class MulticastRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print "{} wrote:".format(self.client_address[0])
        print data
        return


class ThreadedMulticast(SocketServer.ThreadingMixIn,
                        SocketServer.UDPServer, ):
    def __init__(self, multicast, ttl, server_address, handler_class=MulticastRequestHandler, ):
        SocketServer.UDPServer.__init__(self, server_address, handler_class)
        group = socket.inet_aton(multicast)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        ttl = struct.pack('b', ttl)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


def startmulticastthread(multicast, port, ttl):
    address = ('', port)
    server = ThreadedMulticast(multicast, ttl, address, MulticastRequestHandler, )
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()
    print 'Server loop running in thread:', t.getName()
    print raw_input("please input a key will quit: ")
    # Clean up
    server.shutdown()
    server.socket.close()
