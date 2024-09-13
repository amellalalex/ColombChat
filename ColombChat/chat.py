import socket 
import time
import logging
import threading
from peer import Peer

port = 42069
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
        pass

    accept_incoming_thread.join()