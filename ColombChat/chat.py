import socket 
import time
import logging
import threading
import sys

from peer import Peer
from settings import *

peers = list()

def accept_incoming():
    logging.info('Listening for incoming connections...')
    # Setup listening socket
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen()
    # Listen forever
    while True:
        # Accept incoming peer connection
        peer = Peer(s.accept())
        logging.info('Received peer connection: '+str(peer.conn)+','+str(peer.addr))
        # Add peer to list of peers
        peers.append(peer)
        # Create peer monitoring thread 
        thread = threading.Thread(target=monitor_peer_for_incoming_msg, args=(peers[-1],))
        peers[-1].handle = thread
        peers[-1].handle.start()
    # end while True
        
def monitor_peer_for_incoming_msg(peer):
    logging.info('Monitoring peer '+str(peer.addr)+' for incoming messages...')
    while True:
        msg = peer.get()
        if msg != None:
            logging.info('Received message from peer '+str(peer.addr)+': '+str(msg))
        else:
            logging.info('Peer returned None. Removing them.')
            break
    # end while True
    peers.remove(peer)

def process_msg_as_cmd(msg):
    if len(msg) > 1 and msg[0] == '/':
        run_cmd(msg)
        return True 
    else:
        return False

def run_cmd(msg):
    tokens = msg.split(' ')
    
    if tokens[0] == '/connect' and len(tokens) >= 3:
        ip = tokens[1]
        port = int(tokens[2])

        logging.info('Connecting to peer '+str((ip, port))+'.')
        s = socket.socket()
        s.connect((ip, port)) # fmt = /connect <ip> <port>

        peer = Peer((s, (ip, port)))
        peers.append(peer)
        peers[-1].handle = threading.Thread(target=monitor_peer_for_incoming_msg, args=(peers[-1],))
        peers[-1].handle.start()
    # endif tokens[0] == '/connect' and len(tokens) >= 3
    elif tokens[0] == '/connect' and len(tokens) == 2:
        split_addr = tokens[1].split(':')
        ip = split_addr[0]
        port = int(split_addr[1])

        logging.info('Connecting to peer '+str(tokens[1])+'.')
        s = socket.socket()
        s.connect((ip, port))

        peer = Peer((s, (ip, port)))
        peers.append(peer)
        peers[-1].handle = threading.Thread(target=monitor_peer_for_incoming_msg, args=(peers[-1],))
        peers[-1].handle.start()
        
    # endif tokens[0] == '/connect' and len(tokens) == 2
    elif tokens[0] == '/close':
        for peer in peers:
            peer.close()

if __name__ == '__main__':
    # Setup logging
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        format=format,
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    
    # Override default port is command line arg present 
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    # Start accepting incoming connections on thread 
    accept_incoming_thread = threading.Thread(target=accept_incoming)
    accept_incoming_thread.start()

    while True:
        msg = input('>> ')
        if not process_msg_as_cmd(msg):
            for peer in peers:
                peer.send(msg)

    accept_incoming_thread.join()