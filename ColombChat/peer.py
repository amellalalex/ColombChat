from settings import *
import socket
import threading

# WARNING! The mutex may be causing issues when trying to send/receive

class Peer:
    def __init__(self, conn_addr_pair=(None, '0.0.0.0')):
        self.conn = conn_addr_pair[0]
        self.addr = conn_addr_pair[1]
        self.handle = None
        self.lock = threading.Lock()
        
    def get(self):
        try:
            msg = self.conn.recv(msglen)
            if not msg:
                return None
            else:
                return msg
        except ConnectionAbortedError:
            print('ConnectionAbortedError, peer aborted.')
            return None
        except ConnectionResetError:
            print('ConnectionResetError, remote host forcibly closed connection.')
            return None

    def send(self, msg):
        self.conn.send(bytes(msg, 'utf-8'))
        
    def close(self):
        self.conn.close()