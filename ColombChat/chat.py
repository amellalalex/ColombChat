import socket 
import time
import logging
import threading

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

if __name__ == '__main__':
    # Setup logging
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        format=format,
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    
    # Start accepting incoming connections on thread 
    accept_incoming_thread = threading.Thread(target=accept_incoming)
    accept_incoming_thread.start()

    while True:
        msg = input('>> ')
        for peer in peers:
            peer.send(msg)

    accept_incoming_thread.join()