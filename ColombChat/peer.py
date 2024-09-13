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
        self.lock.acquire(timeout=0.080)
        msg = self.conn.recv(msglen)
        self.lock.release()
        if not msg:
            return None
        else:
            return msg
    
    def send(self, msg):
        self.lock.acquire()
        self.conn.send(bytes(msg, 'utf-8'))
        self.lock.release()
        
    def close(self):
        self.lock.acquire()
        self.conn.close()
        self.lock.release()