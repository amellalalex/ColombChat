from settings import *
import socket
import threading
import logging

# WARNING! The mutex may be causing issues when trying to send/receive

class Peer:
    def __init__(self, hostname, conn_addr_pair):
        self.conn = conn_addr_pair[0]
        self.addr = conn_addr_pair[1]
        self.handle = None
        self.lock = threading.Lock()
        
        # Send hostname as part of connection init
        self.send(hostname)
        
        # First message received will be Peer's name 
        self.name = self.get()
        
    def get(self):
        try:
            msg = self.conn.recv(MSGLEN)
            if not msg:
                return None
            else:
                return msg
        except ConnectionAbortedError:
            logging.debug('ConnectionAbortedError, peer aborted.')
            return None
        except ConnectionResetError:
            logging.debug('ConnectionResetError, remote host forcibly closed connection.')
        except OSError:
            logging.debug('OSError, issue in the underlying socket driver.')
            return None
        
    def send(self, msg):
        self.conn.send(bytes(msg, 'utf-8'))
        
    def close(self):
        self.conn.close()