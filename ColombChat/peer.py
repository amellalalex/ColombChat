from settings import *
import socket

class Peer:
    def __init__(self, conn_addr_pair=(None, '0.0.0.0')):
        self.conn = conn_addr_pair[0]
        self.addr = conn_addr_pair[1]
        self.handle = None
        
    def get(self):
        msg = self.conn.recv(msglen)
        if not msg:
            return None
        else:
            return msg
    
    def send(self, msg):
        self.conn.send(bytes(msg, 'utf-8'))